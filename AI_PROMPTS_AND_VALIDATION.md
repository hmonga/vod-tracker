# AI-Powered Development Prompts & Accuracy Guidelines

## Master Prompt for Development

Use this when working with AI code generation (Claude, GitHub Copilot, etc.):

```
I'm building a Valorant crosshair placement analyzer that processes video files 
and provides detailed feedback on crosshair positioning quality.

Project Goal: 
Analyze Valorant gameplay videos (comp, DM, unrated) and identify:
1. Crosshair placement quality (score 1-10)
2. Map-specific weak areas with exact feedback
3. Comparison to professional player standards
4. Actionable improvement recommendations

Key Requirements:
- Process 30-45 minute videos in <10 minutes
- Detect crosshair position at every frame (or sampled)
- Recognize map location and game state from HUD
- Score placement accuracy against professional benchmarks
- Generate detailed JSON report with visualizations

Technical Stack: Python + FastAPI + OpenCV + YOLOv8

Critical Accuracy Requirements:
- Crosshair detection: >95% accuracy
- Map location identification: >90% accuracy
- Game phase recognition: >92% accuracy
- Placement scoring: Consistent within 0.3 points

When you generate code, include:
1. Type hints for all functions
2. Error handling for edge cases
3. Comprehensive comments explaining logic
4. Validation checks for input data
5. Performance optimizations (sample frames, cache results)

Priority: Accuracy over speed in analysis phase
```

## AI Prompts for Specific Components

### 1. Crosshair Detection
```
Build a Python function that detects the player's crosshair position 
in a Valorant gameplay frame with >95% accuracy.

The function should:
- Accept a video frame (numpy array)
- Return (x, y) coordinates of crosshair center
- Handle different crosshair colors (player customizable)
- Work on various map backgrounds
- Run in <50ms per frame

Approach options:
A) Template matching: Match against predefined crosshair shapes
B) Color detection: Identify bright/distinct crosshair colors in center screen
C) ML-based: Train YOLOv8 on crosshair dataset

Recommend the most reliable approach with reasoning.
Include fallback strategies if primary method fails.
```

### 2. Game State Recognition
```
Create a game state detector that identifies from a Valorant frame:
1. Current map (Ascent, Split, Bind, Haven, Icebox, Breeze, Lotus, Sunset)
2. Current round number
3. Player's agent/character
4. Game phase (buy, execute, post-plant, post-spike, etc.)
5. Whether it's CT or T side

Key: Extract and parse HUD elements using OCR and template matching.

Return structured data:
{
  'map': 'Ascent',
  'round': 5,
  'agent': 'Jett',
  'phase': 'execute',
  'side': 'attacker'
}

Focus on reliability - must work on 720p, 1080p, 1440p, 2160p.
Include confidence scores for each detection.
```

### 3. Placement Quality Scorer
```
Implement a placement quality algorithm that scores Valorant 
crosshair placement from 1-10 based on:

Scoring Factors:
1. Head-Level Accuracy (40% weight)
   - Is crosshair at enemy head height?
   - Varies by position on map

2. Angle Positioning (30% weight)
   - Does crosshair cover likely enemy positions?
   - Award points for off-angle positioning

3. Preemptive Positioning (20% weight)
   - Is player pre-aiming or ground-aiming?
   - Pre-aim should score higher

4. Role Alignment (10% weight)
   - Does placement match agent role?
   - Initiators, sentinels, controllers have different standards

Input:
- Crosshair position (x, y)
- Map and specific location
- Player agent/role
- Game phase
- Nearby environment context

Output:
- Score 1-10
- Breakdown by category
- Explanation of score

Key: Be consistent (±0.3 variance on same position repeated).
```

### 4. Map Location Classifier
```
Create a classifier that maps screen coordinates to Valorant 
in-game locations with >90% accuracy.

Input:
- Crosshair screen position (x, y in pixels)
- Game frame (for minimap analysis)
- Current map name
- Player perspective

Output:
{
  'map': 'Ascent',
  'location': 'A_Main',
  'confidence': 0.94,
  'zone': 'long'
}

Approach:
1. Analyze minimap region to understand player position
2. Use crosshair position + direction relative to player
3. Reference map layout coordinates
4. Classify into named zones (A Main, B Site, Mid, etc.)

This needs to work accurately across different resolutions 
and video qualities.
```

