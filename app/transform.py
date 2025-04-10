import re
from bs4 import BeautifulSoup
import warnings
from bs4 import MarkupResemblesLocatorWarning

warnings.filterwarnings("ignore", category=MarkupResemblesLocatorWarning)

def clean(text):
    """Làm sạch HTML và chuẩn hóa khoảng trắng"""
    if not isinstance(text, str):
        return 'Không rõ'
    return re.sub(r'\s+', ' ', BeautifulSoup(text, 'html.parser').get_text()).strip()

def transform_articles(articles):
    transformed = []
    for article in articles:
        transformed.append({
            'title': clean(article.get('raw_title', '')),
            'url': article.get('url', ''),
            'summary': clean(article.get('raw_summary', '')),
            'time': clean(article.get('raw_time', '')),
            'author': clean(article.get('raw_author', ''))
        })
    return transformed

if __name__ == "__main__":
    from crawl import crawl_a
    articles = crawl_a()
    transformed = transform_articles(articles)
    print(transformed)