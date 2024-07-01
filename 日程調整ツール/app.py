from flask import Flask, render_template, request, jsonify
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import datetime
import smtplib
from email.mime.text import MIMEText

app = Flask(__name__)

SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

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
    data = request.json
    start_date = data['start_date']
    end_date = data['end_date']
    
    service = get_calendar_service()
    busy_times = get_free_busy_times(service, start_time=start_date, end_time=end_date)
    
    return jsonify(busy_times)

@app.route('/send_reservation', methods=['POST'])
def send_reservation():
    data = request.json
    start_times = data.get('start_times', [])
    end_times = data.get('end_times', [])

    message_content = "予約の詳細:\n"
    for start, end in zip(start_times, end_times):
        message_content += f"開始時間: {start}, 終了時間: {end}\n"

    msg = MIMEText(message_content)
    msg['Subject'] = '予約確認'

    # 必ずメールアドレスの部分は確認する
    
    msg['From'] = 'your_email@example.com'
    msg['To'] = 'recipient@example.com'

    try:
        with smtplib.SMTP('smtp.example.com', 587) as server:
            server.starttls()
            server.login('your_email@example.com', 'your_password')
            server.sendmail('your_email@example.com', 'recipient@example.com', msg.as_string())
        return jsonify(success=True)
    except Exception as e:
        print(f"Failed to send email: {e}")
        return jsonify(success=False), 500

if __name__ == '__main__':
    app.run(debug=True)
