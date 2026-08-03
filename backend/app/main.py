"""
Valorant Crosshair Placement Analyzer - Main FastAPI Application
"""

import os
import sys
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import logging

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import config
from app.api import routes

# Configure logging
logging.basicConfig(
    level=getattr(logging, config.LOG_LEVEL),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(config.LOG_FILE),
        logging.StreamHandler(),
    ],
)

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application startup and shutdown events"""
    logger.info("🚀 Valorant Crosshair Analyzer starting up...")
    logger.info(f"Temp directory: {config.TEMP_DIR}")
    logger.info(f"API running on {config.API_HOST}:{config.API_PORT}")
    
    # Startup
    yield
    
    # Shutdown
    logger.info("💤 Application shutting down...")


# Create FastAPI app
app = FastAPI(
    title="Valorant Crosshair Placement Analyzer",
    description="AI-powered video analysis for Valorant crosshair placement coaching",
    version="1.0.0",
    lifespan=lifespan,
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=config.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "version": "1.0.0",
        "environment": config.ENV,
    }


# API routes
app.include_router(routes.router, prefix="/api", tags=["API"])


# Root endpoint
@app.get("/")
async def root():
    """Root endpoint with API info"""
    return {
        "name": "Valorant Crosshair Placement Analyzer",
        "version": "1.0.0",
        "docs": "/docs",
        "status": "running",
    }


# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Global exception handler"""
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"},
    )


if __name__ == "__main__":
    import uvicorn
    
    logger.info(f"Starting Valorant Crosshair Analyzer on {config.API_HOST}:{config.API_PORT}")
    
    uvicorn.run(
        "app.main:app",
        host=config.API_HOST,
        port=config.API_PORT,
        reload=config.DEBUG,
        log_level=config.LOG_LEVEL.lower(),
    )
