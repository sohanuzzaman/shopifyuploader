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
# sample_payload = {
#     "product": {
#         "title": "Example Product",
#         "body_html": "<strong>Good quality product</strong>",
#         "vendor": "John's Apparel",
#         "product_type": "T-Shirts",
#         "tags": "cotton, summer",
#         "variants": [
#             {
#                 "option1": "Small",
#                 "price": "19.99",
#                 "sku": "123"
#             },
#             {
#                 "option1": "Medium",
#                 "price": "19.99",
#                 "sku": "124"
#             },
#             {
#                 "option1": "Large",
#                 "price": "19.99",
#                 "sku": "125"
#             }
#         ],
#         "images": [
#             {
#                 "src": "http://example.com/burton.jpg"
#             }
#         ]
#     }
# }
# response = product_uploader(sample_payload)
# print(response)
# Sample response.text
# {"product":{"id":8809299083560,"title":"Example Product","body_html":"\u003cstrong\u003eGood quality product\u003c\/strong\u003e","vendor":"John's Apparel","product_type":"T-Shirts","created_at":"2023-12-07T08:50:19+08:00","handle":"example-product","updated_at":"2023-12-07T08:50:19+08:00","published_at":"2023-12-07T08:50:19+08:00","template_suffix":null,"published_scope":"global","tags":"cotton, summer","status":"active","admin_graphql_api_id":"gid:\/\/shopify\/Product\/8809299083560","variants":[{"id":47293312663848,"product_id":8809299083560,"title":"Small","price":"19.99","sku":"123","position":1,"inventory_policy":"deny","compare_at_price":null,"fulfillment_service":"manual","inventory_management":null,"option1":"Small","option2":null,"option3":null,"created_at":"2023-12-07T08:50:19+08:00","updated_at":"2023-12-07T08:50:19+08:00","taxable":true,"barcode":null,"grams":0,"image_id":null,"weight":0.0,"weight_unit":"g","inventory_item_id":49345146192168,"inventory_quantity":0,"old_inventory_quantity":0,"requires_shipping":true,"admin_graphql_api_id":"gid:\/\/shopify\/ProductVariant\/47293312663848"},{"id":47293312696616,"product_id":8809299083560,"title":"Medium","price":"19.99","sku":"124","position":2,"inventory_policy":"deny","compare_at_price":null,"fulfillment_service":"manual","inventory_management":null,"option1":"Medium","option2":null,"option3":null,"created_at":"2023-12-07T08:50:19+08:00","updated_at":"2023-12-07T08:50:19+08:00","taxable":true,"barcode":null,"grams":0,"image_id":null,"weight":0.0,"weight_unit":"g","inventory_item_id":49345146224936,"inventory_quantity":0,"old_inventory_quantity":0,"requires_shipping":true,"admin_graphql_api_id":"gid:\/\/shopify\/ProductVariant\/47293312696616"},{"id":47293312729384,"product_id":8809299083560,"title":"Large","price":"19.99","sku":"125","position":3,"inventory_policy":"deny","compare_at_price":null,"fulfillment_service":"manual","inventory_management":null,"option1":"Large","option2":null,"option3":null,"created_at":"2023-12-07T08:50:19+08:00","updated_at":"2023-12-07T08:50:19+08:00","taxable":true,"barcode":null,"grams":0,"image_id":null,"weight":0.0,"weight_unit":"g","inventory_item_id":49345146257704,"inventory_quantity":0,"old_inventory_quantity":0,"requires_shipping":true,"admin_graphql_api_id":"gid:\/\/shopify\/ProductVariant\/47293312729384"}],"options":[{"id":11137377829160,"product_id":8809299083560,"name":"Title","position":1,"values":["Small","Medium","Large"]}],"images":[],"image":null}}
