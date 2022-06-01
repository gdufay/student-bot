from typing import Dict, List
from datetime import datetime, timedelta
import pytz

from googleapiclient.errors import HttpError
from googleapiclient.discovery import build

from utils.course import Course
from utils.task import Task


class GoogleService:
    """An abstract class wrapping a google service"""

    API_SERVICE_NAME: str
    API_VERSION: str
    SCOPES: List[str]

    def __init__(self, timezone: str) -> None:
        self.service = None
        self.timezone = timezone

    def build(self, credentials: Dict) -> None:
        try:
            self.service = build(self.API_SERVICE_NAME,
                                 self.API_VERSION, credentials=credentials)
        except HttpError as error:
            print('An error occurred: %s' % error)


class CalendarService(GoogleService):
    API_SERVICE_NAME: str = "calendar"
    API_VERSION: str = "v3"
    SCOPES: List[str] = ["https://www.googleapis.com/auth/calendar.readonly"]

    def __init__(self, timezone: str) -> None:
        super().__init__(timezone)

    def get_today_classes(self) -> List[Course]:
        """Return all events occuring today"""
        try:
            time_min = datetime.now(pytz.timezone(self.timezone)).replace(
                hour=0, minute=0, second=0, microsecond=0)
            time_max = time_min + timedelta(hours=23, minutes=59, seconds=59)

            print(f"Getting events between {time_min} and {time_max}")
            events_result = self.service.events().list(
                calendarId='primary', timeMin=time_min.isoformat(),
                timeMax=time_max.isoformat(), singleEvents=True,
                timeZone=self.timezone, orderBy='startTime'
            ).execute()
            events = events_result.get('items', [])

            if not events:
                print('No upcoming events found.')
            else:
                print(f"Found {len(events)} events !")

            return list(map(Course.from_calendar_event, events))

        except HttpError as error:
            print('An error occurred: %s' % error)
            return []

    def get_next_class(self) -> Course:
        """Return the next incoming event"""
        try:
            now = datetime.now(pytz.timezone(self.timezone)).isoformat()

            print(f"Getting next event at {now}")
            events_result = self.service.events().list(
                calendarId='primary', timeMin=now, maxResults=1,
                singleEvents=True, timeZone=self.timezone, orderBy='startTime'
            ).execute()
            event = events_result["items"]

            if not event:
                print("No upcoming event")
                return None

            print("Found next event !")

            return Course.from_calendar_event(event[0])

        except HttpError as error:
            print('An error occurred: %s' % error)
            return None


class TasksService(GoogleService):
    API_SERVICE_NAME: str = "tasks"
    API_VERSION: str = "v1"
    SCOPES: List[str] = ["https://www.googleapis.com/auth/tasks.readonly"]

    def __init__(self, timezone: str) -> None:
        super().__init__(timezone)

    def get_incoming_tasks(self, period: int = 7) -> List[Task]:
        """Return all incoming tasks in the given period (in days)"""
        try:
            time_min = datetime.now(pytz.timezone(pytz.utc.zone)).replace(
                hour=0, minute=0, second=0, microsecond=0)
            time_max = time_min + timedelta(days=period)

            print("Getting tasks lists")
            tasklists_result = self.service.tasklists().list().execute()
            tasklists = tasklists_result.get("items", [])

            if not tasklists:
                print("No upcoming tasks")
                return []

            print(f"Found {len(tasklists)} tasklists !")
            print(f"Searching between {time_min} and {time_max}")
            ret = []
            for tasklist in tasklists:
                tasks_result = self.tasks_service.tasks().list(
                    tasklist=tasklist["id"], dueMin=time_min.isoformat(),
                    dueMax=time_max.isoformat()
                ).execute()
                tasks = tasks_result.get("items", [])

                ret += [Task.from_tasks_api(task) for task in tasks]

            return ret

        except HttpError as error:
            print('An error occurred: %s' % error)
            return []
