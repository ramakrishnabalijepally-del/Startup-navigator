from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional


class ContactCreate(BaseModel):
    name: str
    email: EmailStr
    subject: Optional[str] = None
    message: str


class ContactResponse(BaseModel):
    model_config = {"from_attributes": True}

    id: int
    name: str
    email: str
    subject: Optional[str]
    message: str
    is_read: bool
    created_at: datetime
