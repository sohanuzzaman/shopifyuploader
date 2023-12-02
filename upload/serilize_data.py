import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from google_drive.read_product_details import format_data_from_sheet
from images.delete_images import delete_images_from_cloudinary
from .shopify_upload import product_uploader

def get_product_details(sheet_id, images):
    """
    Retrieves product details from a Google Sheet, formats images, uploads products to Shopify, 
    and manages images on Cloudinary.

    :param sheet_id: The ID of the Google Sheet containing product details.
    :param images: A tuple where the first item is an image link and the second item is the public ID.
    :return: The response from the Shopify product upload function.
    """

    # Retrieve product details from the sheet
    product_details = format_data_from_sheet(sheet_id) 

    # Format images into the required structure
    formatted_images = [{"src": image[0]} for image in images]

    # Insert formatted images into the product details
    if 'product' in product_details:
        product_details['product']['images'] = formatted_images
    else:
        # Handle cases where the 'product' key is missing in the product details
        raise KeyError("The 'product' key is missing in the product details.")

    # Upload the product to Shopify
    print(product_details)
    shopify_response = product_uploader(product_details)

    # If the product is added successfully, delete the images from Cloudinary
    if shopify_response.status_code == 201:  # Assuming the response indicates success
        public_ids = [image[1] for image in images]
        delete_images_from_cloudinary(public_ids)

    # Return the response from Shopify upload
    return shopify_response

# Ensure your product_uploader function can handle the updated product_details structure.
