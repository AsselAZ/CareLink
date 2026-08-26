from app.db.database import Base
from sqlalchemy import DateTime, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime


class Message(Base):
    __tablename__ = "messages"

    id: Mapped[int] = mapped_column(primary_key=True)

    task_id: Mapped[int] = mapped_column(
        ForeignKey("tasks.id")
    )

    sender_id: Mapped[int] = mapped_column(
        ForeignKey("users.id")
    )

    message: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )
    
    created_at: Mapped[datetime] = mapped_column(
    DateTime,
    default=datetime.now,
    )

    task = relationship("Task")
    sender = relationship("User")