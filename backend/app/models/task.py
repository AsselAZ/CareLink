from enum import Enum
from datetime import date, time

from sqlalchemy import Date, ForeignKey, String, Text, Time
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.database import Base


# Kategorien für Hilfeanfragen
class TaskCategory(str, Enum):
    SHOPPING = "shopping"
    CRAFT = "craft"
    FURNITURE = "furniture"
    APPOINTMENT = "appointment"
    WALK = "walk"
    TIME = "time"


# Status einer Hilfeanfrage
class TaskStatus(str, Enum):
    OPEN = "open"
    ACCEPTED = "accepted"
    DONE = "done"


# Eine Hilfeanfrage erstellen
class Task(Base):
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(primary_key=True)

    title: Mapped[str] = mapped_column(String(150))
    description: Mapped[str | None] = mapped_column(Text, nullable=True)

    category: Mapped[str] = mapped_column(String(30))
    status: Mapped[str] = mapped_column(
        String(20),
        default=TaskStatus.OPEN.value,
    )

    task_date: Mapped[date] = mapped_column(Date)
    start_time: Mapped[time | None] = mapped_column(Time, nullable=True)
    end_time: Mapped[time | None] = mapped_column(Time, nullable=True)

    senior_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
    )

    helper_id: Mapped[int | None] = mapped_column(
        ForeignKey("users.id"),
        nullable=True,
    )

    senior = relationship(
        "User",
        foreign_keys=[senior_id],
    )

    helper = relationship(
        "User",
        foreign_keys=[helper_id],
    )