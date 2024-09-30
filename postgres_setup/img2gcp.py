import os
import requests
import io
from google.cloud import storage
from PIL import Image

# Unsplash API credentials
UNSPLASH_ACCESS_KEY = 'FBsefRi9xXfKtGQPCCCSjUOQm2mmUVO2TC0liLXN5X0'
UNSPLASH_API_URL = 'https://api.unsplash.com/search/photos'

# GCP Storage details
BUCKET_NAME = 'mtc-cloud101-cars'

# Car makes and models
makes_and_models = {
    'Toyota': ['Camry', 'Corolla', 'Rav4', 'Highlander', 'Tacoma'],
    'Honda': ['Civic', 'Accord', 'CR-V', 'Pilot', 'Odyssey'],
    'Ford': ['F-150', 'Escape', 'Explorer', 'Mustang', 'Focus'],
    'Chevrolet': ['Silverado', 'Equinox', 'Malibu', 'Traverse', 'Camaro'],
    'Nissan': ['Altima', 'Rogue', 'Sentra', 'Murano', 'Pathfinder'],
    'BMW': ['3 Series', '5 Series', 'X3', 'X5', '7 Series'],
    'Mercedes-Benz': ['C-Class', 'E-Class', 'GLC', 'GLE', 'S-Class'],
    'Audi': ['A4', 'Q5', 'A6', 'Q7', 'A3'],
    'Volkswagen': ['Jetta', 'Passat', 'Tiguan', 'Atlas', 'Golf'],
    'Hyundai': ['Elantra', 'Sonata', 'Tucson', 'Santa Fe', 'Kona']
}

def fetch_image_from_unsplash(query):
    params = {
        'query': query,
        'per_page': 1,
        'client_id': UNSPLASH_ACCESS_KEY
    }
    response = requests.get(UNSPLASH_API_URL, params=params)
    data = response.json()
    if 'results' in data and len(data['results']) > 0:
        return data['results'][0]['urls']['regular']
    return None

def download_and_resize_image(url):
    response = requests.get(url)
    img = Image.open(io.BytesIO(response.content))
    img = img.resize((800, 600), Image.LANCZOS)
    img_byte_arr = io.BytesIO()
    img.save(img_byte_arr, format='JPEG')
    img_byte_arr = img_byte_arr.getvalue()
    return img_byte_arr

def upload_to_gcs(bucket, blob_name, data):
    blob = bucket.blob(blob_name)
    blob.upload_from_string(data, content_type='image/jpeg')
    return blob.public_url

def main():
    # Initialize GCS client
    storage_client = storage.Client()
    bucket = storage_client.bucket(BUCKET_NAME)

    for make, models in makes_and_models.items():
        for model in models:
            query = f"{make} {model} car"
            print(f"Fetching image for {query}...")
            
            image_url = fetch_image_from_unsplash(query)
            if image_url:
                try:
                    image_data = download_and_resize_image(image_url)
                    blob_name = f"{make}_{model}.jpg"
                    public_url = upload_to_gcs(bucket, blob_name, image_data)
                    print(f"Uploaded {blob_name} to GCS: {public_url}")
                except Exception as e:
                    print(f"Error processing {query}: {str(e)}")
            else:
                print(f"No image found for {query}")

if __name__ == "__main__":
    main()