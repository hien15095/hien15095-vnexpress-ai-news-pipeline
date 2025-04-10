from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator

# Đảm bảo đã set PYTHONPATH trong docker-compose để import được
from app.crawl import crawl_a
from app.transform import transform_articles
from app.save import save_to_postgres

default_args = {
    'owner': 'airflow',
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

def run_pipeline():
    articles = crawl_a()
    transformed = transform_articles(articles)
    save_to_postgres(transformed)
with DAG(
    dag_id='vnexpress_ai_news_pipeline',
    default_args=default_args,
    description='Pipeline crawl - transform - save AI news từ VnExpress',
    schedule_interval='*/5 * * * *',  # Chạy mỗi 5 phút
    start_date=datetime(2023, 1, 1),
    catchup=False,
    tags=['news', 'vnexpress'],
) as dag:
    run_pipeline_task = PythonOperator(
        task_id='run_pipeline',
        python_callable=run_pipeline,
    )
