import requests
import pandas as pd

def get_cat_breeds():
    url = "https://api.thecatapi.com/v1/breeds"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        cats = []

        for breed in data:
            # Xử lý image_url
            image_url = breed.get('image', {}).get('url')
            if not image_url:
                ref_id = breed.get('reference_image_id')
                if ref_id:
                    image_url = f"https://cdn2.thecatapi.com/images/{ref_id}.jpg"
                else:
                    image_url = "https://cdn2.thecatapi.com/images/aae.jpg"

            cats.append({
                'id': breed.get('id'),
                'name': breed.get('name'),
                'origin': breed.get('origin'),
                'temperament': breed.get('temperament', '').strip(),
                'life_span': breed.get('life_span'),
                'image_url': image_url
            })

        return cats

