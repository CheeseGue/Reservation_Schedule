from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from googleapiclient.errors import HttpError
import base64
from base64 import urlsafe_b64encode
import datetime
import pytz

from utils.gmail_service import get_gmail_service
from utils.helpers import determine_recipient_email

def send_reservation_email(service, to_email, subject, body):
  """
  Gmail APIを使用して予約確認メールを送信します。

  Args:
      service: 認可済みのGmailサービスオブジェクト。
      to_email: 受信者メールアドレス。
      subject: メール件名。
      body: メール本文。

  Returns:
      None
  """

  message = MIMEMultipart('mixed')
  message['To'] = to_email
  message['Subject'] = subject

  # メッセージ本文用に text/plain 部分を作成
  text_part = MIMEText(body, 'plain')
  message.attach(text_part)

  
  encoded_message = urlsafe_b64encode(message.as_bytes()).decode('utf-8')
  raw_message = {'raw': encoded_message}


  try:
        service.users().messages().send(userId='me', body=raw_message).execute()
        print("予約確認メールを正常に送信しました!")
  except HttpError as error:
        print(f"メールの送信に失敗しました: {error}")

def main():
  # この関数はテスト目的のみであり、Flaskアプリケーションでは呼び出されません。
  # メール送信機能をテストするために、実際の引数を使用してこの関数を呼び出すことができます。
  pass

if __name__ == '__main__':
  main()
