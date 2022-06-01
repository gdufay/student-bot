from .service import CalendarService, TasksService


class Calendar:
    """Utility class linking different service to create a calendar"""

    def __init__(self):
        self.calendar_service = CalendarService()
        self.tasks_service = TasksService()

    def connect(self) -> None:
        """Connect to calendar server"""
        # The file token.json stores the user's access and refresh tokens,
        # and is created automatically when the authorization flow completes
        # for the first time.
        # if os.path.exists(self.token_path):
        #     self.creds = Credentials.from_authorized_user_file(
        #         self.token_path, Calendar.SCOPES
        #     )
        # # If there are no (valid) credentials available, let the user log in.
        # if not self.creds or not self.creds.valid:
        #     if self.creds and self.creds.expired and self.creds.refresh_token:
        #         self.creds.refresh(Request())
        #     else:
        #         flow = InstalledAppFlow.from_client_secrets_file(
        #             self.credentials_path, Calendar.SCOPES
        #         )
        #         self.creds = flow.run_local_server(port=self.port)
        #     # Save the credentials for the next run
        #     with open(self.token_path, 'w') as token:
        #         token.write(self.creds.to_json())
        pass

    def build(self, credentials) -> None:
        """Build all the required services"""
        # scopes = [*CalendarService.SCOPES, *TasksService.SCOPES]

        self.calendar_service.build(credentials)
        self.tasks_service.build(credentials)

    def get_today_classes(self) -> str:
        """Return all events occuring today"""
        classes = self.calendar_service.get_today_classes()

        if not classes:
            text = "Pas de cours aujourd'hui"
        else:
            text = "Les cours sont :\n\n" + "\n".join(map(str, classes))

        return text

    def get_next_class(self) -> str:
        """Return the next incoming event"""
        course = self.calendar_service.get_next_class()

        if not course:
            text = "Pas de prochain cours"
        else:
            text = "Le prochain cours est :\n\n" + str(course)

        return text

    def get_incoming_tasks(self, period: int) -> str:
        """Return all incoming tasks in the given period (in days)"""
        tasks = self.tasks_service.get_incoming_tasks(period)

        if not tasks:
            text = "Pas de tâches à venir"
        else:
            text = "Les tâches à venir sont :\n\n" + "\n".join(map(str, tasks))

        return text
