from enum import Enum

from pydantic import BaseModel, EmailStr, Field


# Rollen, die bei der Registrierung ausgewählt werden können
class UserRole(str, Enum):
    SENIOR = "senior"
    HELPER = "helper"


# Daten, die das Backend bei einer Registrierung erwartet
class UserCreate(BaseModel):
    first_name: str = Field(min_length=2, max_length=100)
    last_name: str = Field(min_length=2, max_length=100)
    email: EmailStr
    password: str = Field(min_length=8)
    role: UserRole

class UserLogin(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str