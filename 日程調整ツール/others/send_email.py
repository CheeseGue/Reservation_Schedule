import os
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from email.mime.text import MIMEText
from googleapiclient.errors import HttpError
import base64


def send_test_email(to_email, subject, body):
    """Gmail APIを使用してテストメールを送信します."""

    # クライアント秘密キーファイルから認証情報を読み込みます
    flow = InstalledAppFlow.from_client_secrets_file('/Users/ootsuka/Desktop/プログラミング/製作物/日程調整ツール/credentials.json', SCOPES)
    creds = flow.run_local_server(port=0)
    service = build('gmail', 'v1', credentials=creds)

    # 電子メールメッセージを準備します
    message = MIMEText(body)
    message['to'] = to_email
    message['from'] = EMAIL_ADDRESS
    message['subject'] = subject

    # メッセージを base64 でエンコードします
    encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode('utf-8')

    # メッセージ本文を作成します
    raw_message = {
        'raw': encoded_message
    }

    # メールを送信します
    try:
        service.users().messages().send(userId='me', body=raw_message).execute()
        print(f"テストメールを {to_email} に送信しました!")
    except HttpError as error:
        print(f"テストメールの送信に失敗しました: {error}")


# 受信者メールアドレスとテストメールの内容を置き換えます
to_email = "otsukads@gmail.com"
subject = "Gmail APIからのテストメール"
body = "これは、Gmail APIを使用して送信されたテストメールです。"


# Gmail アドレス用の環境変数を設定します
EMAIL_ADDRESS = os.getenv('EMAIL_ADDRESS')

# OAuth 認証情報とスコープを正しく設定していることを確認します
SCOPES = ['https://www.googleapis.com/auth/gmail.send']


# send_test_email 関数を呼び出してメールを送信します
send_test_email(to_email, subject, body)
