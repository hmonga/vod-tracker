# Implementation Roadmap & Technical Guidelines

## Quick Start Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     USER INTERFACE                           │
│          (Upload Video, View Analysis, Track Progress)       │
└────────────────┬──────────────────────────────────────────────┘
                 │
┌────────────────▼──────────────────────────────────────────────┐
│                    API LAYER (FastAPI)                        │
│      /upload, /analyze, /results, /history, /compare         │
└────────────────┬──────────────────────────────────────────────┘
                 │
┌────────────────▼──────────────────────────────────────────────┐
│              VIDEO PROCESSING PIPELINE                        │
│  1. Frame Extraction  2. HUD Detection  3. Crosshair Track   │
│  4. Game State Parse  5. Placement Score 6. Report Generation │
└────────────────┬──────────────────────────────────────────────┘
                 │
┌────────────────▼──────────────────────────────────────────────┐
│           AI/ML MODELS & REFERENCE DATA                       │
│  • Crosshair Detection Model  • Pro Benchmarks               │
│  • Map Location Classifier    • Role-Based Standards          │
└─────────────────────────────────────────────────────────────────┘
```

## Core Technical Decisions

### Crosshair Detection Approach
**Recommended: Template Matching + Color Detection**
- Most Valorant players use distinctive crosshair colors (green, pink, etc.)
- Approach: Detect crosshair color in defined screen region → extract center coordinates
- Backup: Train YOLOv8 model on crosshair variations if template matching isn't robust

```python
# Pseudo-code for crosshair detection
def detect_crosshair(frame):
    # Define common crosshair colors (HSV range)
    # Extract crosshair color from center 20% of screen
    # Find largest connected component
    # Return centroid as crosshair position
```

### Game State Recognition
**Approach: Multi-stage Classification**
1. Extract HUD elements (text recognition for round #, agent name, map)
2. Analyze minimap region for game phase
3. Use temporal context (is spike planted? did round end?)

```python
# Key HUD regions to monitor:
# - Round counter: top-center
# - Agent name: bottom-right
# - Minimap: top-right corner
# - Economy: top-left (buy information)
```

### Map Location Mapping
**Strategy: Minimap-based + Neural Network**
1. Extract minimap from each frame
2. Normalize minimap coordinates
3. Map crosshair screen position → map coordinates using calibration
4. Classify specific location (A Main, B Site, etc.)

**Reference Data Needed:**
- Pro player crosshair placement heatmaps per map per location
- Expected "good placement" reference points for each common angle

## Python Project Structure

```
vod_tracker/
├── main.py                          # Entry point
├── config.py                        # Configuration, constants
├── requirements.txt
│
├── api/
│   ├── __init__.py
│   ├── routes.py                    # FastAPI routes
│   └── models.py                    # Pydantic models
│
├── video_processing/
│   ├── __init__.py
│   ├── extractor.py                 # Frame extraction
│   ├── hud_detector.py               # HUD & game state recognition
│   └── crosshair_tracker.py          # Crosshair detection & tracking
│
├── analysis/
│   ├── __init__.py
│   ├── placement_scorer.py           # Quality scoring algorithm
│   ├── weak_area_detector.py         # Find problem areas
│   ├── pro_benchmarks.py             # Pro player comparisons
│   └── report_generator.py           # Generate output report
│
├── ml_models/
│   ├── __init__.py
│   ├── crosshair_detector.py         # YOLOv8 or template matching
│   ├── map_location_classifier.py    # Classify screen region to map location
│   └── game_state_classifier.py      # Identify game phase
│
├── data/
│   ├── map_layouts/                  # Valorant map images & coordinates
│   ├── pro_benchmarks.json           # Professional player metrics
│   ├── agent_roles.json              # Agent classifications
│   └── placement_standards.json      # Expected placement by role/location
│
└── utils/
    ├── __init__.py
    └── helpers.py                    # Utility functions
