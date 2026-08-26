from pydantic import BaseModel, Field


class MessageCreate(BaseModel):
    message: str = Field(min_length=1)