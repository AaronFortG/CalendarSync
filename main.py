from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import time
from datetime import datetime

# Set up the Google Calendar API
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']


def get_credentials():
    flow = InstalledAppFlow.from_client_secrets_file(
        'credentials.json', SCOPES)
    credentials = flow.run_local_server(port=0)
    return credentials


def main():
    credentials = get_credentials()
    service = build('calendar', 'v3', credentials=credentials)

    print("Listening for real-time updates. Press Ctrl+C to stop.")
    last_check_time = datetime.utcnow()

    while True:
        print("New update")
        events_result = service.events().list(
            calendarId='primary', updatedMin=last_check_time.isoformat() + 'Z').execute()
        events = events_result.get('items', [])

        if events:
            for event in events:
                event_id = event['id']
                print("New Event ID:", event_id)
                print("Summary:", event.get('summary', 'N/A'))
                print("Location:", event.get('location', 'N/A'))
                print("Start:", event['start'].get('dateTime', event['start'].get('date')))
                print("End:", event['end'].get('dateTime', event['end'].get('date')))
                print("Description:", event.get('description', 'N/A'))
                print("Organizer:", event.get('organizer', {}).get('displayName', 'N/A'))
                print("-----")
                last_check_time = datetime.utcnow()  # Update last check time to prevent duplicate event retrieval

        time.sleep(10)  # Wait for 10 seconds before checking for updates again


if __name__ == '__main__':
    main()
