from app.models.query_log import QueryLog
from app.schemas.models import QueryLogResponse
from app.services.embedding_service import EmbeddingService
from app.models.content import Content
from app.db import get_db
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.services.gemini_service import GeminiService
import logging
from typing import List, Optional
from fastapi import HTTPException

logger = logging.getLogger(__name__)
router = APIRouter(tags=["ask"])


@router.post("/ask")
async def ask_question(
    question: str,
    persona: str = "friendly",
    nl_sql: bool = False,
    context_id: Optional[int] = None,
    db: Session = Depends(get_db),
):
    gemini_service = GeminiService()
    if nl_sql:
        response  = gemini_service.process_nl_query(
            nl_question=question,
            persona=persona,
            db=db,
        )
        return response
    else:
        response = gemini_service.generate_context_based_response(
            question=question,
            persona=persona,
            db=db,
            context_id=context_id,
        )
        return response

@router.get(
    "/query-log",
    response_model=List[QueryLogResponse],
)
async def get_query_log(
    db: Session = Depends(get_db),
):
    try:
        query_logs = (
            db.query(QueryLog)
            .order_by(
                QueryLog.created_at,
            )
            .all()
        )
        return [QueryLogResponse(**query_log.__dict__) for query_log in query_logs]
    except Exception as e:
        logger.error(f"Error getting query log: {e}")
        raise HTTPException(
            status_code=500,
            detail="Failed to get query log",
        )



