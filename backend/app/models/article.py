from sqlalchemy import Column, Integer, String, Text, DateTime, JSON
from sqlalchemy.sql import func
from app.database import Base


class Article(Base):
    __tablename__ = "articles"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(500), nullable=False, index=True)
    category = Column(String(100), nullable=False, index=True)
    content = Column(Text, nullable=False)
    summary = Column(String(1000), nullable=True)
    tags = Column(JSON, nullable=True, default=[])
    author = Column(String(255), nullable=True, default="Startup Navigator Team")
    is_published = Column(Integer, default=1)  # 1=published, 0=draft
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
