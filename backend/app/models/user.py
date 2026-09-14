from enum import Enum

from sqlalchemy import Boolean, String, Date
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.database import Base


# Rollen, die ein Nutzer in CareLink haben kann
class UserRole(str, Enum):
    SENIOR = "senior"
    HELPER = "helper"


# Datenbankmodell für einen CareLink Nutzer
class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)

    first_name: Mapped[str] = mapped_column(String(100))
    last_name: Mapped[str] = mapped_column(String(100))
    birth_date: Mapped[Date] = mapped_column(Date)

    email: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        index=True,
    )

    password_hash: Mapped[str] = mapped_column(String(255))

    role: Mapped[str] = mapped_column(String(20))

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
    )
    address = relationship(
    "Address",
    back_populates="user",
    uselist=False,
)