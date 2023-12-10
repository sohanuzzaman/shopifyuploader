import cloudinary.uploader
import os
import uuid
import time
from dotenv import load_dotenv
import sys

# Load environment variables from .env file
load_dotenv('../.env')

CLOUDINARY_API_KEY = os.getenv('CLOUDINARY_API_KEY')
CLOUDINARY_API_SECRET = os.getenv('CLOUDINARY_API_SECRET')

cloudinary.config( 
  cloud_name = "dyp7u4bv0", 
  api_key = CLOUDINARY_API_KEY, 
  api_secret = CLOUDINARY_API_SECRET
)

def smart_crop_image(image_url, width=1000, height=1000, max_retries=5, retry_delay=900):
    for attempt in range(max_retries):
        try:
            # Generate a random public ID
            public_id = str(uuid.uuid4())

            # Upload image directly from the URL
            response = cloudinary.uploader.upload(
                image_url,
                public_id=public_id,
                width=width,
                height=height,
                gravity="auto",
                crop="fill",
                fetch_format="auto",
                quality="auto"
            )
            return response['url'], public_id

        except cloudinary.exceptions.Error as e:
            print(f"Attempt {attempt + 1} failed: {e}")
            if attempt < max_retries - 1:
                print(f"Retrying in {retry_delay} seconds...")
                time.sleep(retry_delay)
            else:
                print("Max retries reached. Failed to upload image.")
                sys.exit()

# Example usage
image_url = "https://drive.google.com/uc?id=1iFmxThasfjNE7fYsENRu47epOuOy3Hpi&export=download"
result_url, public_id = smart_crop_image(image_url)
if result_url:
    print("Image uploaded successfully:", result_url)
else:
    print("Failed to upload image.")
