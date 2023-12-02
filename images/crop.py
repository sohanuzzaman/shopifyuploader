import requests
from PIL import Image
from io import BytesIO
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv('../.env')

CLOUDINARY_API_KEY = os.getenv('CLOUDINARY_API_KEY')
CLOUDINARY_API_SECRET = os.getenv('CLOUDINARY_API_SECRET')

import uuid
import cloudinary
import cloudinary.uploader
          
cloudinary.config( 
  cloud_name = "dyp7u4bv0", 
  api_key = CLOUDINARY_API_KEY, 
  api_secret = CLOUDINARY_API_SECRET
)



def smart_crop_image(image_url, width=1000, height=1000):
    # Generate a random public ID
    public_id = str(uuid.uuid4())

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

# def smart_crop_image(image_url, resolution="1000x1000"):
#     # Endpoint for smart-cropping
#     endpoint = 'https://api.imagga.com/v2/croppings'

#     # Sending GET request to Imagga API
#     response = requests.get(
#         f'{endpoint}?image_url={image_url}&resolution={resolution}',
#         auth=(IMAGGA_API_KEY, IMAGGA_API_SECRET)
#     )

#     if response.status_code != 200:
#         raise Exception("Error in API request")

#     # Parsing response to get cropping coordinates
#     json_response = response.json()
#     croppings = json_response['result']['croppings']
#     if not croppings:
#         raise Exception("No cropping suggestion found")

#     cropping = croppings[0]  # Taking the first suggested cropping
#     x1, y1, x2, y2 = cropping['x1'], cropping['y1'], cropping['x2'], cropping['y2']

#     # Download the image
#     response = requests.get(image_url)
#     image = Image.open(BytesIO(response.content))

#     # Crop the image using coordinates
#     cropped_image = image.crop((x1, y1, x2, y2))

#     # Save or return the cropped image
#     cropped_image_path = 'cropped_image.jpg'
#     cropped_image.save(cropped_image_path)
#     print(f"Cropped image saved as {cropped_image_path}")

#     return cropped_image


