from .service import CalendarService, TasksService


class Calendar:
    """Utility class linking different service to create a calendar"""

    def __init__(self, timezone: str):
        self.calendar_service = CalendarService(timezone=timezone)
        self.tasks_service = TasksService(timezone=timezone)

    def build(self, credentials) -> None:
        """Build all the required services"""
        self.calendar_service.build(credentials)
        self.tasks_service.build(credentials)

    def get_today_classes(self) -> str:
        """Return all events occuring today"""
        try:
            classes = self.calendar_service.get_today_classes()

            if not classes:
                text = "Pas de cours aujourd'hui"
            else:
                text = "Les cours sont :\n\n" + "\n".join(map(str, classes))

            return text
        except AttributeError:
            return "Merci de vous connecter à google: /connect"

    def get_next_class(self) -> str:
        """Return the next incoming event"""
        try:
            course = self.calendar_service.get_next_class()

            if not course:
                text = "Pas de prochain cours"
            else:
                text = "Le prochain cours est :\n\n" + str(course)

            return text
        except AttributeError:
            return "Merci de vous connecter à google: /connect"

    def get_incoming_tasks(self, period: int) -> str:
        """Return all incoming tasks in the given period (in days)"""
        try:
            tasks = self.tasks_service.get_incoming_tasks(period)

            if not tasks:
                text = "Pas de tâches à venir"
            else:
                text = ("Les tâches à venir sont :\n\n"
                        + "\n".join(map(str, tasks)))

            return text
        except AttributeError:
            return "Merci de vous connecter à google: /connect"