```

## Critical Implementation Details

### Frame Processing Optimization
```python
# Don't process every frame - sample strategically
SAMPLE_RATE = 5  # Analyze every 5th frame for initial pass
# Then do frame interpolation for fills between samples
# For videos 30-60 minutes, this keeps analysis time under 10 minutes
```

### Placement Scoring Formula (Detailed)

```python
def calculate_placement_score(crosshair_pos, map_location, game_phase, agent_role):
    """
    Returns score 1-10
    """
    scores = {}
    
    # 1. Head Level Accuracy (40%)
    # Expected head height varies by angle
    expected_head_y = get_expected_head_level(map_location)
    distance_from_head = abs(crosshair_pos.y - expected_head_y)
    scores['head_level'] = max(1, 10 - (distance_from_head / 50))
    
    # 2. Angle Positioning (30%)
    # Is crosshair covering likely enemy positions?
    coverage_score = calculate_angle_coverage(
        crosshair_pos, 
        map_location, 
        common_entry_points[map_location]
    )
    scores['angle_position'] = coverage_score
    
    # 3. Preemptive Positioning (20%)
    # How well is player pre-aiming common positions vs ground?
    preempt_score = 1
    if is_pre_aiming(crosshair_pos, game_phase):
        preempt_score = 8
    elif is_reactively_aiming(crosshair_pos):
        preempt_score = 5
    scores['preemptive'] = preempt_score
    
    # 4. Role Alignment (10%)
    # Does placement match agent role expectations?
    scores['role_alignment'] = get_role_score(agent_role, map_location, crosshair_pos)
    
    # Weighted average
    final_score = (
        scores['head_level'] * 0.4 +
        scores['angle_position'] * 0.3 +
        scores['preemptive'] * 0.2 +
        scores['role_alignment'] * 0.1
    )
    
    return round(final_score, 1)
```

### Weak Area Detection Algorithm

```python
def identify_weak_areas(analysis_frames, map_name):
    """
    Cluster crosshair placements by map location
    Identify locations where average score drops significantly
    """
    areas = group_by_map_location(analysis_frames)
    
    weak_areas = []
    overall_avg = calculate_overall_average(areas)
    
    for area, frames in areas.items():
        area_avg = calculate_average_score(frames)
        
        # Mark as weak if significantly below average
        if area_avg < (overall_avg - 1.5):  # More than 1.5 points below average
            weak_areas.append({
                'location': area,
                'score': area_avg,
                'sample_count': len(frames),
                'common_mistakes': identify_patterns(frames),
                'recommendation': generate_specific_advice(area, frames)
            })
    
    return sorted(weak_areas, key=lambda x: x['score'])
```

### Pro Player Comparison Data

```json
{
  "example_pro_metrics": {
    "Radiant Player Average": {
      "head_level_accuracy": 9.1,
      "angle_positioning": 8.7,
      "preemptive_positioning": 8.9,
      "role_alignment": 9.2,
      "overall": 8.9
    },
    "by_map": {
      "Ascent": {
        "A_Site": 8.8,
        "B_Site": 9.1,
        "Mid": 8.9
      }
    }
  }
}
```

## Model Training Guidance

### If Training Crosshair Detection Model
```python
# Dataset: Capture screenshots from Valorant streams
# - Various crosshair types, colors, settings
# - Different backgrounds (maps)
# - Various screen resolutions

# Training approach:
# 1. Annotate 500+ images with crosshair bounding boxes
# 2. Train YOLOv8n (nano) for speed - inference should be <10ms per frame
# 3. Validate on unseen video footage
# 4. Target: >95% precision, >90% recall
```

## Performance Targets

| Operation | Target Time | Notes |
|-----------|------------|-------|
| Frame extraction | 1-2 min | For 30 min video at 60fps (90K frames) |
| Crosshair detection | 3-4 min | Frame sampling reduces this significantly |
| HUD parsing | 1-2 min | OCR + template matching |
| Analysis & scoring | 2-3 min | Main algorithm execution |
| Report generation | <1 min | JSON serialization |
| **Total** | **<10 min** | For 30-45 minute video |

## Testing Strategy

### Unit Tests
- Crosshair detection on known images
- Scoring algorithm on synthetic data
- Map location classification

### Integration Tests
- Full pipeline on test videos (5-10 minutes)
- Accuracy against manually reviewed footage
- Output report format validation

### Validation
- Compare results against ground truth from professional play
- User feedback correlation with skill improvement

## Deployment Considerations

### Resource Requirements
- **GPU**: Optional but recommended for video processing (NVIDIA GPU)
- **Memory**: 8GB+ RAM for video processing
- **Storage**: Temporary storage for frame extraction (~2GB per 30 min video)

### Scalability
- Use task queues (Celery + Redis) for handling multiple uploads
- Implement video streaming analysis vs. full download
- Cache pro benchmark data

## Next Steps
1. Prototype frame extraction + crosshair detection
2. Build mock game state detector
3. Validate scoring algorithm with sample videos
4. Integrate pro player benchmarks
5. Build UI for results visualization
