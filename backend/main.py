#!/usr/bin/env python3
"""
Valorant Crosshair Placement Analyzer - Backend Entry Point
"""

import os
import sys
import logging

# Add current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import config
from app.main import app

# Configure logging
logging.basicConfig(
    level=getattr(logging, config.LOG_LEVEL),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

logger = logging.getLogger(__name__)


if __name__ == "__main__":
    import uvicorn
    
    logger.info("=" * 80)
    logger.info("🎮 Valorant Crosshair Placement Analyzer")
    logger.info("=" * 80)
    logger.info(f"Environment: {config.ENV}")
    logger.info(f"Host: {config.API_HOST}")
    logger.info(f"Port: {config.API_PORT}")
    logger.info(f"Temp Directory: {config.TEMP_DIR}")
    logger.info(f"Debug Mode: {config.DEBUG}")
    logger.info("=" * 80)
    logger.info("")
    logger.info("📖 API Documentation: http://localhost:8000/docs")
    logger.info("🏥 Health Check: http://localhost:8000/health")
    logger.info("")
    logger.info("Starting server...")
    logger.info("Press Ctrl+C to stop")
    logger.info("")
    logger.info("=" * 80)
    
    try:
        uvicorn.run(
            app,
            host=config.API_HOST,
            port=config.API_PORT,
            reload=config.DEBUG,
            log_level=config.LOG_LEVEL.lower(),
        )
    except KeyboardInterrupt:
        logger.info("Server stopped by user")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Server error: {e}", exc_info=True)
        sys.exit(1)