### 5. Pro Player Benchmark Integration
```
Design a system to compare player placement against 
professional player benchmarks.

For each map location, store reference data:
- Average pro placement score for that location
- Heatmap of common crosshair positions
- Role-specific variations (Jett on site vs. Sage on site)

Comparison output:
{
  'location': 'A_Main',
  'your_score': 5.8,
  'pro_average': 8.3,
  'percentile': '25th',
  'key_difference': 'You aim too low, pros hold head-level',
  'improvement_potential': 2.5
}

Data structure should allow:
- Easy updates as new pro gameplay is analyzed
- Role and agent-specific comparisons
- Temporal trends (pro players improving over time)
```

### 6. Weak Area Detection
```
Implement algorithm to identify map locations where 
player's placement is consistently below average.

Algorithm:
1. Group all analyzed frames by map location
2. Calculate average score for each location
3. Identify locations significantly below player's average
4. Extract common mistakes from that location
5. Generate specific, actionable advice

Output format:
{
  'weak_areas': [
    {
      'location': 'A_Site_Long',
      'your_score': 4.2,
      'your_average': 6.8,
      'gap': 2.6,
      'severity': 'HIGH',
      'common_mistakes': [
        'Crosshair below head level by ~30 pixels',
        'Not adjusting for elevation changes',
        'Missing box angles'
      ],
      'specific_advice': 'When holding A Long, position crosshair aligned with top of box at head height. Practice in aim trainer.',
      'frames_analyzed': 245
    }
  ]
}

Critical: Advice must be specific and actionable.
```

## Accuracy Validation Checklist

### Before Deploying Any Component
- [ ] Unit tests pass with 100% accuracy on synthetic test data
- [ ] Integration tests pass on 5-10 minute sample videos
- [ ] Results validated against manually reviewed footage
- [ ] Edge cases handled (low res, high res, night/bright maps)
- [ ] Performance meets <10 minute total pipeline target

### Testing Against Known Ground Truth
```python
# Create test cases with known answers:
test_cases = [
    {
        'frame': sample_frame_1,
        'expected_crosshair': (960, 540),
        'expected_map': 'Ascent',
        'expected_location': 'A_Main',
        'expected_score': 7.2
    },
    # ... more test cases
]

# Run validation
for test in test_cases:
    result = analyze_frame(test['frame'])
    assert_accuracy(result, test)
```

## Common Pitfalls to Avoid

### 1. Over-Training on Limited Data
- **Problem**: Model performs well on training videos but fails on new players' videos
- **Solution**: Use diverse data sources (different players, settings, resolutions)

### 2. Ignoring Screen Resolution Differences
- **Problem**: Coordinate-based detection fails on different resolutions
- **Solution**: Normalize all coordinates to standard resolution (e.g., 1920x1080)

### 3. Inconsistent Game State Detection
- **Problem**: OCR fails on blurry frames or specific fonts
- **Solution**: Use multiple detection methods + temporal consistency checks

### 4. One-Size-Fits-All Scoring
- **Problem**: Scoring doesn't account for different agent roles or playstyles
- **Solution**: Build role-based and context-aware scoring variants

### 5. Ignoring Professional Play Diversity
- **Problem**: Single "pro standard" doesn't exist - varies by role, map, meta
- **Solution**: Store diverse benchmarks and allow user to select comparison style

### 6. Processing Efficiency Breakdown
- **Problem**: Analyzing every frame takes 30+ minutes for a video
- **Solution**: Smart sampling (every 5th frame) + parallel processing

## Validation Against Real Gameplay

### Before Publishing
1. Analyze 10 videos from different skill levels (Iron through Radiant)
2. Have 2-3 people manually review results for accuracy
3. Compare against actual match outcomes and player rankings
4. Verify weak areas identified match player's actual improvement needs
5. Test on various video codecs and qualities

### User Feedback Loop
```json
{
  "feedback_request": {
    "after_analysis": "Did our feedback help you improve?",
    "follow_up": "Did you work on the identified weak areas?",
    "reanalysis": "Upload another video after 1 week for comparison"
  }
}
```

## Continuous Improvement Strategy

### Version 1.0 (MVP)
- Basic crosshair detection
- Simple placement scoring
- Map location identification
- Basic report generation

### Version 1.1
- Pro player comparison
- Agent-specific scoring
- Weak area detection with specific advice

### Version 1.2
- Performance optimization (<10 min target)
- Better game state detection
- Role-based analysis

### Version 2.0
- Advanced features (agent ability usage, positioning timing, etc.)
- Community benchmarks
- Progress tracking over multiple videos
