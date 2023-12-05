import requests
import json
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv('../.env')

# Environment variables for API credentials
SHOP_NAME = os.getenv('SHOPIFY_SHOP_NAME')
ACCESS_TOKEN = os.getenv('SHOPIFY_ADMIN_API_ACCESS_TOKEN')

# Verify if the necessary environment variables are loaded
if not SHOP_NAME or not ACCESS_TOKEN:
    print("Missing required environment variables: SHOPIFY_SHOP_NAME or SHOPIFY_ADMIN_API_ACCESS_TOKEN")
    exit(1)

# Shopify API endpoint for creating a product
url = f"https://{SHOP_NAME}.myshopify.com/admin/api/2023-01/products.json"

# Headers including the access token
headers = {
    "Content-Type": "application/json",
    "X-Shopify-Access-Token": ACCESS_TOKEN
}

def product_uploader(product_data):
    # Extract the product details from the provided data
    product_info = product_data['product']

    # Prepare the product payload for the Shopify API
    product_payload = product_data

    # Making a POST request to Shopify API
    response = requests.post(url, headers=headers, json=product_payload)

    if response.status_code == 201:
        # Successfully created the product
        print(response)
        return response
    else:
        # Error occurred
        return {"error": response.text}

# Usage with dynamic product data
# dynamic_product_data = { ... }  # This should be provided by another part of your code
# response = product_uploader(dynamic_product_data)
# print(response)
