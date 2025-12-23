from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import logging
from . import rag_routes, textbook_routes
from ..utils.config import config
from ..utils.database import init_db, close_db
from ..utils.logging import setup_logging

# Set up logging
setup_logging()
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    FastAPI lifespan event handler
    """
    logger.info("Starting up the application...")

    # Initialize database tables asynchronously
    await init_db()
    logger.info("Database initialized")

    yield  # Application runs here

    # Cleanup on shutdown
    await close_db()
    logger.info("Application shutdown complete")

# Create FastAPI app with lifespan
app = FastAPI(
    title="Textbook RAG API",
    description="API for the AI-Native Textbook with RAG functionality",
    version="1.0.0",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, restrict to your frontend origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(textbook_routes.router, prefix=config.API_V1_STR)
app.include_router(rag_routes.router, prefix=config.API_V1_STR)

# Root endpoint
@app.get("/")
async def root():
    return {
        "message": "Welcome to the Textbook RAG API",
        "version": "1.0.0",
        "status": "running"
    }

# Health check endpoint
@app.get("/health")
async def health_check():
    from datetime import datetime
    return {
        "status": "healthy",
        "message": "API is running normally",
        "timestamp": datetime.utcnow().isoformat()
    }

# Exception handler for 500 errors
@app.exception_handler(500)
async def internal_exception_handler(request: Request, exc: Exception):
    logger.error(f"Internal server error: {exc}")
    return {
        "error": "Internal server error occurred",
        "status_code": 500
    }

# Run with uvicorn if executed directly
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "src.api.main:app",
        host="0.0.0.0",
        port=8000,
        reload=config.DEBUG
    )
