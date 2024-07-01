from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

CLIENT_SECRETS_FILE_PATH = '/Users/ootsuka/Desktop/プログラミング/製作物/日程調整ツール/credentials.json'

SCOPES = 'https://www.googleapis.com/auth/calendar.readonly'

def get_calendar_service():
    flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_FILE_PATH, SCOPES)
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
