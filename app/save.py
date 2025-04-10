import psycopg2
from psycopg2 import sql
import os

def create_table(conn):
    """Create table if not exists"""
    create_table_query = """
    CREATE TABLE IF NOT EXISTS vnexpress_articles (
        id SERIAL PRIMARY KEY,
        title TEXT NOT NULL,
        url TEXT NOT NULL UNIQUE,
        summary TEXT,
        time TEXT,
        author TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """
    
    with conn.cursor() as cursor:
        cursor.execute(create_table_query)
        conn.commit()

def save_to_postgres(articles):
    """Save articles to PostgreSQL database"""
    conn = None
    try:
        # Connect to PostgreSQL
        conn = psycopg2.connect(
            dbname=os.getenv('POSTGRES_DB', 'news_db'),
            user=os.getenv('POSTGRES_USER', 'postgres'),
            password=os.getenv('POSTGRES_PASSWORD', 'postgres'),
            host=os.getenv('POSTGRES_HOST', 'postgres'),
            port=os.getenv('POSTGRES_PORT', '5432')
        )
        
        # Create table if not exists
        create_table(conn)
        
        # Insert articles
        with conn.cursor() as cursor:
            insert_query = sql.SQL("""
                INSERT INTO vnexpress_articles (title, url, summary, time, author)
                VALUES (%s, %s, %s, %s, %s)
                ON CONFLICT (url) DO NOTHING;
            """)
            
            for article in articles:
                cursor.execute(insert_query, (
                    article['title'],
                    article['url'],
                    article['summary'],
                    article['time'],
                    article['author']
                ))
        
        conn.commit()
        print(f"Successfully saved {len(articles)} articles to PostgreSQL")
        
    except Exception as e:
        print(f"Error saving to PostgreSQL: {e}")
        if conn:
            conn.rollback()
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    from crawl import crawl_vnexpress_ai_articles
    from transform import transform_articles
    
    articles = crawl_vnexpress_ai_articles()
    transformed = transform_articles(articles)
    save_to_postgres(transformed)
