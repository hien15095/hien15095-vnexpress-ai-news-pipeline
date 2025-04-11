import os
import psycopg2
from psycopg2 import Error
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago
from crawl import get_cat_breeds
from transform import get_clean_cat_breeds
from save import insert_cats

# Tạo DAG
dag = DAG(
    'cats_data',
    default_args={'start_date': days_ago(1)},
    schedule_interval='0 9 * * *', #chay 9h sang moi ngay
    catchup=False
)

# Task data_task: Thu thập, xử lý và lưu dữ liệu
def data_task():
    data = get_cat_breeds()  # Thu thập dữ liệu từ crawl.py
    data_transformed = get_clean_cat_breeds(data)  # Biến đổi dữ liệu từ transform.py
    insert_cats(data_transformed)  # Lưu vào DB từ save.py

# Tạo PythonOperator cho task
data_duty = PythonOperator(
    task_id='data',
    python_callable=data_task,
    dag=dag,
)

# Thiết lập thứ tự thực thi (ở đây chỉ có một task)
data_duty
