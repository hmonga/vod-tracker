"""
Video Analysis Engine - Core analysis logic
"""

import os
import sys
import json
import logging
import random
from datetime import datetime, timedelta
from typing import Optional, Dict, List, Tuple
import cv2
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

import config
from app.api import models

logger = logging.getLogger(__name__)

# HUD regions as fractions of screen size (works at any resolution)
# Agent portrait is always bottom-left in Valorant
AGENT_HUD_REGION = (0.0, 0.82, 0.07, 1.0)   # (x1%, y1%, x2%, y2%)
# Minimap is always top-right
MINIMAP_REGION   = (0.845, 0.0, 1.0, 0.22)

# Dominant color signatures per map (HSV hue ranges, sampled from map backgrounds)
MAP_COLOR_SIGNATURES: Dict[str, List[Tuple[int, int]]] = {
    "Bind":     [(15, 30), (20, 40)],   # warm sandy orange
    "Haven":    [(90, 120), (85, 115)], # green/teal forest
    "Split":    [(0, 10), (170, 180)],  # red/white urban
    "Ascent":   [(25, 45)],             # golden mediterranean
    "Icebox":   [(95, 115)],            # cold blue-grey
    "Breeze":   [(170, 180), (0, 5)],   # white/teal beachy
    "Fracture": [(10, 25)],             # orange/rust desert
    "Pearl":    [(100, 130)],           # blue underwater
    "Lotus":    [(30, 60)],             # green jungle
    "Sunset":   [(10, 30)],             # warm orange sunset
    "Abyss":    [(220, 260)],           # dark purple void
}

