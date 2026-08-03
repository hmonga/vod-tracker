"""
API Routes - FastAPI endpoints for video analysis
"""

import os
import sys
import uuid
import asyncio
from datetime import datetime
from typing import Optional
from fastapi import APIRouter, UploadFile, File, HTTPException, BackgroundTasks
from fastapi.responses import FileResponse
import logging

# Add parent directories to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

import config
from app.api import models
from app.analysis import analyzer

logger = logging.getLogger(__name__)

router = APIRouter()

# In-memory storage for active analyses (in production, use database)
active_analyses = {}


@router.post("/upload", response_model=models.VideoAnalysisResponse)
async def upload_video(file: UploadFile = File(...)):
    """
    Upload a Valorant gameplay video for analysis
    
    - **file**: Video file (MP4, MOV, WebM, AVI, MKV)
    
    Returns video_id for tracking analysis progress
    """
    try:
        # Validate file
        if file.size > config.MAX_VIDEO_SIZE:
            raise HTTPException(
                status_code=413,
                detail=f"File too large. Maximum size: {config.MAX_VIDEO_SIZE / (1024**3):.1f}GB",
            )
        
        # Check file extension
        file_ext = file.filename.split(".")[-1].lower()
        if file_ext not in config.SUPPORTED_FORMATS:
            raise HTTPException(
                status_code=400,
                detail=f"Unsupported format. Supported: {', '.join(config.SUPPORTED_FORMATS)}",
            )
        
        # Generate video ID
        video_id = str(uuid.uuid4())
        
        # Save uploaded file
        upload_path = config.UPLOAD_DIR / f"{video_id}_{file.filename}"
        with open(upload_path, "wb") as f:
            content = await file.read()
            f.write(content)
        
        logger.info(f"Video uploaded: {video_id} ({file.filename})")
        
        # Initialize analysis tracking
        active_analyses[video_id] = {
            "status": "queued",
            "filename": file.filename,
            "size": file.size,
            "upload_time": datetime.now(),
            "progress": 0,
            "current_step": "Queued for processing",
            "file_path": upload_path,
        }
        
        return models.VideoAnalysisResponse(
            video_id=video_id,
            status="success",
            message=f"Video uploaded successfully. Analysis will begin shortly.",
        )
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Upload error: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Upload failed")


@router.get("/analysis/{video_id}", response_model=models.AnalysisResult)
async def get_analysis(video_id: str):
    """
    Get analysis results for a video
    
    - **video_id**: Video ID from upload endpoint
    """
    try:
        # Get analysis from storage (mock implementation)
        analysis = await analyzer.get_analysis(video_id)
        
        if not analysis:
            raise HTTPException(status_code=404, detail="Analysis not found")
        
        return analysis
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Analysis retrieval error: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Failed to retrieve analysis")


@router.get("/analysis/{video_id}/progress", response_model=models.AnalysisProgress)
async def get_analysis_progress(video_id: str):
    """
    Get current analysis progress for a video
    
    - **video_id**: Video ID from upload endpoint
    """
    try:
        if video_id not in active_analyses:
            raise HTTPException(status_code=404, detail="Analysis not found")
        
        analysis_data = active_analyses[video_id]
        
        return models.AnalysisProgress(
            video_id=video_id,
            status=analysis_data.get("status", "unknown"),
            progress_percent=analysis_data.get("progress", 0),
            current_step=analysis_data.get("current_step", ""),
            eta_seconds=analysis_data.get("eta", None),
            error_message=analysis_data.get("error", None),
        )
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Progress retrieval error: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Failed to retrieve progress")


@router.post("/analyze/{video_id}")
async def start_analysis(video_id: str, background_tasks: BackgroundTasks):
    """
    Start analysis for an uploaded video
    
    - **video_id**: Video ID from upload endpoint
    """
    try:
        if video_id not in active_analyses:
            raise HTTPException(status_code=404, detail="Video not found")
        
        # Add analysis task to background
        background_tasks.add_task(analyzer.analyze_video, video_id, active_analyses)
        
        # Update status
        active_analyses[video_id]["status"] = "processing"
        active_analyses[video_id]["current_step"] = "Extracting frames..."
        
        logger.info(f"Analysis started for video: {video_id}")
        
        return models.VideoAnalysisResponse(
            video_id=video_id,
            status="success",
            message="Analysis started",
        )
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Analysis start error: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Failed to start analysis")


@router.get("/benchmarks", response_model=list)
async def get_benchmarks(map_name: Optional[str] = None):
    """
    Get pro player benchmark data
    
    - **map_name**: Optional filter by map name
    """
    try:
        benchmarks = await analyzer.get_benchmarks(map_name)
        return benchmarks
    
    except Exception as e:
        logger.error(f"Benchmarks retrieval error: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Failed to retrieve benchmarks")


@router.get("/stats/{video_id}", response_model=models.PlayerStats)
async def get_player_stats(video_id: str):
    """
    Get player statistics from analysis
    
    - **video_id**: Video ID from upload endpoint
    """
    try:
        stats = await analyzer.get_player_stats(video_id)
        
        if not stats:
            raise HTTPException(status_code=404, detail="Stats not found")
        
        return stats
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Stats retrieval error: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Failed to retrieve stats")


@router.get("/download-report/{video_id}")
async def download_report(video_id: str, format: str = "pdf"):
    """
    Download analysis report
    
    - **video_id**: Video ID from upload endpoint
    - **format**: Report format (pdf or json)
    """
    try:
        report_path = await analyzer.generate_report(video_id, format)
        
        if not report_path or not os.path.exists(report_path):
            raise HTTPException(status_code=404, detail="Report not found")
        
        return FileResponse(
            path=report_path,
            filename=f"analysis_{video_id}.{format}",
            media_type="application/pdf" if format == "pdf" else "application/json",
        )
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Report download error: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Failed to download report")


@router.get("/maps")
async def get_maps():
    """Get list of supported Valorant maps"""
    return {
        "maps": list(config.VALORANT_MAPS.keys()),
        "details": config.VALORANT_MAPS,
    }


@router.get("/agents")
async def get_agents():
    """Get list of Valorant agents and their roles"""
    return {
        "roles": config.AGENT_ROLES,
    }


@router.get("/health")
async def health():
    """Health check endpoint"""
    return models.HealthCheck(
        status="healthy",
        version="1.0.0",
        environment=config.ENV,
    )
