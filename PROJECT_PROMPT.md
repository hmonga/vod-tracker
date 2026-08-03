# Valorant Crosshair Placement Analyzer - Project Specification

## Project Overview
Build an AI-powered video analysis tool that evaluates player crosshair placement in Valorant gameplay videos and provides detailed feedback on placement quality, weak areas, and improvement recommendations.

## Core Requirements

### Input Processing
- Accept video files (.mp4, .mov, .webm) of any Valorant game mode (Competitive, Deathmatch, Unrated, Spike Rush)
- Support videos of varying quality/resolution (720p to 4K)
- Handle different frame rates (30fps, 60fps, 120fps+)
- Process videos up to 45 minutes in length

### Video Frame Analysis
1. **Crosshair Detection**
   - Detect crosshair position at every frame
   - Track crosshair movement patterns
   - Identify crosshair behavior during different scenarios (pre-aim, tracking, spray control)

2. **Game State Recognition**
   - Identify the current map and specific locations (site names, key areas, common positions)
   - Recognize game phase (buy phase, executes, post-plant, post-spike)
   - Detect player agents/roles
   - Identify round outcomes (win/loss/pistol/eco)

3. **Crosshair Placement Quality Metrics**
   - **Pre-Aim Score**: Is crosshair positioned at head level before engaging?
   - **Angle Hold Quality**: Is crosshair placed at common enemy positions?
   - **Timing Alignment**: Is crosshair reactive or proactive?
   - **Off-Angle Exploitation**: Is player using off-angles effectively?
   - **Positioning Context**: Is crosshair appropriate for player's role/agent?

### Analysis Output

#### Per-Frame Analysis
- Timestamp and map location
- Crosshair position (pixel coordinates + in-game map location)
- Placement quality score (1-10)
- Context (pre-aim, mid-fight, post-fight)

#### Weak Areas Identification
```
Format:
{
  "area": "A Site Long",
  "weak_placement_frequency": "45%",
  "common_mistakes": [
    "Crosshair too low (not at head level)",
    "Looking at ground instead of common positions"
  ],
  "average_score": 4.2,
  "severity": "high"
}
```

#### Specific Feedback Categories
1. **Head-Level Consistency**
   - Percentage of time crosshair is at proper height
   - Frames where placement is incorrect
   - Comparison to pro player benchmarks

2. **Map-Specific Weaknesses**
   - Per-site analysis
   - Specific location recommendations (e.g., "When holding A Main, aim at box corner")
   - Common angles player misses

3. **Scenario-Based Issues**
   - Pre-plant vs post-plant differences
   - Eco round performance
   - Duelist vs Controller agent-specific placement patterns

4. **Agent-Specific Context**
   - Adjust expectations based on agent (Jett positioning differs from Sage)
   - Role-appropriate feedback (Sentinel vs Initiator)

### AI/ML Components

#### Computer Vision
- **Object Detection**: OpenCV/YOLOv8 for crosshair detection
- **Optical Character Recognition**: Detect HUD elements for map/round info
- **Scene Understanding**: Classify game state from frame content

#### Video Processing Pipeline
```
1. Frame extraction + downsampling for efficiency
2. HUD element detection (mini-map, agent name, round counter)
3. Crosshair position extraction
4. Map location mapping
5. Temporal analysis (track crosshair movement patterns)
6. Quality scoring algorithm
```

#### Reference Data
- **Pro Player Benchmarks**: Incorporate crosshair placement patterns from professional players
- **Map Heatmaps**: Expected crosshair positions for each map location
- **Role-Based Standards**: Different expectations for different agent roles

### Scoring Algorithm

```
Placement Quality Score = 
  0.4 × (head_level_accuracy) +
  0.3 × (angle_positioning_quality) +
  0.2 × (preemptive_positioning) +
  0.1 × (role_alignment)

Where each factor is 0-10
```

### Output Report Format

```json
{
  "video_info": {
    "filename": "comp_ascent.mp4",
    "duration_minutes": 32,
    "average_fps": 60,
    "resolution": "1920x1080"
  },
  "overall_score": 6.8,
  "summary": "Good fundamentals but struggles with off-angle positioning",
  
  "scores_by_category": {
    "head_level_consistency": 7.2,
    "angle_positioning": 5.9,
    "preemptive_placement": 7.1,
    "role_alignment": 8.0
  },
  
  "weak_areas": [
    {
      "location": "A Site",
      "weak_score": 4.2,
      "reason": "Consistently aiming below head level on A Main",
      "fix": "In A Main, position crosshair 30px higher, aligned with boxes"
    },
    {
      "location": "B Site Long",
      "weak_score": 5.1,
      "reason": "Not using off-angle positioning effectively",
      "fix": "Rotate to closet angle to catch rotations earlier"
    }
  ],
  
  "map_analysis": {
    "map": "Ascent",
    "strong_areas": ["Mid"],
    "weak_areas": ["A Site Long", "B Main"],
    "specific_feedback": [...]
  },
  
  "improvement_plan": [
    {
      "priority": 1,
      "focus": "Head level placement in A Main",
      "duration_days": 7,
      "drills": "Aim trainers focusing on horizontal tracking at head level"
    }
  ],
  
  "comparison_to_pros": {
    "pro_average_score": 8.2,
    "your_score": 6.8,
    "key_differences": [...]
  }
}
```

## Technical Stack Recommendations

### Backend
- **Language**: Python (OpenCV, MediaPipe/YOLO, video processing)
- **Framework**: FastAPI or Flask for API endpoints
- **Video Processing**: FFmpeg for encoding/decoding
- **Storage**: Database to store analysis results

### Frontend
- **Visualization**: Interactive timeline with frame-by-frame analysis
- **Map Overlays**: Show crosshair positions on Valorant map
- **Heatmaps**: Visual representation of weak areas
- **Progress Tracking**: Comparison over multiple videos

### AI/ML Libraries
- **YOLOv8**: For crosshair detection
- **OpenCV**: Video processing and image analysis
- **MediaPipe**: Pose/scene understanding
- **NumPy/Pandas**: Data analysis

## Quality Metrics

### Accuracy Standards
- Crosshair detection: >95% accuracy
- Map location identification: >90% accuracy
- Game phase recognition: >92% accuracy
- Placement scoring consistency: <5% variance on test videos

### Benchmark Against Professionals
- Compare user placement scores against Radiant/Pro player benchmarks
- Identify specific pro techniques user can adopt

## Implementation Phases

### Phase 1: Foundation
- Video upload and frame extraction
- Basic crosshair detection
- HUD element recognition

### Phase 2: Analysis Engine
- Map location mapping
- Placement quality scoring
- Basic reporting

### Phase 3: Advanced Features
- Pro player comparison
- Agent-specific analysis
- Interactive visualization

### Phase 4: Optimization & Scale
- Model fine-tuning
- Performance optimization
- User feedback integration

## Success Criteria
- ✅ Analyze 30-minute video in <10 minutes
- ✅ Identify >80% of weak placement areas correctly
- ✅ Provide actionable, map-specific recommendations
- ✅ Users report understanding their weak areas after analysis
- ✅ Feedback correlates with player's skill level
- ✅ Consistent results across multiple videos

## Additional Considerations

### Data Privacy
- Store minimal raw footage (delete after analysis)
- Allow anonymous analysis
- No player identification requirements

### Extensibility
- Future: Agent positioning analysis
- Future: Ability usage timing analysis
- Future: Map control efficiency metrics
- Future: Crosshair movement smoothness analysis

### User Experience
- Clear before/after comparisons
- Video clips highlighting weak moments
- Downloadable improvement plan
- Progress tracking over multiple submissions
