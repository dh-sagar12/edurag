import logging
from app.models.content import Content
from app.models.query_log import QueryLog
from app.schemas.models import MetrixResponse, TopicResponse
from app.services.embedding_service import EmbeddingService
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db import get_db
from fastapi import HTTPException, File
from fastapi import UploadFile
from typing import List, Optional
from fastapi import Form

logger = logging.getLogger(__name__)
router = APIRouter(tags=["content"])


@router.post(
    "/upload-content",
    summary="Upload content",
    description="Upload content to be processed and stored in the database",
)
def upload_content(
    title: str = Form(..., description="Title of the content"),
    topic: str = Form(..., description="Topic of the content"),
    grade: str = Form(..., description="Grade of the content"),
    file: UploadFile = File(..., description="File to upload"),
    db: Session = Depends(get_db),
):
    try:
        text_content = file.file.read().decode("utf-8")

        content_instance = Content(
            title=title,
            topic=topic,
            grade=grade,
            content=text_content,
        )
        db.add(content_instance)
        db.flush()
        vector_store = EmbeddingService()
        vector_store.add(
            content_instance.id,
            text_content,
        )
        db.commit()
        return {
            "message": "Content uploaded successfully",
        }
    except Exception as e:
        db.rollback()
        logger.error(f"Error uploading content: {e}")
        raise HTTPException(
            status_code=500,
            detail="Failed to upload content",
        )


@router.get(
    "/topics",
    summary="fitler topic based on grades and title",
    description="Filter topic based on grades and title",
    response_model=List[TopicResponse,],
)
def get_topics(
    db: Session = Depends(get_db),
    grade: Optional[str] = None,
    title: Optional[str] = None,
):
    try:
        query: List[Content] = db.query(Content)
        if grade:
            print("grade available as ", grade)
            query = query.filter(Content.grade == grade)
        if title:
            print("title available as ", title)
            query = query.filter(Content.title.contains(title))
        topics = query.all()
        return [
            TopicResponse(
                id= topic.id,
                topic=topic.topic,
                grade=topic.grade,
                title=topic.title,
            )
            for topic in topics
        ]
    except Exception as e:
        logger.error(f"Error getting topics: {e}")
        raise HTTPException(
            status_code=500,
            detail="Failed to get topics",
        )

@router.get(
    "/metrix",
    summary="get metrix",
    description="Get metrix",
    response_model=MetrixResponse,
)
def get_metrix(
    db: Session = Depends(get_db),
):
    try:
        total_topics = db.query(Content.topic).distinct().count()
        total_file_uploaded = db.query(Content).count()
        total_queries = db.query(QueryLog).count()
        return {
            "total_topics": total_topics,
            "total_file_uploaded": total_file_uploaded,
            "total_queries": total_queries,
        }
    except Exception as e:
        logger.error(f"Error getting metrix: {e}")
        raise HTTPException(
            status_code=500,
            detail="Failed to get metrix",
        )