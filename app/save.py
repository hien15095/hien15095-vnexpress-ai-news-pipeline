import psycopg2
import os
import requests
from crawl import get_cat_breeds
from transform import get_clean_cat_breeds


def insert_cats(cat_data_list):
    connection = None
    cursor = None
    try:
        # Kết nối đến PostgreSQL
        connection = psycopg2.connect(
            host='postgres',
            database='airflow',
            user='airflow',
            password='airflow'
        )
        cursor = connection.cursor()

        # Tạo bảng nếu chưa có
        create_table_query = """
        CREATE TABLE IF NOT EXISTS Cats (
            id VARCHAR PRIMARY KEY,
            name VARCHAR,
            origin VARCHAR,
            temperament TEXT[] NOT NULL,
            life_span VARCHAR,
            image_url VARCHAR
        );
        """
        cursor.execute(create_table_query)

        # Lệnh INSERT
        insert_query = """
        INSERT INTO Cats (id, name, origin, temperament, life_span, image_url)
        VALUES (%s, %s, %s, %s, %s, %s)
        """

        for cat in cat_data_list:
            # 'temperament' đang là list, ví dụ ["Active","Energetic","Gentle"]
            # Ta có thể truyền list trực tiếp cho cột TEXT[]
            values = (
                cat['id'],
                cat['name'],
                cat['origin'],
                cat['temperament'],   # chính là list Python
                cat['life_span'],
                cat['image_url']
            )
            cursor.execute(insert_query, values)

        connection.commit()
        print("Chèn dữ liệu thành công!")
    except psycopg2.Error as e:
        print("Lỗi PostgreSQL:", e)
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()


##luu anh ve data
def download_images(cat_data_list, folder):
    # Tạo thư mục nếu chưa tồn tại
    if not os.path.exists(folder):
        os.makedirs(folder)
    
    for cat in cat_data_list:
        img_url = cat.get('image_url')
        cat_id = cat.get('id')
        if img_url and cat_id:
            try:
                # Gửi request lấy dữ liệu hình ảnh
                r = requests.get(img_url, stream=True)
                if r.status_code == 200:
                    # Đường dẫn file: folder/<id>.jpg
                    file_path = os.path.join(folder, f"{cat_id}.jpg")
                    # Ghi file ảnh
                    with open(file_path, 'wb') as f:
                        for chunk in r.iter_content(1024):
                            f.write(chunk)
                    print(f"Tải ảnh cho {cat['name']} thành công: {file_path}")
                else:
                    print(f"Lỗi tải ảnh cho {cat['name']}, status code: {r.status_code}")
            except Exception as e:
                print(f"Lỗi khi tải ảnh cho {cat['name']}: {e}")
