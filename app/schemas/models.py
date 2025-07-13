from datetime import datetime
from pydantic import BaseModel
from typing import Optional, List


class QueryLogResponse(BaseModel):
    id: int
    user_question: str
    persona: str
    ai_response: str
    created_at: datetime


class TopicFilter(BaseModel):
    grade: Optional[str] = None
    topic: Optional[str] = None


class TopicResponse(BaseModel):
    id: int
    topic: str
    grade: str
    title: str


class MetrixResponse(BaseModel):
    total_topics: int
    total_file_uploaded: int
    total_queries: int
