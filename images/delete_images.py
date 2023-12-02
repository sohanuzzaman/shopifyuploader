from dotenv import load_dotenv
import os
import cloudinary

# Load environment variables from .env file
load_dotenv('../.env')

CLOUDINARY_API_KEY = os.getenv('CLOUDINARY_API_KEY')
CLOUDINARY_API_SECRET = os.getenv('CLOUDINARY_API_SECRET')


cloudinary.config( 
  cloud_name = "dyp7u4bv0", 
  api_key = CLOUDINARY_API_KEY, 
  api_secret = CLOUDINARY_API_SECRET
)


def delete_images_from_cloudinary(public_ids):
    # Delete images
    try:
        response = cloudinary.api.delete_resources(public_ids)
        return response
    except Exception as e:
        return str(e)