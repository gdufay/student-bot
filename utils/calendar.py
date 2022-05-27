from __future__ import print_function

import datetime
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

class Calendar:
    """Wrapper class around google calendar"""

    # If modifying these scopes, delete the file token.json.
    SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

    def __init__(self, credentials_path="credentials.json", token_path="token.json", port=0):
        self.credentials_path = credentials_path
        self.token_path = token_path
        self.port = port
        self.creds = None
        self.service = None

    def connect(self) -> None:
        """Connect to calendar server"""
        # The file token.json stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists(self.token_path):
            self.creds = Credentials.from_authorized_user_file(self.token_path, Calendar.SCOPES)
        # If there are no (valid) credentials available, let the user log in.
        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    self.credentials_path, Calendar.SCOPES)
                self.creds = flow.run_local_server(port=self.port)
            # Save the credentials for the next run
            with open(self.token_path, 'w') as token:
                token.write(creds.to_json())

    def build(self) -> None:
        """Build the calendar service"""
        if not self.creds:
            print("Not connected. Connecting...")
            self.connect()

        try:
            service = build('calendar', 'v3', credentials=self.creds)
        except HttpError as error:
            print('An error occurred: %s' % error)

    def get_today_events(self):
        """Return all events occuring today"""
        pass

    def get_next_events(self):
        """Return the next incoming event"""
        pass

    def get_incoming_tasks(self, period=7):
        """Return all incoming tasks in the given period (in days)"""
        pass


#    try:
#        # Call the Calendar API
#        # now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
#        # print('Getting the upcoming 10 events')
#        # events_result = service.events().list(calendarId='primary', timeMin=now,
#        #                                       maxResults=10, singleEvents=True,
#        #                                       orderBy='startTime').execute()
#        # events = events_result.get('items', [])
#
#        # if not events:
#        #     print('No upcoming events found.')
#        #     return
#
#        # # Prints the start and name of the next 10 events
#        # for event in events:
#        #     start = event['start'].get('dateTime', event['start'].get('date'))
#        #     print(start, event['summary'])
#        calendars_result = service.calendarList().list().execute()
#        calendars = calendars_result.get('items', [])
#
#        if not calendars:
#            print("No calendars")
#            return
#
#        for calendar in calendars:
#            print(f"{calendar['summary']}, primary : {calendar.get('primary', False)}")
#
#    except HttpError as error:
#        print('An error occurred: %s' % error)
