from __future__ import print_function

from datetime import datetime, timedelta
import pytz
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google.oauth2 import service_account
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from .course import Course

class Calendar:
    """Wrapper class around google calendar"""

    # If modifying these scopes, delete the file token.json.
    SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

    def __init__(self, credentials_path="credentials.json", token_path="token.json", port=0, tz="Europe/Paris"):
        self.credentials_path = credentials_path
        self.token_path = token_path
        self.port = port
        self.creds = None
        self.service = None
        self.tz = tz

    def connect(self) -> None:
        """Connect to calendar server"""
        #self.creds = service_account.Credentials.from_service_account_file(self.credentials_path, scopes=Calendar.SCOPES)
        #self.creds = delegated_credentials = credentials.with_subject('dufaygaetan.gd@gmail.com')

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
                token.write(self.creds.to_json())

    def build(self) -> None:
        """Build the calendar service"""
        if not self.creds:
            print("Not connected. Connecting...")
            self.connect()

        try:
            self.service = build('calendar', 'v3', credentials=self.creds)
        except HttpError as error:
            print('An error occurred: %s' % error)

    # TODO: type annotation
    def get_today_events(self):
        """Return all events occuring today"""
        try:
            time_min = datetime.now(pytz.timezone(self.tz)).replace(hour=0, minute=0, second=0, microsecond=0)
            time_max = time_min + timedelta(hours=23, minutes=59, seconds=59)

            print(f"Getting events between {time_min} and {time_max}")
            events_result = self.service.events().list(calendarId='primary', timeMin=time_min.isoformat(),
                                                  timeMax=time_max.isoformat(), singleEvents=True, timeZone=self.tz,
                                                  orderBy='startTime').execute()
            events = events_result.get('items', [])

            if not events:
                print('No upcoming events found.')
            else:
                print(f"Found {len(events)} events !")

            return list(map(lambda event: Course.from_calendar_event(event), events))

        except HttpError as error:
            print('An error occurred: %s' % error)
            return []

    def get_next_event(self):
        """Return the next incoming event"""
        try:
            now = datetime.now(pytz.timezone(self.tz)).isoformat()

            print(f"Getting next event at {now}")
            events_result = self.service.events().list(calendarId='primary', timeMin=now,
                                                  maxResults=1, singleEvents=True, timeZone=self.tz,
                                                  orderBy='startTime').execute()
            event = events_result["items"]

            if not event:
                print("No upcoming event")
                return None

            print("Found next event !")

            return Course.from_calendar_event(event[0])

        except HttpError as error:
            print('An error occurred: %s' % error)
            return None


    def get_incoming_tasks(self, period=7):
        """Return all incoming tasks in the given period (in days)"""
        pass
