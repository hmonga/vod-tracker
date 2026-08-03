"""
Video Analysis Engine - Core analysis logic
"""

import os
import sys
import json
import logging
import random
from datetime import datetime, timedelta
from typing import Optional, Dict, List
import cv2
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

import config
from app.api import models

logger = logging.getLogger(__name__)


class VideoAnalyzer:
    """Main video analyzer class"""
    
    def __init__(self):
        self.analysis_cache = {}
        self.load_benchmarks()
    
    def load_benchmarks(self):
        """Load pro player benchmark data"""
        try:
            benchmark_file = config.BASE_DIR / "data" / "pro_benchmarks.json"
            if benchmark_file.exists():
                with open(benchmark_file, "r") as f:
                    self.benchmarks = json.load(f)
            else:
                logger.warning("Benchmark file not found, using defaults")
                self.benchmarks = self._generate_default_benchmarks()
        except Exception as e:
            logger.error(f"Error loading benchmarks: {e}")
            self.benchmarks = self._generate_default_benchmarks()
    
    def _generate_default_benchmarks(self) -> Dict:
        """Generate default benchmark data"""
        benchmarks = {}
        for map_name, map_data in config.VALORANT_MAPS.items():
            benchmarks[map_name] = {}
            for area in map_data["areas"]:
                benchmarks[map_name][area] = {
                    "pro_average": round(random.uniform(7.5, 9.0), 1),
                    "by_agent": {
                        role: round(random.uniform(7.0, 9.2), 1)
                        for role in config.AGENT_ROLES.keys()
                    },
                    "common_mistakes": [
                        "Crosshair too low",
                        "Not covering common entries",
                        "Overextended positioning",
                    ],
                }
        return benchmarks
    
    async def analyze_video(self, video_id: str, active_analyses: Dict):
        """
        Analyze video (main analysis pipeline)
        In production, this would contain real ML/CV logic
        """
        try:
            logger.info(f"Starting analysis for {video_id}")
            
            # Get file path
            video_data = active_analyses[video_id]
            file_path = video_data["file_path"]
            
            if not os.path.exists(file_path):
                raise FileNotFoundError(f"Video file not found: {file_path}")
            
            # Step 1: Extract video metadata
            active_analyses[video_id]["status"] = "processing"
            active_analyses[video_id]["current_step"] = "Extracting video metadata..."
            active_analyses[video_id]["progress"] = 5
            
            metadata = self._extract_metadata(file_path)
            logger.info(f"Video metadata: {metadata}")
            
            # Step 2: Extract frames
            active_analyses[video_id]["current_step"] = "Extracting frames from video..."
            active_analyses[video_id]["progress"] = 15
            
            frames = self._extract_frames(file_path, metadata)
            logger.info(f"Extracted {len(frames)} frames")
            
            # Step 3: Detect game state and crosshair
            active_analyses[video_id]["current_step"] = "Analyzing crosshair placement..."
            active_analyses[video_id]["progress"] = 40
            
            placements = self._analyze_placements(frames)
            logger.info(f"Analyzed {len(placements)} placements")
            
            # Step 4: Score placements
            active_analyses[video_id]["current_step"] = "Scoring placement quality..."
            active_analyses[video_id]["progress"] = 60
            
            scores = self._score_placements(placements)
            
            # Step 5: Identify weak areas
            active_analyses[video_id]["current_step"] = "Identifying weak areas..."
            active_analyses[video_id]["progress"] = 75
            
            weak_areas = self._identify_weak_areas(scores)
            
            # Step 6: Generate report
            active_analyses[video_id]["current_step"] = "Generating report..."
            active_analyses[video_id]["progress"] = 90
            
            analysis_result = self._generate_analysis_result(
                video_id=video_id,
                filename=video_data["filename"],
                upload_time=video_data["upload_time"],
                metadata=metadata,
                scores=scores,
                weak_areas=weak_areas,
            )
            
            # Cache result
            self.analysis_cache[video_id] = analysis_result
            
            # Update status
            active_analyses[video_id]["status"] = "complete"
            active_analyses[video_id]["progress"] = 100
            active_analyses[video_id]["current_step"] = "Analysis complete!"
            
            logger.info(f"Analysis complete for {video_id}")
            
        except Exception as e:
            logger.error(f"Analysis error for {video_id}: {e}", exc_info=True)
            active_analyses[video_id]["status"] = "error"
            active_analyses[video_id]["error"] = str(e)
            active_analyses[video_id]["progress"] = 0
    
    def _extract_metadata(self, file_path: str) -> Dict:
        """Extract video metadata using OpenCV"""
        try:
            cap = cv2.VideoCapture(file_path)
            
            fps = cap.get(cv2.CAP_PROP_FPS)
            width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            duration = frame_count / fps if fps > 0 else 0
            
            cap.release()
            
            return {
                "fps": fps,
                "width": width,
                "height": height,
                "frame_count": frame_count,
                "duration": duration,
                "resolution": f"{width}x{height}",
                "codec": "h264",  # Placeholder
            }
        except Exception as e:
            logger.error(f"Metadata extraction error: {e}")
            return {
                "fps": 60,
                "width": 1920,
                "height": 1080,
                "frame_count": 1000,
                "duration": 16.67,
                "resolution": "1920x1080",
                "codec": "h264",
            }
    
    def _extract_frames(self, file_path: str, metadata: Dict) -> List[np.ndarray]:
        """Extract frames from video (sampled)"""
        frames = []
        try:
            cap = cv2.VideoCapture(file_path)
            frame_count = 0
            sample_rate = config.FRAME_SAMPLE_RATE
            
            while frame_count < 50:  # Limit to 50 frames for demo
                ret, frame = cap.read()
                if not ret:
                    break
                
                if frame_count % sample_rate == 0:
                    frames.append(frame)
                
                frame_count += 1
            
            cap.release()
            logger.info(f"Extracted {len(frames)} sampled frames")
            
        except Exception as e:
            logger.error(f"Frame extraction error: {e}")
        
        return frames
    
    def _analyze_placements(self, frames: List[np.ndarray]) -> List[Dict]:
        """Analyze crosshair placements (mock implementation)"""
        placements = []
        
        maps = list(config.VALORANT_MAPS.keys())
        
        for i, frame in enumerate(frames):
            # Mock placement data
            placement = {
                "frame_index": i,
                "timestamp": i * 5,  # Assuming 5 seconds per frame
                "map": random.choice(maps),
                "location": random.choice(config.VALORANT_MAPS[maps[0]]["areas"]),
                "agent": random.choice(sum(config.AGENT_ROLES.values(), [])),
                "crosshair_x": random.uniform(0, 1920),
                "crosshair_y": random.uniform(0, 1080),
                "head_level": random.choice([True, False]),
                "angle_coverage": random.uniform(0.5, 1.0),
                "confidence": random.uniform(0.7, 0.99),
            }
            placements.append(placement)
        
        return placements
    
    def _score_placements(self, placements: List[Dict]) -> List[Dict]:
        """Score placements on quality"""
        scores = []
        
        for placement in placements:
            # Calculate score based on various factors
            head_level_score = 9 if placement["head_level"] else 5
            angle_score = 10 * placement["angle_coverage"]
            
            overall_score = round(
                head_level_score * 0.4 +
                angle_score * 0.3 +
                random.uniform(6, 9) * 0.3,  # Mock pre-aim score
                1
            )
            
            # Ensure score is in valid range
            overall_score = max(1, min(10, overall_score))
            
            placement["score"] = overall_score
            scores.append(placement)
        
        return scores
    
    def _identify_weak_areas(self, scores: List[Dict]) -> List[models.WeakArea]:
        """Identify weak areas from scores"""
        weak_areas = []
        
        # Group by location
        locations = {}
        for score in scores:
            location = score["location"]
            if location not in locations:
                locations[location] = []
            locations[location].append(score["score"])
        
        # Calculate averages
        overall_avg = sum(s["score"] for s in scores) / len(scores) if scores else 5
        
        # Find weak areas
        for location, location_scores in locations.items():
            avg = sum(location_scores) / len(location_scores)
            
            if avg < overall_avg - 1.5:  # Significantly below average
                weak_area = models.WeakArea(
                    location=location,
                    score=round(avg, 1),
                    your_average=round(overall_avg, 1),
                    gap=round(overall_avg - avg, 1),
                    severity="HIGH" if avg < 4 else "MEDIUM",
                    common_mistakes=[
                        "Crosshair positioning too low",
                        "Not covering key angles",
                        "Overextended positioning",
                    ],
                    specific_advice=f"Focus on {location} placement. Practice holding head-level angles and covering common entry points.",
                    frames_analyzed=len(location_scores),
                )
                weak_areas.append(weak_area)
        
        return sorted(weak_areas, key=lambda x: x.score)[:5]  # Top 5 weak areas
    
    def _generate_analysis_result(
        self,
        video_id: str,
        filename: str,
        upload_time: datetime,
        metadata: Dict,
        scores: List[Dict],
        weak_areas: List[models.WeakArea],
    ) -> models.AnalysisResult:
        """Generate complete analysis result"""
        
        overall_score = round(
            sum(s["score"] for s in scores) / len(scores) if scores else 6.5,
            1
        )
        
        # Category scores
        category_scores = [
            models.CategoryScore(
                name="Head Level Accuracy",
                score=round(overall_score + random.uniform(-1, 1), 1),
                description="How consistently your crosshair is at enemy head height",
                weight=0.4,
            ),
            models.CategoryScore(
                name="Angle Positioning",
                score=round(overall_score + random.uniform(-1.5, 0.5), 1),
                description="How well you cover likely enemy positions",
                weight=0.3,
            ),
            models.CategoryScore(
                name="Pre-Aim Quality",
                score=round(overall_score + random.uniform(-0.5, 1), 1),
                description="How proactive vs reactive your aiming is",
                weight=0.2,
            ),
            models.CategoryScore(
                name="Role Alignment",
                score=round(overall_score + random.uniform(-0.5, 0.5), 1),
                description="How well your placement matches your agent role",
                weight=0.1,
            ),
        ]
        
        # Improvement plan
        improvement_plan = [
            models.ImprovementPlan(
                week=1,
                focus="Master Head-Level Placement",
                action="20 min daily aim training focusing on head-level positioning",
                expected_improvement="+1.2 points",
            ),
            models.ImprovementPlan(
                week=2,
                focus="Angle Coverage",
                action="Review pro VODs and practice common angle positions",
                expected_improvement="+1.0 points",
            ),
            models.ImprovementPlan(
                week=3,
                focus="Map-Specific Refinement",
                action="Dedicate time to weak areas identified in analysis",
                expected_improvement="+0.8 points",
            ),
        ]
        
        # Pro comparisons
        pro_comparisons = [
            models.ProComparison(
                location=area,
                your_score=round(random.uniform(4, 8), 1),
                pro_average=round(random.uniform(8, 9.5), 1),
                percentile="35th",
                key_difference="Your placement is too low, pros maintain head-level",
                improvement_potential=round(random.uniform(1, 2), 1),
            )
            for area in ["A Main", "B Site", "Mid"]
        ]
        
        return models.AnalysisResult(
            video_id=video_id,
            filename=filename,
            upload_time=upload_time,
            analysis_time=datetime.now(),
            duration_minutes=metadata["duration"] / 60,
            overall_score=overall_score,
            category_scores=category_scores,
            weak_areas=weak_areas,
            pro_comparisons=pro_comparisons,
            improvement_plan=improvement_plan,
            summary=f"Good fundamentals with room for improvement. Focus on {weak_areas[0].location if weak_areas else 'general placement'} placement.",
            strong_points=["Good pre-aim awareness", "Consistent angle holding"],
            areas_to_improve=[f"Improve {area.location} placement" for area in weak_areas[:2]],
        )
    
    async def get_analysis(self, video_id: str) -> Optional[models.AnalysisResult]:
        """Get cached analysis result"""
        return self.analysis_cache.get(video_id)
    
    async def get_benchmarks(self, map_name: Optional[str] = None) -> List[Dict]:
        """Get benchmark data"""
        if map_name:
            return [self.benchmarks.get(map_name, {})]
        return [self.benchmarks]
    
    async def get_player_stats(self, video_id: str) -> Optional[models.PlayerStats]:
        """Get player statistics"""
        analysis = self.analysis_cache.get(video_id)
        if not analysis:
            return None
        
        return models.PlayerStats(
            total_videos_analyzed=1,
            total_playtime_minutes=analysis.duration_minutes,
            average_overall_score=analysis.overall_score,
            strongest_location="Mid Control",
            weakest_location=analysis.weak_areas[0].location if analysis.weak_areas else "Unknown",
            improvement_percentage=random.uniform(5, 25),
            last_analysis_date=analysis.analysis_time,
        )
    
    async def generate_report(self, video_id: str, format: str = "json") -> Optional[str]:
        """Generate report (placeholder)"""
        analysis = self.analysis_cache.get(video_id)
        if not analysis:
            return None
        
        report_path = config.TEMP_DIR / f"report_{video_id}.{format}"
        
        if format == "json":
            with open(report_path, "w") as f:
                json.dump(analysis.dict(), f, indent=2, default=str)
        
        return str(report_path)


# Global analyzer instance
analyzer = VideoAnalyzer()
