from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from email.mime.text import MIMEText
from googleapiclient.errors import HttpError
import base64
import os

SCOPES = 'https://www.googleapis.com/auth/gmail.send'

CLIENT_SECRETS_FILE_PATH = '/Users/ootsuka/Desktop/プログラミング/製作物/日程調整ツール/credentials.json'
EMAIL_ADDRESS = os.getenv('EMAIL_ADDRESS')
EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD')

def get_gmail_service():
    credentials = get_credentials()
    service = build('gmail', 'v1', credentials=credentials)
    return service

def get_credentials():
    flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_FILE_PATH, SCOPES)
    credentials = flow.run_local_server(port=0)
    return credentials

def send_reservation_email(service, to_email, subject, body):
    message = MIMEText(body)
    message['to'] = to_email
    message['from'] = EMAIL_ADDRESS
    message['subject'] = subject

    encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode('utf-8')
    raw_message = {'raw': encoded_message}

    try:
        service.users().messages().send(userId='me', body=raw_message).execute()
        print("予約確認メールを正常に送信しました!")
    except HttpError as error:
        print(f"メールの送信に失敗しました: {error}")
