from images.crop import smart_crop_image
import os

def list_images_in_folder(service, folder_id):
    """
    List all images in a specified Google Drive folder, crop them, and save locally.

    :param service: The authenticated Google Drive service instance.
    :param folder_id: The ID of the folder in which to search for images.
    :return: A list of paths to the locally saved cropped images.
    """
    query = f"mimeType contains 'image/' and '{folder_id}' in parents and trashed = false"
    response = service.files().list(q=query, spaces='drive', fields='files(id, name, webContentLink)').execute()
    images = response.get('files', [])

    cropped_image_paths = []
    for image in images:
        image_url = image['webContentLink']
        cropped_image = smart_crop_image(image_url)
        cropped_image_paths.append(cropped_image)

    return cropped_image_paths
