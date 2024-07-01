import os
from flask import Flask, render_template, request, jsonify
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import smtplib
from email.mime.text import MIMEText
from googleapiclient.errors import HttpError
import base64
from base64 import urlsafe_b64encode
import datetime
import pytz

app = Flask(__name__)

SCOPES = ['https://www.googleapis.com/auth/calendar.readonly', 'https://www.googleapis.com/auth/gmail.send']

def get_calendar_service():
    flow = InstalledAppFlow.from_client_secrets_file('/Users/ootsuka/Desktop/プログラミング/製作物/日程調整ツール/credentials.json', SCOPES)
    creds = flow.run_local_server(port=0)
    service = build('calendar', 'v3', credentials=creds)
    return service

def get_free_busy_times(service, calendar_id='primary', start_time=None, end_time=None):
    events_result = service.events().list(
        calendarId=calendar_id, timeMin=start_time, timeMax=end_time,
        singleEvents=True, orderBy='startTime').execute()
    events = events_result.get('items', [])
    
    busy_times = []
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        end = event['end'].get('dateTime', event['end'].get('date'))
        busy_times.append((start, end))
    
    return busy_times

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/confirm_reservation.html')
def confirm_reservation():
    return render_template('confirm_reservation.html')

@app.route('/get_free_busy_times', methods=['POST'])
def get_free_busy_times_api():
    data = request.get_json()
    start_date = data['start_date']
    end_date = data['end_date']
    
    service = get_calendar_service()
    busy_times = get_free_busy_times(service, start_time=start_date, end_time=end_date)
    
    return jsonify(busy_times)

# クライアント秘密キーファイルのパスを置き換えます
CLIENT_SECRETS_FILE_PATH = '/Users/ootsuka/Desktop/プログラミング/製作物/日程調整ツール/credentials.json'

# Gmailアドレスを置き換えます
EMAIL_ADDRESS = os.getenv('EMAIL_ADDRESS')

# Gmailパスワードを置き換えます
EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD')

def determine_recipient_email(data):
    # ロジックを実装する
    # 例:
    # - 主催者メールアドレスがあれば、それを利用する
    # - チーム/プロジェクトアドレスがあれば、それを利用する
    # - 適切なアドレスが見つからない場合は、エラーを発生させる
    
    recipient_email = data.get('organizer_email', 'otsukads@gmail.com')
    
    return recipient_email

def get_gmail_service():
    """
    提供された認証情報を使用して Gmail API サービスオブジェクトを構築して返します。
    """
    credentials = get_credentials()
    service = build('gmail', 'v1', credentials=credentials)
    return service


def get_credentials():
    """
    クライアント秘密キーファイルから OAuth2 認証情報を読み込みます。
    """
    flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_FILE_PATH, SCOPES)
    credentials = flow.run_local_server(port=0)
    return credentials


def send_reservation_email(service, to_email, subject, body):
    """
    Gmail API を使用して予約確認メールを送信します。
    """
    message = MIMEText(body)
    message['to'] = to_email
    message['from'] = EMAIL_ADDRESS
    message['subject'] = subject

    encoded_message = urlsafe_b64encode(message.as_bytes()).decode('utf-8')
    raw_message = {'raw': encoded_message}

    try:
        service.users().messages().send(userId='me', body=raw_message).execute()
        print("予約確認メールを正常に送信しました!")
    except HttpError as error:
        print(f"メールの送信に失敗しました: {error}")


@app.route('/send_reservation', methods=['POST'])
def send_reservation():
    """
    予約確認メールを送信するための POST リクエストを処理します。
    """
    data = request.get_json()
    start_times = data.get('start_times', [])
    end_times = data.get('end_times', [])

    message_content = "予約詳細:\n"
    for i, (start_time, end_time) in enumerate(zip(start_times, end_times)):
        # 予約件数
        reservation_number = i + 1

        # 日本時間に変換
        # pytz ライブラリをインストールする必要があります: pip install pytz
        import pytz

        # 日本時間 (JST) のタイムゾーンを取得
        jst_timezone = pytz.timezone('Asia/Tokyo')

        # 開始時間と終了時間を JST に変換
        start_datetime_jst = pytz.utc.localize(datetime.datetime.strptime(start_time, '%Y-%m-%dT%H:%M:%S.%fZ')).astimezone(jst_timezone)
        end_datetime_jst = pytz.utc.localize(datetime.datetime.strptime(end_time, '%Y-%m-%dT%H:%M:%S.%fZ')).astimezone(jst_timezone)

        # 時刻フォーマット (秒を含む)
        time_format = '%Y年%m月%d日 %H:%M'

        # 予約詳細メッセージに更新
        message_content += f"{reservation_number}件目: 開始時間: {start_datetime_jst.strftime(time_format)}, 終了時間: {end_datetime_jst.strftime(time_format)}\n"


    recipient_email = determine_recipient_email(data)

    send_reservation_email(
        get_gmail_service(),
        to_email=recipient_email,
        subject="予約確認",
        body=message_content
    )

    return jsonify(success=True)


if __name__ == '__main__':
    app.run(debug=True)
