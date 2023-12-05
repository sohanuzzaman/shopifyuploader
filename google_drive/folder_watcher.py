import time
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from drive_utils import create_drive_service
from images.get_images import list_images_in_folder
from images.delete_images import delete_images_from_cloudinary
from create_sheet import create_sheet_in_folder, append_to_sheet
from upload.serilize_data import get_product_details
from notification.email_sender import send_email


# Example usage
drive_service = create_drive_service()
# Your Google Drive integration logic here

def list_subfolders(service, folder_id):
    query = f"mimeType = 'application/vnd.google-apps.folder' and '{folder_id}' in parents"
    response = service.files().list(q=query, spaces='drive', fields='files(id, name)').execute()
    return response.get('files', [])

def find_2nd_degree_subfolders(service, parent_folder_id):
    first_degree_folders = list_subfolders(service, parent_folder_id)
    second_degree_folders = []

    for folder in first_degree_folders:
        subfolders = list_subfolders(service, folder['id'])
        second_degree_folders.extend(subfolders)

    return second_degree_folders

def update_folder_name(service, folder_id, new_name):
    # Update the folder metadata with the new name
    folder_metadata = {'name': new_name}

    # Update the folder on Google Drive
    service.files().update(fileId=folder_id, body=folder_metadata).execute()


def look_for_new_folders():
    drive_service = create_drive_service()
    parent_folder_id = "1Ju6LXgDpdre9oRNj_dC6LtzxLmRiT9-3"  # Your main folder ID

    while True:
        second_degree_folders = find_2nd_degree_subfolders(drive_service, parent_folder_id)
        folders_to_process = []

        for folder in second_degree_folders:
            if "(Uploaded)" not in folder['name']:
                folders_to_process.append(folder)
                print(f"Folder to process: {folder['name']} with ID: {folder['id']}")

        for folder in folders_to_process:
            time.sleep(900)
            product_detail_sheet = create_sheet_in_folder(folder['id'])
            images = list_images_in_folder(drive_service, folder['id'])
            
            # Prepare data for appending
            data_to_append = []
            for image in images:
                # Assuming image is a tuple with the first element as 'url' and the second as 'public_id'
                url, public_id = image 
                data_to_append.append([url, public_id])

            # Append data to the sheet
            append_to_sheet(spreadsheet_id=product_detail_sheet, data=data_to_append)
            upload_to_shopify = get_product_details(product_detail_sheet, images)
            if upload_to_shopify.status_code == 201:
                # Prepend "(Uploaded)" to the folder name
                updated_name = "(Uploaded) " + folder['name']
                update_folder_name(drive_service, folder['id'], updated_name)

                # Extract public IDs from data_to_append for deletion
                public_ids_to_delete = [item[1] for item in data_to_append]
                delete_images_from_cloudinary(public_ids_to_delete)
                
        send_email()
        time.sleep(3 * 3600)  # Sleep for 3 hours

look_for_new_folders()


look_for_new_folders()