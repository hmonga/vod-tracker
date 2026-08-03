# Vod Tracker - Development Context & Setup Guide

> **Last Updated:** August 3, 2026  
> **Project Status:** Real CV detection implemented, production upgrade in progress  
> **Repository:** https://github.com/hmonga/vod-tracker

---

## 🔑 REMINDER FOR NEXT CHAT SESSION

**Harsh owes an API key** to make this app fully production-grade.

Ask him for it at the start of the next conversation:

> "Hey, you said you'd give me an API key to upgrade Vod Tracker from mock to real production — do you have it now?"

**What the key is for:**
The app currently uses OpenCV hue-based detection for map/agent/crosshair (real, not mock).
To take it to the next level it needs one or more of these:
- **Riot Games API key** → pull actual match data (map, agent, round info) tied to the player's Riot ID — eliminates ALL guesswork from video detection, gives exact data
- **OpenAI / Vision API key** (optional) → use GPT-4 Vision to describe what's wrong with crosshair placement in plain English, frame by frame

With the Riot API key specifically, the app can:
1. Ask user for their Riot ID (e.g. `harsh#NA1`)
2. Pull their last 20 matches from Riot's API (map, agent, outcome, stats)
3. Match the VOD video to the correct game automatically
4. Get exact per-round positioning data
5. Give pinpoint accurate improvement advice based on real match context

**Without the key** everything still works — OpenCV detects map/agent from the video itself — just less precise than reading it directly from Riot's servers.

---

---

## 📋 Project Overview

**Vod Tracker** is a Valorant crosshair placement analyzer that:
- Accepts video files (Valorant comp, DM, unrated games)
- Analyzes player crosshair placement frame-by-frame
- Provides scoring, weak areas, and pro player comparisons
- Delivers desktop application (Windows installer) + web interface

**Target Users:** Gen Z gamers wanting to improve their crosshair placement  
**Aesthetic:** Modern, glassmorphism UI with animations, vibrant gradient colors

---

## 🏗️ Architecture Overview

### Full-Stack Architecture
```
Vod Tracker (Monorepo)
├── Backend (Python FastAPI)
│   ├── Video processing pipeline (OpenCV, FFmpeg)
│   ├── Crosshair placement analysis
│   ├── Scoring engine (1-10 scale)
│   └── REST API (8 endpoints, Pydantic validation)
├── Frontend (React 18 + Next.js 14)
│   ├── Modern UI with Framer Motion animations
│   ├── Tailwind CSS custom theme
│   └── React Query for state management
└── Desktop (Electron wrapper)
    └── Embedded Python backend + bundled frontend
    └── NSIS installer for Windows (.exe distribution)
```

### Technology Stack

**Backend:**
- FastAPI 0.104.1+ (async REST API on port 8000)
- Python 3.9+
- OpenCV 4.8.1.78 (video frame extraction)
- NumPy 1.24.3 (numerical computation)
- Pydantic 2.5.0 (request/response validation)
- SQLAlchemy 2.0.23 (prepared for database, currently in-memory)
- ffmpeg-python (video manipulation)

**Frontend:**
- React 18.2.0 with Next.js 14.0.0 (App Router)
- TypeScript 5.3.3
- Tailwind CSS 3.3.6 (custom theme with brand colors)
- Framer Motion 10.16.12 (12+ keyframe animations)
- React Query 5.25.0 (async state management)
- React Hook Form + Zod (form validation)
- Axios 1.6.2 (HTTP client)

**Desktop:**
- Electron 27.0.0
- electron-builder 24.6.4 (NSIS Windows installer)
- cross-env 7.0.3 (cross-platform environment)

---

## 📂 Project Structure

