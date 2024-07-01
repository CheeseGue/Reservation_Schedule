import os
from flask import Flask, render_template, request, jsonify
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from email.mime.text import MIMEText
from googleapiclient.errors import HttpError
import base64
import datetime
import pytz

from utils.calendar_service import get_calendar_service, get_free_busy_times
from utils.gmail_service import get_gmail_service, send_reservation_email
from utils.helpers import determine_recipient_email

app = Flask(__name__)

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

@app.route('/send_reservation', methods=['POST'])
def send_reservation():
    data = request.get_json()
    start_times = data.get('start_times', [])
    end_times = data.get('end_times', [])

    message_content = "予約詳細:\n"
    for i, (start_time, end_time) in enumerate(zip(start_times, end_times)):
        reservation_number = i + 1

        jst_timezone = pytz.timezone('Asia/Tokyo')
        start_datetime_jst = pytz.utc.localize(datetime.datetime.strptime(start_time, '%Y-%m-%dT%H:%M:%S.%fZ')).astimezone(jst_timezone)
        end_datetime_jst = pytz.utc.localize(datetime.datetime.strptime(end_time, '%Y-%m-%dT%H:%M:%S.%fZ')).astimezone(jst_timezone)
        time_format = '%Y年%m月%d日 %H:%M'

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
