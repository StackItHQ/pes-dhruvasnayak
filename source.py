import gspread
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import os
import pickle

# Define the scope for accessing Google Sheets and Google Drive
SCOPES = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']

# Path to store the credentials token
TOKEN_PICKLE = 'token.pickle'

def get_credentials():
    creds = None
    # Check if we have saved credentials from a previous session
    if os.path.exists(TOKEN_PICKLE):
        with open(TOKEN_PICKLE, 'rb') as token:
            creds = pickle.load(token)

    # If credentials are not available or are invalid, we go through the OAuth flow
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('client_secret.json', SCOPES)
            creds = flow.run_local_server(port=8080)

        # Save the credentials for the next run
        with open(TOKEN_PICKLE, 'wb') as token:
            pickle.dump(creds, token)

    return creds

def get_sheet():
    # Authenticate and get the credentials
    creds = get_credentials()

    # Authorize with the credentials
    client = gspread.authorize(creds)

    # Open the Google Sheet by name
    sheet = client.open("gs_data").sheet1  # You can specify the worksheet by index or name
    return sheet

# Create operation: Add a new row
def create_row(data):
    sheet = get_sheet()
    sheet.append_row(data)
    print("Row added successfully!")

# Read operation: Get a row by ID
def read_row_by_id(id):
    sheet = get_sheet()
    records = sheet.get_all_records()
    for row in records:
        if row['id'] == id:
            return row
    return None

# Update operation: Modify a row by ID
def update_row_by_id(id, new_data):
    sheet = get_sheet()
    cell = sheet.find(str(id))  # Find the cell containing the ID
    if cell:
        row_number = cell.row
        sheet.update(f'A{row_number}:D{row_number}', [new_data])  # Update the row with new data
        print(f"Row with ID {id} updated successfully!")
    else:
        print(f"Row with ID {id} not found.")

# Delete operation: Remove a row by ID
def delete_row_by_id(id):
    sheet = get_sheet()
    cell = sheet.find(str(id))  # Find the cell containing the ID
    if cell:
        row_number = cell.row
        sheet.delete_rows(row_number)
        print(f"Row with ID {id} deleted successfully!")
    else:
        print(f"Row with ID {id} not found.")

if __name__ == '__main__':
   
    create_row([2, "John", 25, "male"])
    create_row([1, "John", 25, "male"])

    
    update_row_by_id(1, [1, "Dhruva", 22, "male"])

    # Delete: Remove a row by ID
    delete_row_by_id(2)
