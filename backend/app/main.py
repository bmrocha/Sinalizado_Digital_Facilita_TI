"""
Sistema de Sinalização Digital - Sicoob Credisete
API REST principal construída com FastAPI
"""

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
import structlog
from contextlib import asynccontextmanager

from app.core.config import settings
from app.core.database import engine
from app.models import base
from app.api.v1.api import api_router
from app.core.security import get_current_user_optional

# Configure structured logging
logger = structlog.get_logger()

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events"""
    # Startup
    logger.info("Starting Digital Signage API", version="1.0.0")

    # Create database tables
    async with engine.begin() as conn:
        await conn.run_sync(base.Base.metadata.create_all)

    yield

    # Shutdown
    logger.info("Shutting down Digital Signage API")

# Create FastAPI application
app = FastAPI(
    title="Sistema de Sinalização Digital - Sicoob Credisete",
    description="API REST para gerenciamento de sinalização digital",
    version="1.0.0",
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# Set up CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

# Include API router
app.include_router(api_router, prefix=settings.API_V1_STR)

@app.get("/")
async def root():
    """Root endpoint - redirect to docs"""
    return RedirectResponse(url="/docs")

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "Digital Signage API"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=settings.API_HOST,
        port=settings.API_PORT,
        reload=True,
        log_config=None
    )
