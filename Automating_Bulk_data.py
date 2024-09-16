import pandas as pd
import requests

# Define API endpoint 
API_URL = 'https://api.ecommerceplatform.com/v1/products'
API_KEY = 'your_api_key_here'

df = pd.read_csv('products.csv')

# to upload a single product
def upload_product(product_data):
    headers = {
        'Authorization': f'Bearer {API_KEY}',
        'Content-Type': 'application/json'
    }
    response = requests.post(API_URL, json=product_data, headers=headers)
    if response.status_code == 201:
        print(f"Product {product_data['name']} uploaded successfully.")
    else:
        print(f"Failed to upload product {product_data['name']}. Status code: {response.status_code}")

# Iterate over each row in the DataFrame and upload the product
for index, row in df.iterrows():
    product_data = {
        'name': row['name'],
        'description': row['description'],
        'price': row['price'],
        'image_url': row['image_url']
    }
    upload_product(product_data)