import pandas as pd
from crawl import get_cat_breeds

def get_clean_cat_breeds(data):
    default_image = "https://cdn2.thecatapi.com/images/aae.jpg"
    cleaned_data = []
    for breed in data:
        # Làm sạch temperament
        temperament_str = breed.get('temperament', '')
        temperament_list = [item.strip() for item in temperament_str.split(',')] if temperament_str else []

        # Kiểm tra image_url
        image_url = breed.get('image', {}).get('url')
        if not image_url:
            image_url = default_image

        cleaned_data.append({
            'id': breed.get('id'),
            'name': breed.get('name'),
            'origin': breed.get('origin'),
            'temperament': temperament_list,
            'life_span': breed.get('life_span'),
            'image_url': image_url
        })

    return cleaned_data

