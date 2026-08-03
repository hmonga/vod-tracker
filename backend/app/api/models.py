"""
API Models - Pydantic schemas for request/response validation
"""

from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime
from enum import Enum


class ScoreStatus(str, Enum):
    """Score status enum"""
    GOOD = "good"
    WARNING = "warning"
    WEAK = "weak"


# Request Models
class VideoUploadRequest(BaseModel):
    """Video upload request"""
    filename: str
    size: int
    duration_seconds: Optional[int] = None


class VideoMetadata(BaseModel):
    """Video metadata"""
    filename: str
    size: int
    duration: int
    fps: int
    resolution: str
    codec: str


# Response Models
class PlacementScore(BaseModel):
    """Placement score for a specific area"""
    location: str
    score: float = Field(..., ge=1, le=10)
    status: ScoreStatus
    description: str
    recommendation: Optional[str] = None


class CategoryScore(BaseModel):
    """Score for a specific category"""
    name: str
    score: float = Field(..., ge=1, le=10)
    description: str
    weight: float


class WeakArea(BaseModel):
    """Weak area identification"""
    location: str
    score: float
    your_average: float
    gap: float
    severity: str
    common_mistakes: List[str]
    specific_advice: str
    frames_analyzed: int


class ProComparison(BaseModel):
    """Comparison with pro player benchmarks"""
    location: str
    your_score: float
    pro_average: float
    percentile: str
    key_difference: str
    improvement_potential: float


class ImprovementPlan(BaseModel):
    """Improvement plan entry"""
    week: int
    focus: str
    action: str
    expected_improvement: str


class AnalysisResult(BaseModel):
    """Complete analysis result"""
    video_id: str
    filename: str
    upload_time: datetime
    analysis_time: datetime
    duration_minutes: float
    
    # Scores
    overall_score: float = Field(..., ge=1, le=10)
    category_scores: List[CategoryScore]
    
    # Analysis
    weak_areas: List[WeakArea]
    pro_comparisons: List[ProComparison]
    
    # Plan
    improvement_plan: List[ImprovementPlan]
    
    # Summary
    summary: str
    strong_points: List[str]
    areas_to_improve: List[str]


class AnalysisProgress(BaseModel):
    """Analysis progress tracking"""
    video_id: str
    status: str  # "uploading", "processing", "analyzing", "complete", "error"
    progress_percent: int = Field(..., ge=0, le=100)
    current_step: str
    eta_seconds: Optional[int] = None
    error_message: Optional[str] = None


class VideoAnalysisResponse(BaseModel):
    """Response for video analysis endpoint"""
    video_id: str
    status: str
    message: str


class BenchmarkData(BaseModel):
    """Pro player benchmark data"""
    map_name: str
    location: str
    pro_average_score: float
    by_agent: Dict[str, float]
    common_mistakes: List[str]


class HealthCheck(BaseModel):
    """Health check response"""
    status: str
    version: str
    environment: str


class ErrorResponse(BaseModel):
    """Error response"""
    detail: str
    error_code: Optional[str] = None
    timestamp: datetime = Field(default_factory=datetime.now)


# Statistics Models
class PlayerStats(BaseModel):
    """Player statistics"""
    total_videos_analyzed: int
    total_playtime_minutes: int
    average_overall_score: float
    strongest_location: str
    weakest_location: str
    improvement_percentage: float
    last_analysis_date: Optional[datetime] = None


class MapStats(BaseModel):
    """Map-specific statistics"""
    map_name: str
    times_analyzed: int
    average_score: float
    locations: Dict[str, float]
    trend: str  # "improving", "declining", "stable"
