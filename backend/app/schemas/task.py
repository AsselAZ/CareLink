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


# Daten, die beim Erstellen einer Hilfeanfrage für bestimmte Kategorien erwartet werden     
class ShoppingDetailsCreate(BaseModel):
    shopping_list: str = Field(min_length=1)
    store: str | None = None


class AppointmentDetailsCreate(BaseModel):
    location: str = Field(min_length=2, max_length=200)
    appointment_type: str | None = None


class FurnitureDetailsCreate(BaseModel):
    weight_kg: float | None = Field(default=None, ge=0)
    floor: int | None = None
    elevator_available: bool | None = None


class CraftDetailsCreate(BaseModel):
    work_type: str = Field(min_length=2, max_length=150)
    required_tools: str | None = None
    difficulty: str | None = None

    # Daten, die beim Erstellen einer Hilfeanfrage erwartet werden
class TaskCreate(BaseModel):
    title: str = Field(min_length=3, max_length=150)
    description: str | None = None
    category: TaskCategory
    task_date: date
    start_time: time | None = None
    end_time: time | None = None

    shopping_details: ShoppingDetailsCreate | None = None
    appointment_details: AppointmentDetailsCreate | None = None
    furniture_details: FurnitureDetailsCreate | None = None
    craft_details: CraftDetailsCreate | None = None