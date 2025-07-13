from sqlalchemy import Column, Integer, String, Text, DateTime, Float, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func

Base = declarative_base()

class ContentChunk(Base):
    __tablename__ = "content_chunks"
    
    id = Column(Integer, primary_key=True, index=True)
    content_id = Column(Integer, nullable=False)
    chunk_text = Column(Text, nullable=False)
    chunk_index = Column(Integer, nullable=False)
    embedding_vector = Column(JSON, nullable=True)  # Store as JSON for backup
    created_at = Column(DateTime, default=func.now())