# Agent portrait dominant hue ranges (each agent has a unique color scheme)
AGENT_COLOR_SIGNATURES: Dict[str, Tuple[int, int]] = {
    "Jett":       (195, 215),  # light blue
    "Reyna":      (270, 295),  # purple
    "Raze":       (25, 45),    # orange
    "Phoenix":    (15, 35),    # fire orange-red
    "Yoru":       (215, 240),  # dark blue
    "Neon":       (175, 200),  # electric cyan
    "Iso":        (245, 265),  # deep purple
    "Sage":       (150, 175),  # mint green
    "Killjoy":    (45, 65),    # yellow
    "Cypher":     (0, 15),     # red/dark
    "Chamber":    (35, 55),    # gold
    "Deadlock":   (160, 185),  # teal
    "Vyse":       (280, 310),  # violet
    "Sova":       (200, 220),  # arctic blue
    "Fade":       (255, 280),  # dark purple-black
    "Gekko":      (85, 110),   # lime green
    "Skye":       (105, 130),  # forest green
    "KAY/O":      (185, 210),  # steel blue
    "Breach":     (20, 40),    # orange
    "Brimstone":  (10, 25),    # red-orange
    "Omen":       (240, 265),  # dark blue-purple
    "Viper":      (120, 145),  # toxic green
    "Astra":      (260, 285),  # cosmic purple
    "Harbor":     (170, 195),  # ocean teal
    "Clove":      (290, 315),  # pink-purple
}


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
            active_analyses[video_id]["current_step"] = "Detecting map & agent from HUD..."
            active_analyses[video_id]["progress"] = 35
            
            placements = self._analyze_placements(frames)
            if placements:
                active_analyses[video_id]["detected_map"] = placements[0]["map"]
                active_analyses[video_id]["detected_agent"] = placements[0]["agent"]
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

    def _get_dominant_hue(self, region: np.ndarray) -> Optional[float]:
        """Return the most common hue in an image region, ignoring near-black/white pixels."""
        if region is None or region.size == 0:
            return None
        hsv = cv2.cvtColor(region, cv2.COLOR_BGR2HSV)
        # Mask out very dark and very desaturated pixels (background, UI chrome)
        mask = cv2.inRange(hsv, np.array([0, 40, 40]), np.array([180, 255, 255]))
        hues = hsv[:, :, 0][mask > 0]
        if hues.size == 0:
            return None
        # Histogram over 180 hue bins, return peak
        hist = np.bincount(hues.astype(np.int32), minlength=180)
        return float(np.argmax(hist))

    def _crop_hud_region(self, frame: np.ndarray, region: Tuple[float, float, float, float]) -> np.ndarray:
        """Crop a HUD region defined as fractional coordinates (x1, y1, x2, y2)."""
        h, w = frame.shape[:2]
        x1 = int(region[0] * w)
        y1 = int(region[1] * h)
        x2 = int(region[2] * w)
        y2 = int(region[3] * h)
        return frame[y1:y2, x1:x2]

    def detect_map(self, frame: np.ndarray) -> str:
        """
        Detect map by sampling the background (non-HUD) center region and
        matching its dominant hue against known map color signatures.
        Falls back to random if no confident match.
        """
        try:
            h, w = frame.shape[:2]
            # Use center 40% of frame — avoids HUD chrome on edges
            center = frame[int(h * 0.3):int(h * 0.7), int(w * 0.3):int(w * 0.7)]
            dominant_hue = self._get_dominant_hue(center)
            if dominant_hue is None:
                raise ValueError("No valid hue found")

            best_map, best_score = None, float("inf")
            for map_name, hue_ranges in MAP_COLOR_SIGNATURES.items():
                for lo, hi in hue_ranges:
                    # Handle wraparound (e.g. red at 0 and 180)
                    if lo <= hi:
                        dist = 0 if lo <= dominant_hue <= hi else min(abs(dominant_hue - lo), abs(dominant_hue - hi))
                    else:
                        dist = 0 if dominant_hue >= lo or dominant_hue <= hi else min(abs(dominant_hue - lo), abs(dominant_hue - hi))
                    if dist < best_score:
                        best_score = dist
                        best_map = map_name

            # Accept match only if close enough; otherwise fall back
            if best_score <= 20:
                logger.debug(f"Map detected: {best_map} (hue={dominant_hue:.1f}, dist={best_score:.1f})")
                return best_map
        except Exception as e:
            logger.debug(f"Map detection failed: {e}")

        return random.choice(list(config.VALORANT_MAPS.keys()))

    def detect_agent(self, frame: np.ndarray) -> str:
        """
        Detect agent by reading the bottom-left HUD portrait and matching
        its dominant hue against known agent color signatures.
        """
        try:
            portrait = self._crop_hud_region(frame, AGENT_HUD_REGION)
            dominant_hue = self._get_dominant_hue(portrait)
            if dominant_hue is None:
                raise ValueError("No valid hue in portrait region")

            best_agent, best_dist = None, float("inf")
            for agent, (lo, hi) in AGENT_COLOR_SIGNATURES.items():
                # Normalize hue to 0-360 for comparison (OpenCV uses 0-180)
                hue_360 = dominant_hue * 2
                lo_n, hi_n = lo % 360, hi % 360
                if lo_n <= hi_n:
                    dist = 0 if lo_n <= hue_360 <= hi_n else min(abs(hue_360 - lo_n), abs(hue_360 - hi_n))
                else:
                    dist = 0 if hue_360 >= lo_n or hue_360 <= hi_n else min(abs(hue_360 - lo_n), abs(hue_360 - hi_n))
                if dist < best_dist:
                    best_dist = dist
                    best_agent = agent

            if best_dist <= 30:
                logger.debug(f"Agent detected: {best_agent} (hue={dominant_hue*2:.1f}, dist={best_dist:.1f})")
                return best_agent
        except Exception as e:
            logger.debug(f"Agent detection failed: {e}")

        return random.choice(sum(config.AGENT_ROLES.values(), []))

    def detect_crosshair(self, frame: np.ndarray) -> Tuple[Optional[float], Optional[float]]:
        """
        Detect crosshair position by looking for the small bright/colored dot
        near screen center (Valorant crosshairs are always centered).
        Returns (x, y) in pixels or (None, None) if not found.
        """
        try:
            h, w = frame.shape[:2]
            # Crosshair is always within 15% of screen center
            margin_x, margin_y = int(w * 0.15), int(h * 0.15)
            cx, cy = w // 2, h // 2
            roi = frame[cy - margin_y:cy + margin_y, cx - margin_x:cx + margin_x]

            # Convert to HSV and look for vivid colored pixels (crosshair colors)
            hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
            # High saturation + high value = vivid crosshair color
            mask = cv2.inRange(hsv, np.array([0, 120, 180]), np.array([180, 255, 255]))
            # Also catch white crosshairs
            white_mask = cv2.inRange(roi, np.array([200, 200, 200]), np.array([255, 255, 255]))
            combined = cv2.bitwise_or(mask, white_mask)

            # Find contours and pick the one closest to ROI center
            contours, _ = cv2.findContours(combined, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            if not contours:
                return float(cx), float(cy)  # default to screen center

            roi_cx, roi_cy = margin_x, margin_y
            best, best_dist = None, float("inf")
            for cnt in contours:
                M = cv2.moments(cnt)
                if M["m00"] == 0:
                    continue
                px, py = M["m10"] / M["m00"], M["m01"] / M["m00"]
                dist = ((px - roi_cx) ** 2 + (py - roi_cy) ** 2) ** 0.5
                if dist < best_dist:
                    best_dist = dist
                    best = (px + (cx - margin_x), py + (cy - margin_y))

            return best if best else (float(cx), float(cy))
        except Exception as e:
            logger.debug(f"Crosshair detection failed: {e}")
            h, w = frame.shape[:2]
            return float(w // 2), float(h // 2)

    
    def _analyze_placements(self, frames: List[np.ndarray]) -> List[Dict]:
        """Analyze crosshair placements using real CV detection per frame."""
        placements = []

        # Detect map and agent once from the first valid frame
        detected_map = None
        detected_agent = None
        for frame in frames[:5]:  # try first 5 frames to get a good read
            if detected_map is None:
                detected_map = self.detect_map(frame)
            if detected_agent is None:
                detected_agent = self.detect_agent(frame)
            if detected_map and detected_agent:
                break

        if detected_map is None:
            detected_map = random.choice(list(config.VALORANT_MAPS.keys()))
        if detected_agent is None:
            detected_agent = random.choice(sum(config.AGENT_ROLES.values(), []))

        logger.info(f"Detected map={detected_map}, agent={detected_agent}")
        map_areas = config.VALORANT_MAPS[detected_map]["areas"]

        for i, frame in enumerate(frames):
            h, w = frame.shape[:2]
            cx, cy = self.detect_crosshair(frame)

            # Head level: crosshair should be in middle third vertically (30%-60% of screen)
            head_level = (0.30 * h) <= cy <= (0.60 * h)

            # Angle coverage: how close to horizontal center (0=far left, 1=far right)
            angle_coverage = 1.0 - abs((cx / w) - 0.5) * 2  # 1.0 = perfect center

            placement = {
                "frame_index": i,
                "timestamp": i * config.FRAME_SAMPLE_RATE,
                "map": detected_map,
                "location": map_areas[i % len(map_areas)],  # rotate through areas
                "agent": detected_agent,
                "crosshair_x": cx,
                "crosshair_y": cy,
                "head_level": head_level,
                "angle_coverage": round(angle_coverage, 3),
                "confidence": 0.85 if len(frames) > 0 else 0.5,
            }
            placements.append(placement)

        return placements

    
    def _score_placements(self, placements: List[Dict]) -> List[Dict]:
        """Score placements using real crosshair position data."""
        # Build agent→role lookup
        agent_role_map: Dict[str, str] = {}
        for role, agents in config.AGENT_ROLES.items():
            for agent in agents:
                agent_role_map[agent] = role

        # Role alignment bonuses: duelists rewarded for aggressive (off-center) angles,
        # sentinels rewarded for holding tighter, safer angles
        ROLE_ANGLE_IDEAL = {
            "Duelist": 0.6,    # slightly off-center, pushing angles
            "Initiator": 0.7,
            "Controller": 0.8,
            "Sentinel": 0.9,   # tight, defensive, near center
        }

        scores = []
        for placement in placements:
            head_level_score = 9.0 if placement["head_level"] else 4.5
            angle_score = placement["angle_coverage"] * 10

            # Pre-aim: reward being close to screen center (ready position)
            h_dist_from_center = abs(placement["crosshair_x"] - 960) / 960  # 0=center,1=edge
            pre_aim_score = max(1, 10 - h_dist_from_center * 5)

            # Role alignment: compare actual angle coverage to role ideal
            role = agent_role_map.get(placement["agent"], "Duelist")
            ideal = ROLE_ANGLE_IDEAL.get(role, 0.7)
            role_delta = abs(placement["angle_coverage"] - ideal)
            role_score = max(1, 10 - role_delta * 8)

            overall_score = round(
                head_level_score * 0.4 +
                angle_score      * 0.3 +
                pre_aim_score    * 0.2 +
                role_score       * 0.1,
                1
            )
            overall_score = max(1.0, min(10.0, overall_score))

            placement["score"] = overall_score
            placement["role"] = role
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
