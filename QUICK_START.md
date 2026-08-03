# Quick Start Guide: Valorant Crosshair Placement Analyzer

## What You're Building

An AI-powered tool that:
1. Takes a Valorant gameplay video as input
2. Analyzes every frame's crosshair placement
3. Compares against professional player standards
4. Identifies weak areas on specific maps
5. Provides specific, actionable improvement advice

**Output**: Detailed HTML/JSON report with:
- Overall placement score
- Per-location analysis (A Site, B Site, Mid, etc.)
- Comparison to pro players
- Specific weaknesses with fixes
- Improvement recommendations

---

## Why This Is Valuable

**Problem**: Most Valorant players don't know *why* they lose fights. Crosshair placement is fundamental - poor placement means you die before even seeing enemies.

**Solution**: Automated video analysis that teaches:
- "Your crosshair is too low at A Main - position it at head level instead"
- "You're missing off-angle positions 60% of the time at B Site"
- "You're 2.5 points below pro standard for your role"

**Accuracy Requirements** are critical because bad feedback wastes player time.

---

## Key Components You Need to Build

### 1. **Video Processing Pipeline**
- Extract frames from video file
- Identify which game is being played (map, round, phase)
- Track crosshair position across frames

### 2. **Crosshair Detection** (Most Critical)
- Detect where crosshair is pointing in each frame
- Must work with different crosshair colors/styles
- Must maintain >95% accuracy across resolutions

### 3. **Placement Scoring Engine**
- Score placement quality 1-10 based on:
  - Head-level accuracy (is crosshair at enemy head height?)
  - Angle coverage (does it protect common entry points?)
  - Preemptive positioning (is player pre-aiming vs reacting?)
  - Agent role alignment (does it match agent capabilities?)

### 4. **Weak Area Identification**
- Find locations (A Main, B Site, etc.) where player scores lowest
- Explain exactly what's wrong
- Provide specific drill/fix

### 5. **Pro Benchmarking**
- Store reference scores from professional gameplay
- Compare user to pro standard
- Show improvement potential

### 6. **Report Generation**
- Create visual, easy-to-understand output
- Show before/after comparisons
- Provide training plan

---

## Accuracy Standards

| Metric | Target | Why It Matters |
|--------|--------|----------------|
| Crosshair Detection | >95% | Wrong positions = wrong analysis |
| Map Location ID | >90% | Advice must be location-specific |
| Game Phase Recognition | >92% | Pre-plant vs post-plant placements differ |
| Placement Scoring | ±0.3 variance | User needs consistent, reliable feedback |

If you're hitting <90% on any metric, your feedback will frustrate users.

---

## Recommended Tech Stack

```
Backend: Python 3.9+
  - FastAPI: Web server for uploads/analysis
  - OpenCV: Video processing
  - YOLOv8: Crosshair detection (if using ML)
  - Tesseract-OCR: Read game HUD text
  - NumPy/Pandas: Data analysis

Frontend: React/Vue
  - Display analysis results
  - Interactive map with weak areas highlighted
  - Timeline of video with placement scores
  - Pro comparison visualization

Database: PostgreSQL (store analysis results)
Storage: S3 or local filesystem (temporary video storage)
```

---

## Development Phases

### Phase 1: Core Detection (Week 1-2)
✓ Read video files
✓ Extract frames
✓ Detect crosshair position
✓ Recognize map/round info from HUD

**Success**: Can identify what map/location and where crosshair is pointing

### Phase 2: Scoring Engine (Week 2-3)
✓ Build placement scoring algorithm
✓ Create reference benchmark data
✓ Calculate scores for frames

**Success**: Placement scores are consistent and make sense

### Phase 3: Analysis & Reporting (Week 3-4)
✓ Identify weak areas
✓ Generate improvement recommendations
✓ Create final report

**Success**: Report clearly shows what's wrong and how to fix it

### Phase 4: UI & Optimization (Week 4-5)
✓ Build frontend interface
✓ Optimize performance
✓ Test on real videos

**Success**: App processes 30-minute video in <10 minutes

### Phase 5: Validation & Refinement (Week 5+)
✓ Test on diverse player videos
✓ Validate against manual reviews
✓ Gather user feedback
✓ Iterate on accuracy

---

## Critical Success Factors

### 1. **Crosshair Detection Robustness**
Must work on:
- 720p, 1080p, 1440p, 2160p resolutions
- Different crosshair colors/styles
- All map backgrounds
- Stream/recorded video quality

