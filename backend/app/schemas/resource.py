from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List


class ResourceCreate(BaseModel):
    title: str
    category: str
    url: str
    description: Optional[str] = None
    resource_type: Optional[str] = "link"
    tags: Optional[List[str]] = []
    is_active: Optional[int] = 1


class ResourceUpdate(BaseModel):
    title: Optional[str] = None
    category: Optional[str] = None
    url: Optional[str] = None
    description: Optional[str] = None
    resource_type: Optional[str] = None
    tags: Optional[List[str]] = None
    is_active: Optional[int] = None


class ResourceResponse(BaseModel):
    model_config = {"from_attributes": True}

    id: int
    title: str
    category: str
    url: str
    description: Optional[str]
    resource_type: Optional[str]
    tags: Optional[List[str]]
    is_active: int
    created_at: datetime
    updated_at: Optional[datetime]
