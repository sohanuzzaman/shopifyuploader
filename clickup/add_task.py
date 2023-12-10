import os
import requests
from datetime import datetime, timedelta
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv('../.env')

# Environment variables for API credentials
CLICKUP_API_KEY = os.getenv('CLICKUP_API_TOKEN')

# Debugging: Print the API key to verify it's being loaded (Remove this in production)
print(f"API Key: {CLICKUP_API_KEY}")

def add_clickup_task(product_id, product_name):
    """
    Adds a task to a specified list in ClickUp with the due date set to the next day.
    The task is not assigned to any specific individual.

    :param task_title: Title of the task.
    :param task_description: Description of the task.
    :return: Response from the ClickUp API.
    """

    # Fixed list ID
    list_id = "900303602406"
    
    # Task details 
    task_title = f"Update {product_name} details and publish on shopify"
    task_description = f"This is the direct link to edit product details:\nhttps://admin.shopify.com/store/4f9f2b/products/{product_id}"

    # Endpoint for creating a task in ClickUp
    url = f"https://api.clickup.com/api/v2/list/{list_id}/task"

    # Headers with authorization and content type
    headers = {
        "Authorization": CLICKUP_API_KEY,
        "Content-Type": "application/json"
    }

    # Calculate the next day's date in Unix timestamp
    due_date = int((datetime.now() + timedelta(days=1)).timestamp() * 1000)

    # Task data
    task_data = {
        "name": task_title,
        "description": task_description,
        "due_date": due_date
    }

    try:
        # Making a POST request
        response = requests.post(url, headers=headers, json=task_data)
        response.raise_for_status()  # Raises a HTTPError for bad requests
        return response.json()
    except requests.exceptions.HTTPError as err:
        return {"error": f"HTTP error occurred: {err}"}
    except requests.exceptions.RequestException as err:
        return {"error": f"Request error occurred: {err}"}

# Example usage
# product_id = "8754076975400"  # Replace with actual product ID
# response = add_clickup_task(product_id)
# print(response)
