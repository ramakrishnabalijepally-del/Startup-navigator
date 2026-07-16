from sqlalchemy import Column, Integer, String, Text, DateTime, JSON
from sqlalchemy.sql import func
from app.database import Base


class Resource(Base):
    __tablename__ = "resources"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(500), nullable=False, index=True)
    category = Column(String(100), nullable=False, index=True)
    url = Column(String(2000), nullable=False)
    description = Column(Text, nullable=True)
    resource_type = Column(String(50), nullable=True)  # link, pdf, tool, template
    tags = Column(JSON, nullable=True, default=[])
    is_active = Column(Integer, default=1)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