**Test with**: Sample videos from different settings before shipping

### 2. **Consistent Placement Scoring**
- If you analyze the same frame twice, score should be same (±0.1)
- Should be comparable across different players' videos
- Must align with actual skill improvement

**Test with**: Repeated analysis, compare to pro player scores

### 3. **Specific, Actionable Advice**
❌ Bad: "Your placement needs work"
✅ Good: "In A Main, move crosshair 35px higher to align with box corner at head level. Practice in Aim Lab targeting this position."

**Test with**: Have players implement feedback and see if they improve

### 4. **Performance**
- 30-minute video should analyze in <10 minutes
- Use smart frame sampling (every 5th frame often sufficient)
- Cache results to avoid reprocessing

**Test with**: Time your pipeline on videos of various lengths

---

## Data Sources for Pro Benchmarks

### Where to Get Reference Data:
1. **Twitch/YouTube**: Radiant player VODs
   - Screen record their gameplay
   - Manually annotate crosshair placement
   - Build reference heatmaps per location

2. **Professional Streams**: Team player POVs
   - High quality, consistent settings
   - Different agents/roles

3. **Community Data**: Valorant coaches' recommendations
   - General guidance on placement by location
   - Agent-specific tips

### Benchmark Storage Format:
```json
{
  "pro_placement_standards": {
    "Ascent": {
      "A_Main": {
        "optimal_crosshair": {"x_offset": 0, "y_offset": -40},
        "pro_average_score": 8.4,
        "by_agent": {
          "Jett": 8.6,
          "Chamber": 8.2,
          "Sage": 8.1
        },
        "common_mistakes": [
          "Too low",
          "Not covering window",
          "Overextended"
        ]
      }
    }
  }
}
```

---

## Potential Challenges & Solutions

| Challenge | Solution |
|-----------|----------|
| Crosshair not visible in some frames | Interpolate from nearby frames, track movement |
| HUD text hard to read (OCR failures) | Use image processing + template matching hybrid |
| Different settings (resolution, crosshair style) | Normalize to standard reference, build detection flexibility |
| Analyzing full 45-min video takes too long | Frame sampling every 5 frames usually sufficient |
| Scoring algorithm seems inconsistent | Build extensive test suite with known answers |
| Users expect results to match their skill level | Validate against actual player rankings |

---

## Quick Validation Steps

After each component:
1. Test on 5-10 sample videos (different resolutions, maps, qualities)
2. Compare results to manual analysis
3. Document accuracy percentage
4. If accuracy <90%, iterate before moving forward
5. Keep test videos as regression test suite

---

## Getting Started

1. **Clone/Set up project structure** (see TECHNICAL_ROADMAP.md)
2. **Start with crosshair detection**
   - Hardest part, most critical
   - Get this right before moving forward
3. **Build game state recognition**
   - Extract HUD info, recognize current map/location
4. **Implement placement scoring**
   - Create algorithm that makes intuitive sense
   - Test with known positions
5. **Add professional benchmarks**
   - Research pro placement patterns
   - Store as reference data
6. **Build reporting & UI**
   - Make results clear and actionable

---

## Success Metrics

✅ Analyzes 30-minute video in <10 minutes
✅ Identifies weak areas with >80% accuracy
✅ Users understand their placement mistakes after reading report
✅ Users improve when following recommendations
✅ Reports match player skill level (Iron vs Radiant different benchmarks)
✅ Community provides positive feedback on accuracy

---

## Resources to Study

- **Valorant Crosshair Guides**: Professional coaches' positioning tips
- **OpenCV Tutorials**: Video processing and object detection
- **YOLOv8**: Object detection for crosshair/HUD detection
- **Valorant Map Coordinates**: Reference geometry for placement calculations
- **Professional VODs**: Study pro placement patterns on each map

---

## Next Immediate Steps

1. Read [PROJECT_PROMPT.md](PROJECT_PROMPT.md) for complete specification
2. Read [TECHNICAL_ROADMAP.md](TECHNICAL_ROADMAP.md) for implementation details
3. Read [AI_PROMPTS_AND_VALIDATION.md](AI_PROMPTS_AND_VALIDATION.md) for accuracy guidelines
4. Start building Phase 1: Video processing + crosshair detection
5. Create test suite with known videos before moving to Phase 2
