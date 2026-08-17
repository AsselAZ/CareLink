from sqlalchemy import Boolean, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.database import Base


# Zusätzliche Angaben für Einkaufsanfragen
class ShoppingDetails(Base):
    __tablename__ = "shopping_details"

    id: Mapped[int] = mapped_column(primary_key=True)

    task_id: Mapped[int] = mapped_column(
        ForeignKey("tasks.id"),
        unique=True,
    )

    shopping_list: Mapped[str] = mapped_column(Text)
    store: Mapped[str | None] = mapped_column(String(120), nullable=True)

    task = relationship("Task")


# Zusätzliche Angaben für Terminbegleitungen
class AppointmentDetails(Base):
    __tablename__ = "appointment_details"

    id: Mapped[int] = mapped_column(primary_key=True)

    task_id: Mapped[int] = mapped_column(
        ForeignKey("tasks.id"),
        unique=True,
    )

    location: Mapped[str] = mapped_column(String(200))
    appointment_type: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    task = relationship("Task")


# Zusätzliche Angaben für Möbelhilfe
class FurnitureDetails(Base):
    __tablename__ = "furniture_details"

    id: Mapped[int] = mapped_column(primary_key=True)

    task_id: Mapped[int] = mapped_column(
        ForeignKey("tasks.id"),
        unique=True,
    )

    weight_kg: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
    )

    floor: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
    )

    elevator_available: Mapped[bool | None] = mapped_column(
        Boolean,
        nullable=True,
    )

    task = relationship("Task")


# Zusätzliche Angaben für handwerkliche Hilfe
class CraftDetails(Base):
    __tablename__ = "craft_details"

    id: Mapped[int] = mapped_column(primary_key=True)

    task_id: Mapped[int] = mapped_column(
        ForeignKey("tasks.id"),
        unique=True,
    )

    work_type: Mapped[str] = mapped_column(String(150))

    required_tools: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    difficulty: Mapped[str | None] = mapped_column(
        String(30),
        nullable=True,
    )

    task = relationship("Task")