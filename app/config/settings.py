from pydantic_settings import BaseSettings
from functools import lru_cache
import os

class Settings(BaseSettings):
    # Database
    database_url: str = os.getenv("DATABASE_URL")
    
    # OpenAI
    openai_api_key: str = os.getenv("OPENAI_API_KEY")
    openai_embedding_model: str = os.getenv("OPENAI_EMBEDDING_MODEL")
    openai_chat_model: str = os.getenv("OPENAI_CHAT_MODEL")
    
    # FAISS
    faiss_index_path: str = os.getenv("FAISS_INDEX_PATH")
    
    # Application
    app_name: str = os.getenv("APP_NAME")
    debug: bool = os.getenv("DEBUG")
    
    # Chunking
    gemini_api_key: str = os.getenv("GEMINI_API_KEY")
    gemini_chat_model: str = os.getenv("GEMINI_CHAT_MODEL")
    
    class Config:
        env_file = ".env"

@lru_cache()
def get_settings():
    return Settings()



# First call – initializes and caches
s1 = get_settings()

# Second call – uses cache, does not reinitialize
s2 = get_settings()

# Clear cache
get_settings.cache_clear()

# Next call – reinitializes because cache was cleared
s3 = get_settings()
