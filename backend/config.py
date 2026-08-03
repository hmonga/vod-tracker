"""
Valorant Crosshair Placement Analyzer - Configuration
"""

import os
from typing import List
from pathlib import Path

# Environment
ENV = os.getenv("ENV", "development")
DEBUG = ENV == "development"

# Directories
BASE_DIR = Path(__file__).parent.parent
TEMP_DIR = Path(os.getenv("TEMP_DIR", "/tmp/vod-tracker"))
UPLOAD_DIR = TEMP_DIR / "uploads"
PROCESSING_DIR = TEMP_DIR / "processing"
LOGS_DIR = BASE_DIR / "logs"

# Ensure directories exist
for dir_path in [TEMP_DIR, UPLOAD_DIR, PROCESSING_DIR, LOGS_DIR]:
    dir_path.mkdir(parents=True, exist_ok=True)

# Video Processing
MAX_VIDEO_SIZE = int(os.getenv("MAX_VIDEO_SIZE", 2 * 1024 * 1024 * 1024))  # 2GB
SUPPORTED_FORMATS = ["mp4", "mov", "webm", "avi", "mkv"]
FRAME_SAMPLE_RATE = int(os.getenv("FRAME_SAMPLE_RATE", 5))  # Analyze every 5th frame
VIDEO_PROCESSING_TIMEOUT = int(os.getenv("TIMEOUT_SECONDS", 3600))  # 1 hour

# API Configuration
API_HOST = os.getenv("API_HOST", "0.0.0.0")
API_PORT = int(os.getenv("API_PORT", 8000))
CORS_ORIGINS = [
    "http://localhost:3000",
    "http://localhost:5173",
    "http://127.0.0.1:3000",
    "http://127.0.0.1:5173",
]

# Processing
MAX_WORKERS = int(os.getenv("MAX_WORKERS", 4))
CACHE_RESULTS = True
CACHE_TTL = 3600  # 1 hour

# Database (future use)
DATABASE_URL = os.getenv("DATABASE_URL", f"sqlite:///{BASE_DIR}/vod_tracker.db")

# Logging
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOG_FILE = LOGS_DIR / "app.log"

# Analysis Settings
MIN_PLACEMENT_SCORE = 1
MAX_PLACEMENT_SCORE = 10
PLACEMENT_SCORE_DECIMAL_PLACES = 1

# Crosshair Detection
CROSSHAIR_DETECTION_CONFIDENCE = 0.85
CROSSHAIR_COLORS = [
    (0, 255, 0),      # Green
    (255, 0, 255),    # Magenta
    (255, 100, 0),    # Orange
    (100, 100, 255),  # Light Blue
    (255, 255, 0),    # Yellow
]

# Map Locations
VALORANT_MAPS = {
    "Ascent": {
        "sites": ["A", "B"],
        "areas": ["A Main", "A Site", "A Heaven", "B Main", "B Site", "B Lobby", "Mid", "Spawn"],
    },
    "Split": {
        "sites": ["A", "B"],
        "areas": ["A Main", "A Site", "A Tower", "B Main", "B Site", "B Lobby", "Mid", "Spawn"],
    },
    "Bind": {
        "sites": ["A", "B"],
        "areas": ["A Main", "A Site", "B Main", "B Site", "Mid", "Spawn"],
    },
    "Haven": {
        "sites": ["A", "B", "C"],
        "areas": ["A Main", "A Site", "B Main", "B Site", "C Main", "C Site", "Mid", "Spawn"],
    },
}

# Agent Classifications
AGENT_ROLES = {
    "Duelist": ["Jett", "Phoenix", "Reyna", "Yoru", "Neon", "Iso"],
    "Initiator": ["Sova", "Breach", "Skye", "KAY/O", "Gekko"],
    "Controller": ["Brimstone", "Viper", "Omen", "Astra", "Harbor"],
    "Sentinel": ["Cypher", "Killjoy", "Sage", "Deadlock", "Vyse"],
}

# Pro Player Benchmarks (placeholder - will be loaded from JSON)
PRO_BENCHMARKS_FILE = BASE_DIR / "data" / "pro_benchmarks.json"

print(f"Config loaded: ENV={ENV}, DEBUG={DEBUG}")
print(f"Temp Dir: {TEMP_DIR}")
print(f"Upload Dir: {UPLOAD_DIR}")
