from datetime import datetime
from dataclasses import dataclass
from typing import TypeVar, Type

T = TypeVar('T')

@dataclass
class Task:
    """Class representing a task"""
    title: str
    description: str
    due_date: str

    @classmethod
    def from_tasks_api(cls: Type['T'], task) -> T:
        due_date = datetime.strptime(task["due"], "%Y-%m-%dT%H:%M:%S.%fZ").strftime("%d/%m/%Y")
        description = task.get("notes", "Pas de description")
        title = task.get("title", "Pas de titre")

        return cls(title=title, description=description, due_date=due_date)

    def __str__(self):
        return f"Titre : {self.title}\nDescription: {self.description}\nEchéance: {self.due_date}\n"
