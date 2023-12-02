from drive_utils import create_sheets_service

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

    # Initialize a dictionary to hold the product data
    product_data = {}

    # Process each key-value pair
    for row in values:
        if len(row) >= 2:
            key, value = row[0], row[1]
            product_data[key] = value

    # Now build the product structure
    product = {
        "title": product_data.get("Name of the Product", ""),
        "body_html": "<strong>Great product!</strong>",
        "vendor": "Your Vendor Name",
        "product_type": "Crystal Stone",
        "tags": ["Andara Crystal", "Love"],
        "variants": [{
            "price": product_data.get("Price", "0"),
            "grams": int(product_data.get("Weight", "0")),
            "inventory_quantity": int(product_data.get("Quantity", "0"))
        }],
        "images": [],  # Populate with image URLs if available
        "metafields": [
            {
                "key": "country_of_origin",
                "value": product_data.get("Origin", ""),
                "value_type": "string",
                "namespace": "custom"
            }
        ]
    }
    return {"product": product}

# Example usage
# sheet_id = '1zCertz7JF85FipT25nEfytYOt4yUgf-uj4sxn9ABMpY'
# formatted_data = format_data_from_sheet(sheet_id)
# print(formatted_data)
