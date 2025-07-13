
from sqlalchemy import Column, Integer, String, Text, DateTime, Float, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func

Base = declarative_base()
class QueryLog(Base):
    __tablename__ = "query_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    user_question = Column(Text, nullable=False)
    ai_response = Column(Text, nullable=False)
    persona = Column(String(50), default="friendly")
    created_at = Column(DateTime, default=func.now())
