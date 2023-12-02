import os
import time
from google.oauth2 import service_account
from googleapiclient.discovery import build

def create_drive_service():
    # Path to your service_account_file.json
    service_account_file = '../ancient-lattice-406804-51b8cc893821.json' 

    # Scopes required by the application
    scopes = ['https://www.googleapis.com/auth/drive']

    # Authenticate using the service account file
    credentials = service_account.Credentials.from_service_account_file(service_account_file, scopes=scopes)

    # Build the service
    service = build('drive', 'v3', credentials=credentials)
    return service


def create_sheets_service():
    # Path to your service_account_file.json
    service_account_file = '../ancient-lattice-406804-51b8cc893821.json' 

    # Scopes required by the application
    # The scope for Sheets API is different from Drive API
    scopes = ['https://www.googleapis.com/auth/spreadsheets']

    # Authenticate using the service account file
    credentials = service_account.Credentials.from_service_account_file(service_account_file, scopes=scopes)

    # Build the service
    service = build('sheets', 'v4', credentials=credentials)
    return service
