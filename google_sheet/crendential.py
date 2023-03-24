import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

def load_credential():
    """Load credential from token.json or create a new one"""
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('temp/token.json'):
        creds = Credentials.from_authorized_user_file('temp/token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'temp/credentials.json', SCOPES)
            creds = flow.run_local_server(port=56789)
        # Save the credentials for the next run
        with open('temp/token.json', 'wt', encoding='UTF-8') as token:
            token.write(creds.to_json())
   
    return creds
