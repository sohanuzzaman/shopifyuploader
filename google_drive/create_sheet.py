from drive_utils import create_drive_service, create_sheets_service
# Create the Google Sheets service instance
sheets_service = create_sheets_service()

def check_existing_sheet(folder_id, sheet_title="Product Info"):
    """
    Check if a Google Sheet with a given title exists in a specified folder.

    :param folder_id: The ID of the folder to search in.
    :param sheet_title: The title of the sheet to search for.
    :return: The ID of the existing sheet if found, otherwise None.
    """
    drive_service = create_drive_service()

    # Search for the file in the specified folder
    query = f"name = '{sheet_title}' and '{folder_id}' in parents and mimeType = 'application/vnd.google-apps.spreadsheet'"
    response = drive_service.files().list(q=query, spaces='drive').execute()

    for file in response.get('files', []):
        # Return the first matching file's ID
        return file.get('id')
    return None

def create_sheet_in_folder(folder_id, sheet_title="Product Info"):
    """
    Create or find a Google Sheet in a specified folder with a given title.

    :param folder_id: The ID of the folder where the sheet will be placed.
    :param sheet_title: The title of the Google Sheet. Default is 'Product Info'.
    :return: The ID of the found or newly created sheet.
    """
    existing_sheet_id = check_existing_sheet(folder_id, sheet_title)
    if existing_sheet_id:
        print(f"Sheet '{sheet_title}' already exists with ID: {existing_sheet_id}")
        return existing_sheet_id
    """
    Copy a specific template Google Sheet to a specified folder with a given title.

    :param folder_id: The ID of the folder where the copied sheet will be placed.
    :param sheet_title: The title of the new copied Google Sheet. Default is 'Product Info'.
    :return: The ID of the newly created sheet if successful, or None if an error occurs.
    """
    template_sheet_id = '1zCertz7JF85FipT25nEfytYOt4yUgf-uj4sxn9ABMpY'  # Template sheet ID

    try:
        drive_service = create_drive_service()

        # Copy the template sheet
        copied_file = {'name': sheet_title}
        sheet_copy = drive_service.files().copy(fileId=template_sheet_id, body=copied_file).execute()

        # Move the copied sheet to the desired folder
        file_id = sheet_copy['id']
        file = drive_service.files().get(fileId=file_id, fields='parents').execute()
        previous_parents = ",".join(file.get('parents'))
        drive_service.files().update(fileId=file_id,
                                     addParents=folder_id,
                                     removeParents=previous_parents,
                                     fields='id, parents').execute()

        return file_id
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

# Example usage
# folder_id = 'YOUR_FOLDER_ID'  # Replace with the actual folder ID
# new_sheet_id = create_sheet_in_folder(folder_id)
# if new_sheet_id:
#     print(f"Sheet created successfully with ID: {new_sheet_id}")
# else:
#     print("Failed to create sheet")




def append_to_sheet(spreadsheet_id, data, sheet_name="Images"):
    """
    Append data to a specific Google Sheet.

    :param sheets_service: The authenticated Google Sheets service instance.
    :param spreadsheet_id: The ID of the spreadsheet to update.
    :param data: A list of rows to append, where each row is a list of values.
    :param sheet_name: The name of the sheet in the spreadsheet to update. Default is 'Images'.
    :return: None
    """
    range = f"{sheet_name}!A:B"  # Assuming you want to add data to columns A and B
    value_input_option = 'USER_ENTERED'
    insert_data_option = 'INSERT_ROWS'
    value_range_body = {
        "values": data
    }

    request = sheets_service.spreadsheets().values().append(
        spreadsheetId=spreadsheet_id,
        range=range,
        valueInputOption=value_input_option,
        insertDataOption=insert_data_option,
        body=value_range_body
    )
    response = request.execute()
    print(f"Data appended successfully: {response}")

# Example usage
# sheets_service = create_sheets_service()
# spreadsheet_id = new_sheet_id  # The ID of the newly created spreadsheet
# data_to_append = [['url1', 'public_id1'], ['url2', 'public_id2']]  # Example data
# append_to_sheet(sheets_service, spreadsheet_id, data_to_append)
