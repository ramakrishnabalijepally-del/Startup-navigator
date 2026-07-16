from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List, Any


class SearchRequest(BaseModel):
    query: str


class SourceDoc(BaseModel):
    article_id: Optional[int] = None
    title: str
    category: str
    excerpt: Optional[str] = None


class SearchResponse(BaseModel):
    query: str
    answer: str
    sources: List[SourceDoc]
    history_id: int


class SearchHistoryResponse(BaseModel):
    model_config = {"from_attributes": True}

    id: int
    query: str
    answer: Optional[str]
    sources: Optional[Any]
    category_hint: Optional[str]
    created_at: datetime
