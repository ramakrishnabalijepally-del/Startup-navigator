from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List


class ArticleCreate(BaseModel):
    title: str
    category: str
    content: str
    summary: Optional[str] = None
    tags: Optional[List[str]] = []
    author: Optional[str] = "Startup Navigator Team"
    is_published: Optional[int] = 1


class ArticleUpdate(BaseModel):
    title: Optional[str] = None
    category: Optional[str] = None
    content: Optional[str] = None
    summary: Optional[str] = None
    tags: Optional[List[str]] = None
    author: Optional[str] = None
    is_published: Optional[int] = None


class ArticleResponse(BaseModel):
    model_config = {"from_attributes": True}

    id: int
    title: str
    category: str
    content: str
    summary: Optional[str]
    tags: Optional[List[str]]
    author: Optional[str]
    is_published: int
    created_at: datetime
    updated_at: Optional[datetime]


class ArticleListResponse(BaseModel):
    model_config = {"from_attributes": True}

    id: int
    title: str
    category: str
    summary: Optional[str]
    tags: Optional[List[str]]
    author: Optional[str]
    created_at: datetime
