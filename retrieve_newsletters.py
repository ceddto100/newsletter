import os
import base64
import pickle
from google.oauth2 import service_account
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.auth.transport.requests import Request

# Set the scopes required to access the Gmail API
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

# Function to authenticate and build the Gmail API service
def authenticate_gmail():
    creds = None
    # Load credentials from token.pickle if available
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)

    # If credentials are not available or expired, initiate new login flow
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)

        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    # Build the Gmail API service
    service = build('gmail', 'v1', credentials=creds)
    return service

# Function to retrieve specific emails from the inbox
def get_specific_emails(service, user_id='me', query='', max_results=50):
    try:
        # Search for emails based on the given query
        results = service.users().messages().list(userId=user_id, q=query, maxResults=max_results).execute()
        messages = results.get('messages', [])

        if not messages:
            print('No emails found matching the query.')
            return

        # Loop through the messages and get their content
        for msg in messages:
            msg_id = msg['id']
            message = service.users().messages().get(userId=user_id, id=msg_id).execute()

            # Decode email content
            payload = message['payload']
            headers = payload.get('headers', [])
            data = payload.get('body', {}).get('data')

            if data:
                decoded_data = base64.urlsafe_b64decode(data).decode('utf-8')
                print(decoded_data)
            else:
                parts = payload.get('parts', [])
                for part in parts:
                    if part.get('mimeType') == 'text/plain':
                        data = part['body']['data']
                        decoded_data = base64.urlsafe_b64decode(data).decode('utf-8')
                        print(decoded_data)

    except HttpError as error:
        print(f'An error occurred: {error}')

if __name__ == '__main__':
    # Install required dependencies
    # Run the following command in your terminal to install the required libraries:
    # pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib

    # Authenticate and get the Gmail API service
    gmail_service = authenticate_gmail()

    # Define the query to retrieve specific emails
    email_query = 'from:aibreakfastemail@gmail.com OR from:futuretools@mail.beehiiv.com OR from:news@lore.com OR from:hello@mindstream.news OR from:aisupremacy@substack.com'

    # Retrieve specific emails from the inbox
    get_specific_emails(gmail_service, query=email_query, max_results=50)
    def render_html():
        return