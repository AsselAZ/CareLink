from datetime import date, time
from enum import Enum

from pydantic import BaseModel, Field


# Kategorien, die ein Senior auswählen kann
class TaskCategory(str, Enum):
    SHOPPING = "shopping"
    CRAFT = "craft"
    FURNITURE = "furniture"
    APPOINTMENT = "appointment"
    WALK = "walk"
    TIME = "time"


# Daten, die beim Erstellen einer Hilfeanfrage erwartet werden
class TaskCreate(BaseModel):
    title: str = Field(min_length=3, max_length=150)
    description: str | None = None
    category: TaskCategory
    task_date: date
    start_time: time | None = None
    end_time: time | None = None