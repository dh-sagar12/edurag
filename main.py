import os
from pathlib import Path
from fastapi import FastAPI, HTTPException, Path as PathParam
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import logging
import sys
from app.config.settings import get_settings
from app.db import create_tables
from app.api.content import router as content_router
from app.api.ask import router as ask_router
from fastapi.staticfiles import StaticFiles

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("app.log"), logging.StreamHandler(sys.stdout)],
)

logger = logging.getLogger(__name__)
settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    logger.info("Starting AI Tutoring System...")
    try:
        create_tables()
        logger.info("Database tables created successfully")
    except Exception as e:
        logger.error(f"Error creating database tables: {e}")
        raise

    yield

    # Shutdown
    logger.info("Shutting down AI Tutoring System...")


app = FastAPI(
    title=settings.app_name,
    description="AI-powered tutoring system with RAG capabilities",
    version="1.0.0",
    lifespan=lifespan,
)


# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(content_router, prefix="/api/v1")
app.include_router(ask_router, prefix="/api/v1")

frontend_dist = Path(__file__).parent / "frontend" / "dist"

app.mount(
    "/",
    StaticFiles(directory=frontend_dist, html=True),
    name="frontend",
)

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "AI Tutoring System API",
        "version": "1.0.0",
        "status": "operational",
    }



@app.get("/health")
async def health_check():
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=settings.debug)
