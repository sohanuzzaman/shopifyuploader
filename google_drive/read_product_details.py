from drive_utils import create_sheets_service
from dotenv import load_dotenv
import os, re
from openai import OpenAI

import json

# Load environment variables from .env file
load_dotenv('../.env')

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
OPENAI_ORGANIZATION = os.getenv('OPENAI_ORGANIZATION')

# Function to read and format data from a Google Sheet
def format_data_from_sheet(sheet_id):
    service = create_sheets_service()

    # Specify the sheet and range you want to read
    range_name = 'Product Details'
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=sheet_id, range=range_name).execute()
    values = result.get('values', [])

    if not values:
        print('No data found.')
        return

    # Call the function to create Shopify product object
    shopify_product = create_shopify_product_from_unstructured_data(values)
    return shopify_product


def extract_json(response):
    # Regex pattern to match the outermost JSON structure
    json_pattern = r'\{.*\}'

    # Search for JSON in the response
    match = re.search(json_pattern, response, re.DOTALL)
    if match:
        try:
            # Parse the JSON string
            json_data = json.loads(match.group())
            return json_data
        except json.JSONDecodeError:
            print("Failed to parse JSON from the matched string.")
            return None
    else:
        print("No JSON found in the response.")
        return None
    

def create_shopify_product_from_unstructured_data(sheet_data):
    # Set up OpenAI API
    client = OpenAI(api_key=OPENAI_API_KEY)

    # Convert sheet data to a more readable string format for the prompt
    # formatted_data = "\n".join([f"{item[0]}: {item[1]}" for item in sheet_data])
    formatted_data = sheet_data

    # Prepare the prompt for OpenAI, asking for a JSON formatted response
    prompt = f"""
    Create a Shopify product JSON object for items listed in Andara Temple, using the following data from a Google Sheet:
    
    {formatted_data}
    
    Based on the product type, generate an SEO-friendly product title and over 600 word description Personalize the description for women interested in spirituality and astrology:

    If the Product Type is 'Crystal stone' write the description with the following sections (Don't mention the section number in the description):
    1. Capture audience's attention with an engaging description, focus on the spritual purpose and benefits. (60 words or more)
    2. Write a section title with crystal emojies in the begining and end. The section is about how this crystal is especial and personally curated by helena. Followed by a 60 words description, bullet points with emojies as list style
    3. Title similer to this '🙏🏼 Spiritual Benefits and Healing Properties 🙏🏼' followd by 80 words description (highlight 3-4 points)
    4. Section tile is something like '📜 Specifications and Materials 📜'. Highlight the Type, Color, Source, condition... etc. Section length 50 words
    5. 💖 Honoring Our Lemurian Roots 💖, Describe our ethos of love, compassion, and ethical integrity.
    6. Write a descripption similer to this '💫 Thank you so much for taking the time to explore the mystical world of Andara crystals in my shop. May you find the piece that resonates with your soul's journey. If you feel called by the magic of this PRODUCT NAME HERE' remember that it has been waiting just for you.
    7. Conclude with a variation of this '🙌 Check out the entire collection in my shop for more treasures that might catch your spirit's eye. Thank you for embarking on this journey with me – may love and light guide your path. 🙌' 
    
    If the Product Type is 'Jewelry':
    Description sections:
    1. Start with an enchanting opening, focusing on the handmade nature and artisanal value of the jewelry. (60 or more words)
    2. Describe the design, materials, and the craftsmanship detail.
    3. Title similer to this '🙏🏼 Spiritual Benefits and Healing Properties 🙏🏼' followd by 80 words description (highlight 3-4 points)
    4. Emphasize the unique qualities and the craftsmanship of each piece.
    5 4. Section tile is something like '📜 Specifications and Materials 📜'.
    6. Write a descripption similer to this '💫 Thank you so much for taking the time to explore our creations. May you find the piece that resonates with your soul's journey. If you feel called by the magic of this PRODUCT NAME HERE' remember that it has been waiting just for you.
    7. Conclude with a variation of this '🙌 Check out the entire collection in my shop for more treasures that might catch your spirit's eye. Thank you for embarking on this journey with me – may love and light guide your path. 🙌' 


    Additional Instructions:
    - The product description should be formatted in HTML for visual appeal and clarity.
    - Description word count can't be less than required
    - Provided examples are just suggestions, be creative
    - Set the product status to 'draft'.
    - Add a Metafield 'ORIGIN' with key 'country_of_origin' and namespace 'custom'.
    """

    # Call OpenAI API
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo-1106",
        messages=[
            {"role": "system", "content": "You are a marketing genius specialized in Etsy product marketing. Your responses should be formatted as JSON objects."},
            {"role": "user", "content": prompt}
        ]
    )

    # Extract the content from the ChatCompletionMessage
    response = completion.choices[0].message.content

    # Extract and return the JSON part from the response
    return extract_json(response)

# test_data = [['Name of the Product', 'Light Green Rare Andara with Bubbles and White Mineral'], ['Weight', '22'], ['Price', '122'], ['Quantity', '1'], ['Origin', 'Indonesia'], ['tags/keywords', 'Andara Crystal, Raw Crystal, Activated Crystal, Healing Andara Crystal, Spritulity, Love and compassion, Helena Houdova']]
# print (create_shopify_product_from_unstructured_data(test_data))
