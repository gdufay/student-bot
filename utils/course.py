from datetime import datetime
from dataclasses import dataclass
from typing import TypeVar, Type

T = TypeVar('T')


@dataclass
class Course:
    """Class representing a course"""
    name: str
    location: str
    start_time: str

    @classmethod
    def from_calendar_event(cls: Type['T'], event) -> T:
        start = datetime.fromisoformat(
            event['start'].get('dateTime', event['start'].get('date'))
        ).strftime("%H:%M")
        location = event.get("location", "Pas de salle")
        name = event.get("summary", "Pas de titre")

        return cls(name=name, location=location, start_time=start)

    def __str__(self):
        return (f"Cours : {self.name}\n"
                f"Salle: {self.location}\n"
                f"Heure: {self.start_time}\n")