```
Vod_Tracker/
├── backend/
│   ├── main.py                    # Entry point (python main.py)
│   ├── config.py                  # Centralized configuration
│   ├── requirements.txt            # Python dependencies
│   ├── app/
│   │   ├── main.py               # FastAPI app setup
│   │   ├── api/
│   │   │   ├── models.py         # Pydantic validation models (15+ classes)
│   │   │   └── routes.py         # 8 API endpoints
│   │   └── analysis/
│   │       └── analyzer.py       # Video analysis engine (mock implementation)
│   └── Dockerfile
│
├── frontend/
│   ├── package.json              # Node.js dependencies + build scripts
│   ├── tsconfig.json
│   ├── tailwind.config.ts        # Tailwind theme customization
│   ├── next.config.js            # Next.js build configuration
│   ├── electron-main.js          # Electron entry point
│   ├── preload.js               # Electron security layer
│   ├── src/
│   │   └── app/
│   │       ├── layout.tsx        # Root layout
│   │       ├── page.tsx          # Home/landing page
│   │       ├── globals.css       # Global styles + animations
│   │       ├── providers.tsx     # React Query + Toast setup
│   │       └── upload/
│   │           └── page.tsx      # Video upload interface
│   └── src/components/
│       └── Navbar.tsx            # Navigation header
│
├── Documentation/
│   ├── README.md                 # Project overview + download link
│   ├── GETTING_STARTED.md        # Quick start guide
│   ├── QUICK_START.md            # 5-minute setup
│   ├── START_HERE.md             # Entry point guide
│   ├── PROJECT_PROMPT.md         # Original AI prompt & vision
│   ├── TECHNICAL_ROADMAP.md      # Architecture & implementation details
│   ├── UI_UX_DESIGN.md          # Design system & color palette
│   ├── INSTALLER_GUIDE.md        # Windows .exe build instructions
│   ├── FRONTEND_SETUP.md         # Frontend-specific setup
│   ├── INSTALLATION_SUMMARY.md   # All installation methods
│   ├── GITHUB_RELEASE_SETUP.md  # GitHub Actions + releases
│   ├── BUILD_SUMMARY.md          # Build process overview
│   ├── FILE_CHECKLIST.md         # Complete file inventory
│   ├── AI_PROMPTS_AND_VALIDATION.md # System prompts & validation
│   └── DEVELOPMENT_CONTEXT.md    # THIS FILE
│
├── CI/CD:
│   ├── .github/workflows/build-release.yml  # Auto-build on push/tag
│   ├── build-installer.bat                  # Windows batch build script
│   ├── setup.sh                             # Unix setup script
│   └── setup.bat                            # Windows setup script
│
├── Docker:
│   ├── docker-compose.yml        # Full-stack orchestration
│   ├── backend/Dockerfile
│   └── frontend/Dockerfile
│
├── Configuration:
│   ├── .env.example              # Environment variables template
│   └── .gitignore
```

---

## 🎨 Design System

