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

# Product data without variants
product_data = {
    "product": {
        "title": "test product 4",
        "body_html": "<strong>Great product!</strong>",
        "vendor": "Your Vendor Name",
        "product_type": "Your Product Type",
        "tags": ["Andara Crystal", "Andara from Egypt"],
        "variants": [{
            "price": "100.00",
            "grams": 100
        }],
        "images": [
            {"src": "https://res.cloudinary.com/dyp7u4bv0/image/upload/v1701440431/c2335b48-f1cf-419b-a7ce-29c0828ec6d3.jpg"},
            {"src": "https://res.cloudinary.com/demo/image/upload/c_crop,h_200,w_200/docs/models.jpg"}
        ]
    }
}


def product_uploader():
    # Make a POST request to create a new product
    response = requests.post(url, headers=headers, data=json.dumps(product_data))

    # Check the response
    if response.status_code == 201:
        print("Product created successfully.")
        return response
    else:
        print(f"Failed to create product. Status Code: {response.status_code}, Response: {response.text}")
