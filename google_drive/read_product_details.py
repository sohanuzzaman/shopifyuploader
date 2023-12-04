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
    Create a Shopify product JSON object for items from Andara Temple, a shop featuring handmade jewelry and naturally occurring, Helena Houdova-curated crystal stones. Use the provided unstructured data from a Google Sheet:

    {formatted_data}

    Craft an SEO-friendly product description and title, adhering to these guidelines:

    1. Start with a captivating introduction. For jewelry, emphasize its handmade nature. For crystal stones, highlight their natural origin and curation by Helena Houdova.
    2. For crystals, describe the color, appearance, and natural qualities, linking them to love and peace. For jewelry, focus on craftsmanship and design details.
    3. Stress the product's authenticity, its unique source, and the legacy behind it.
    4. Explain the symbolic significance - for jewelry, focus on artisanal value; for crystals, on their spiritual and healing properties.
    5. Discuss the mystical energy, transformative healing, and spiritual growth associated with the product.
    6. Detail craftsmanship for jewelry and the careful selection process for crystals.
    7. Emphasize its use in meditation and spiritual practices.
    8. Highlight healing properties, such as chakra alignment for crystals, and the artisanal quality for jewelry.
    9. Provide specifics like dimensions, weight, and materials in a well-structured HTML format, avoiding congested paragraphs.
    10. Conclude with its aesthetic value and an invitation to add it to the reader's collection.
    11. Use emojis to enhance engagement, particularly in the introduction and conclusion.
    12. Set the product status as 'draft'.
    13. The product description should be 300 - 500 words long.
    14. Know the product type from the google sheet data. It's Either 

    Incorporate relevant keywords for SEO naturally. Metafield: 'ORIGIN' with key 'country_of_origin' and namespace 'custom'.
    """

    # Call OpenAI API
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo-1106",
        messages=[
            {"role": "system", "content": "You are a helpful assistant. Respond with JSON formatted outputs."},
            {"role": "user", "content": prompt}
        ]
    )

    # Extract the content from the ChatCompletionMessage
    response = completion.choices[0].message.content

    # Extract and return the JSON part from the response
    return extract_json(response)

# test_data = [['Name of the Product', 'Rare Magical Semi- Milky Soft Blue Andara'], ['Weight', '22'], ['Price', '122'], ['Quantity', '1'], ['Origin', 'Indonesia']]
# print (create_shopify_product_from_unstructured_data(test_data))