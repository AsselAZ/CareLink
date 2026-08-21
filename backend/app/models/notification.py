from sqlalchemy import Boolean, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.database import Base


class Notification(Base):
    __tablename__ = "notifications"

    id: Mapped[int] = mapped_column(primary_key=True)

    # Welcher User bekommt die Benachrichtigung?
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id")
    )

    # Text der Benachrichtigung
    message: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    # Wurde die Benachrichtigung schon gelesen?
    is_read: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
    )