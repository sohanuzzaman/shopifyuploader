import time
from drive_utils import create_drive_service
from get_images import list_images_in_folder
from create_sheet import create_sheet_in_folder, append_to_sheet


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
            product_detail_sheet = create_sheet_in_folder(folder['id'])
            images = list_images_in_folder(drive_service, folder['id'])
            
            # Prepare data for appending
            data_to_append = []
            for image in images:
                # Assuming image is a tuple with the first element as 'url' and the second as 'public_id'
                url, public_id = image  # Unpack the tuple
                data_to_append.append([url, public_id])

            # Append data to the sheet
            append_to_sheet(spreadsheet_id=product_detail_sheet, data=data_to_append)



        time.sleep(1000)  # Wait for approximately 12 minutes before checking again

look_for_new_folders()


look_for_new_folders()