**Color Palette:**
- Primary Brand: Purple (#8B5CF6)
- Secondary: Pink (#EC4899)
- Accent: Cyan (#06B6D4)
- Dark Background: #0F172A (darker: #0A0E27)
- Success: #10B981
- Warning: #F97316
- Danger: #EF4444
- Info: #3B82F6

**Animations (Framer Motion):**
- fadeInUp, slideInRight, glow, float, shimmer, spin-slow, pulse-slow
- Staggered delays (0s, 0.1s, 0.2s, 0.3s)
- Hover lift effects on interactive elements

**Typography:**
- UI: Poppins/Inter
- Code: Space Mono
- Responsive: mobile <640px, tablet 640-1024px, desktop >1024px

---

## 🚀 Setup & Deployment Instructions

### **Option 1: Development Setup (Local Machine)**

#### Prerequisites
- Python 3.9+
- Node.js 18+ (v22.13.1 tested)
- npm 10+
- FFmpeg (optional, for video processing)

#### Backend Setup
```bash
cd backend
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
python main.py
```
Backend runs on **http://localhost:8000**

#### Frontend Setup
```bash
cd frontend
npm install
npm run dev
```
Frontend runs on **http://localhost:3000**

### **Option 2: Windows Installer Build**

From the project root:
```bash
# On Windows:
./build-installer.bat

# Output: frontend/dist/Vod Tracker Setup 1.0.0.exe (~150-200MB)
```

The installer:
- Bundles frontend as static files
- Embeds Python backend
- Auto-starts backend on app launch
- Creates desktop shortcut + Start Menu entry
- One-click installation

### **Option 3: Docker Setup**

```bash
docker-compose up
```
Services:
- Backend: http://localhost:8000
- Frontend: http://localhost:3000

---

## 🔌 API Endpoints

All endpoints return JSON (Pydantic-validated):

| Method | Endpoint | Purpose |
|--------|----------|---------|
| POST | `/api/upload` | Upload video file (multipart form) |
| POST | `/api/analyze/{video_id}` | Start background analysis |
| GET | `/api/analysis/{video_id}` | Get analysis results |
| GET | `/api/analysis/{video_id}/progress` | Real-time progress tracking |
| GET | `/api/benchmarks` | Pro player reference data |
| GET | `/api/stats/{video_id}` | Player statistics |
| GET | `/api/download-report/{video_id}` | Export as PDF/JSON |
| GET | `/api/maps` | Map reference data |
| GET | `/api/agents` | Agent role definitions |
| GET | `/health` | Health check |

---

## 📊 Analysis Pipeline

```
Video Upload
    ↓
Extract Metadata (resolution, FPS, duration)
    ↓
Sample Frames (every N frames)
    ↓
Detect Crosshair & Placement
    ↓
Score Placement (0.4×head_level + 0.3×angle + 0.2×preemptive + 0.1×role)
    ↓
Identify Weak Areas (>1.5 points below average)
    ↓
Compare to Pro Benchmarks
    ↓
Generate Report (JSON/PDF)
    ↓
Return to User
```

**Scoring Formula:** 1-10 scale
- Head Level Accuracy: 40%
- Angle Coverage: 30%
- Preemptive Aiming: 20%
- Role Alignment: 10%

---

## ⚙️ Configuration

### Environment Variables (`.env`)
```env
# Backend
BACKEND_ENV=development
BACKEND_PORT=8000
BACKEND_HOST=0.0.0.0
NEXT_PUBLIC_API_URL=http://localhost:8000

# Processing
MAX_VIDEO_SIZE=2147483648  # 2GB in bytes
FRAME_SAMPLE_RATE=5        # Process every Nth frame
SUPPORTED_FORMATS=mp4,mov,webm,avi,mkv

# Paths
TEMP_DIR=./backend/temp
UPLOAD_DIR=./backend/uploads
LOGS_DIR=./backend/logs
```

### Backend Config (config.py)
- Video settings: max size, formats, sample rate
- API settings: host, port, CORS origins
- Valorant maps: all competitive map definitions with sites/areas
- Agent roles: Duelist, Sentinel, Initiator, Controller

---

## 🎯 Current Implementation Status

### ✅ Complete
- Project structure and file organization
- FastAPI backend with all 8 endpoints defined
- Frontend pages: Home, Upload, Results (framework)
- Tailwind CSS theme + Framer Motion animations
- Pydantic models for all request/response validation
- Configuration system (centralized, flexible)
- Docker support (compose + individual Dockerfiles)
- GitHub Actions CI/CD workflow
- Windows installer builder (NSIS/electron-builder)
- Setup scripts for Unix and Windows
- Comprehensive documentation (14 files)
- Git repository initialized and synced to GitHub

### 🟡 Partially Complete (Mock/Framework Only)
- VideoAnalyzer class (architecture complete, ML/CV logic is placeholder)
- Analysis results (returns realistic mock data, not actual video analysis)
- Database integration (SQLAlchemy prepared, currently in-memory storage)
- Results dashboard page (UI components created, not fully wired)
- PDF export (JSON export works, PDF conversion not implemented)

### ⏳ Not Started
- Real crosshair detection (ML/CV model needed)
- Real placement scoring (algorithmic analysis)
- Actual pro player benchmark comparison
- Database schema + migrations
- Authentication/authorization
- User account system

---

## 🐛 Known Issues & Limitations

### Mac Development Setup
- System Python pip has limited package index
- **Workaround:** Use virtual environment (`python3 -m venv`) with upgraded pip
- **Alternative:** Use Homebrew Python or Docker for consistent environment

### npm Registry Issue
- If npm install fails with `@radix-ui/react-primitives` 404 error, your npm is configured for internal Fiserv registry
- **Fix:** Create `.npmrc` in frontend directory:
  ```
  registry=https://registry.npmjs.org/
  ```

### Video Processing
- OpenCV (cv2) may require system-level dependencies on Mac
- **Install:** `brew install opencv`
- ffmpeg-python requires FFmpeg: `brew install ffmpeg`

### Windows-Only Features
- Electron app packaging (requires Windows for .exe build)
- NSIS installer generation (Windows only)
- **Workaround on Mac/Linux:** Build in Docker or cross-compile with wine

---

## 📝 Next Steps for Desktop Implementation

### Phase 1: Local Testing (Desktop)
1. Clone repository: `git clone https://github.com/hmonga/vod-tracker.git`
2. Follow setup instructions above
3. Test all UI interactions and animations
4. Verify API communication works

### Phase 2: Backend ML/CV Integration
1. Replace mock data in `analyzer.py` with real crosshair detection
2. Implement actual placement scoring algorithm
3. Add pro player benchmark matching
4. Test with sample Valorant videos

### Phase 3: Database & Persistence
1. Set up SQLite or PostgreSQL
2. Migrate from in-memory storage to database
3. Add user history/statistics tracking
4. Implement result export (PDF reports)

### Phase 4: Production Deployment
1. Build Windows installer: `./build-installer.bat`
2. Test installer on clean Windows machine
3. Create GitHub release with .exe download
4. Add analytics/telemetry (optional)

---

## 🔗 Important Links

- **GitHub Repository:** https://github.com/hmonga/vod-tracker
- **GitHub Releases:** https://github.com/hmonga/vod-tracker/releases (Windows installer)
- **Issues/Feature Requests:** GitHub Issues tab

---

## 💡 Development Tips

### Quick Start Commands
```bash
# Start everything locally
cd backend && python main.py &
cd frontend && npm run dev

# Access app
http://localhost:3000
```

### Testing Mock API
```bash
# Check backend health
curl http://localhost:8000/health

# Get maps reference
curl http://localhost:8000/api/maps

# Get agent roles
curl http://localhost:8000/api/agents
```

### Building & Debugging
```bash
# Frontend type checking
npm run type-check

# Backend linting (when added)
# python -m pylint app/

# Docker full-stack test
docker-compose up --build
```

### Git Workflow
```bash
git add .
git commit -m "Description"
git push origin main

# Tags trigger Windows installer build
git tag v1.1.0
git push origin v1.1.0
```

---

## 📚 Documentation Files Quick Reference

| File | Purpose |
|------|---------|
| README.md | Overview + download link |
| START_HERE.md | Entry point for new users |
| QUICK_START.md | 5-minute setup guide |
| PROJECT_PROMPT.md | Original vision + AI prompts |
| TECHNICAL_ROADMAP.md | Architecture deep-dive |
| UI_UX_DESIGN.md | Design system details |
| INSTALLER_GUIDE.md | Windows .exe building |
| FRONTEND_SETUP.md | React/Next.js specifics |
| DEVELOPMENT_CONTEXT.md | **THIS FILE** - Complete reference |

---

## 🆘 Troubleshooting

### Backend won't start
```bash
# Check Python version
python3 --version  # Need 3.9+

# Check pip packages
pip list | grep fastapi

# Reinstall dependencies
pip install --upgrade pip
pip install -r requirements.txt --force-reinstall
```

### Frontend build fails
```bash
# Clear cache
rm -rf node_modules package-lock.json
npm install

# Check Node version
node --version  # Need 18+
```

### API calls return 404
- Ensure backend is running on port 8000
- Check NEXT_PUBLIC_API_URL in .env
- Verify CORS middleware in backend/app/main.py

### Video upload fails
- Check MAX_VIDEO_SIZE limit (2GB default)
- Verify SUPPORTED_FORMATS include your video type
- Ensure /backend/uploads directory exists and is writable

---

## 📞 Contact & Support

For issues or questions:
1. Check relevant .md documentation files
2. Review GitHub Issues
3. Check conversation history in Copilot chat
4. Reference this DEVELOPMENT_CONTEXT.md for complete context

---

**Last Sync to GitHub:** August 3, 2026  
**Repository Owner:** hmonga  
**License:** MIT (or as specified in LICENSE file)
