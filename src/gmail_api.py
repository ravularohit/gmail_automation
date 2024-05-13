import os
from src.logger_util import logging
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request


CREDENTIALS_FILE = './src/credentials.json'


API_SERVICE_NAME = 'gmail'
API_VERSION = 'v1'


def get_gmail_service():
    try:
        scopes = ['https://www.googleapis.com/auth/gmail.readonly',
                'https://www.googleapis.com/auth/gmail.modify']

        creds = None
        if os.path.exists(CREDENTIALS_FILE):
            flow = InstalledAppFlow.from_client_secrets_file(
                CREDENTIALS_FILE, scopes=scopes)
            creds = flow.run_local_server(port=0)
        else:
            raise FileNotFoundError(f"Credentials file not found: {CREDENTIALS_FILE}")
    except Exception:
        logging.exception("excpetion occured",exc_info=True)

    return build(API_SERVICE_NAME, API_VERSION, credentials=creds)


def list_messages(service, label_ids=['INBOX','UNREAD']):

    try:
        response = service.users().messages().list(userId='me', labelIds=label_ids).execute()
        messages = response.get('messages', [])
        return [message['id'] for message in messages]
    except Exception as e:
        logging.exception("excpetion occured",exc_info=True)
        return []


def get_message(service, message_id):
    try:
        message = service.users().messages().get(userId='me', id=message_id).execute()
        return message
    except Exception as e:
        logging.exception("excpetion occured",exc_info=True)
        return []
    

