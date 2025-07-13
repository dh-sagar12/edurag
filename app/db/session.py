from sqlalchemy.orm import Session
from .database import get_db

def get_database_session() -> Session:
    return next(get_db())
