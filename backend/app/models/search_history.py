from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base


class SearchHistory(Base):
    __tablename__ = "search_history"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    query = Column(Text, nullable=False)
    answer = Column(Text, nullable=True)
    sources = Column(JSON, nullable=True)  # list of {article_id, title, category}
    category_hint = Column(String(100), nullable=True)  # most relevant category from RAG
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", back_populates="search_history")
