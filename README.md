# Valorant Crosshair Placement Analyzer

A modern, AI-powered desktop application that analyzes Valorant gameplay videos and provides detailed feedback on crosshair placement quality, weak areas, and improvement recommendations.

## 📥 Download

**[📦 Download Latest Version (ZIP)](https://github.com/hmonga/vod-tracker/archive/refs/heads/main.zip)**

Simply click the link above to download the complete app. Extract and run `build-installer.bat` (Windows) or `setup.sh` (macOS/Linux) to get started!

## 🎮 Features

✨ **Instant Analysis** - Upload a video and get comprehensive placement analysis in minutes
📊 **Detailed Scoring** - Get scores for head-level accuracy, angle positioning, pre-aim quality, and role alignment
🗺️ **Map-Specific Feedback** - Identify weak areas on specific maps (A Site, B Site, Mid, etc.)
🏆 **Pro Comparisons** - Compare your placement against professional player benchmarks
📈 **Improvement Plans** - Receive actionable recommendations to level up your game
⚡ **Modern UI** - Beautiful, Gen Z-focused interface with smooth animations

## 📋 Prerequisites

- **Node.js** 18+ (for frontend)
- **Python** 3.9+ (for backend)
- **FFmpeg** (for video processing)
- **4GB+ RAM** recommended
- **2GB free disk space** for video processing

### Install Prerequisites

**macOS:**
```bash
# Using Homebrew
brew install node python ffmpeg
```

**Windows:**
- Download and install Node.js from https://nodejs.org/
- Download and install Python from https://www.python.org/
- Download and install FFmpeg from https://ffmpeg.org/download.html

**Linux (Ubuntu/Debian):**
```bash
sudo apt-get update
sudo apt-get install nodejs python3 python3-pip ffmpeg
```

## 🚀 Quick Start

### 1. Clone/Extract Project
```bash
cd ~/vod-tracker  # or wherever you extracted it
```

### 2. Backend Setup (Terminal 1)

```bash
cd backend

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Start backend server
python main.py
```

The backend will start on `http://localhost:8000`

**Verify it's working:**
- Open http://localhost:8000/docs in your browser
- You should see the API documentation

### 3. Frontend Setup (Terminal 2)

```bash
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

The frontend will start on `http://localhost:3000`

**Access the app:**
- Open http://localhost:3000 in your browser
- You should see the Valorant Crosshair Analyzer home page

## 📖 How to Use

### 1. Upload Video
- Click "Upload Video" button
- Drag and drop or select a Valorant gameplay video (.mp4, .mov, .webm)
- Supported formats: MP4, MOV, WebM
- Maximum file size: 2GB
- Recommended: Videos 5-45 minutes long

### 2. Wait for Analysis
- The app will analyze your video frame by frame
- Processing time: ~10 minutes per 30-minute video
- You'll see a progress bar and ETA

### 3. View Results
- **Overall Score**: Your placement quality (1-10)
- **Category Breakdown**: Scores for head-level, angle positioning, pre-aim, role alignment
- **Weak Areas**: Locations where your placement is below average
- **Map Analysis**: Per-location performance breakdown
- **Pro Comparison**: How you compare to professional player standards
- **Improvement Plan**: Specific drills and exercises to improve

### 4. Download Report
- Export your analysis as PDF or JSON
- Share with coaches or teammates
- Track progress over multiple uploads

## 🏗️ Project Structure

```
vod-tracker/
├── backend/                          # Python FastAPI backend
│   ├── app/
│   │   ├── main.py                   # FastAPI application
│   │   ├── api/
│   │   │   ├── routes.py             # API endpoints
│   │   │   └── models.py             # Pydantic models
│   │   ├── video_processing/
│   │   │   ├── extractor.py          # Frame extraction
│   │   │   ├── hud_detector.py       # Game state detection
│   │   │   └── crosshair_tracker.py  # Crosshair detection
│   │   ├── analysis/
│   │   │   ├── scorer.py             # Placement scoring
│   │   │   ├── weak_areas.py         # Weak area detection
│   │   │   ├── benchmarks.py         # Pro comparisons
│   │   │   └── report.py             # Report generation
│   │   ├── ml_models/
│   │   │   ├── crosshair_detector.py # ML-based detection
│   │   │   └── game_state.py         # Game state classifier
│   │   ├── data/
│   │   │   ├── pro_benchmarks.json   # Professional metrics
│   │   │   ├── agent_roles.json      # Agent classifications
│   │   │   └── maps.json             # Map data
│   │   └── utils/
│   │       └── helpers.py            # Utility functions
│   ├── requirements.txt              # Python dependencies
│   ├── config.py                     # Configuration
│   └── main.py                       # Entry point
│
├── frontend/                         # React/Next.js frontend
│   ├── src/
│   │   ├── app/
│   │   │   ├── layout.tsx            # Root layout
│   │   │   ├── page.tsx              # Home page
│   │   │   ├── upload/page.tsx       # Upload page
│   │   │   ├── results/page.tsx      # Results page
│   │   │   └── globals.css           # Global styles
│   │   ├── components/
│   │   │   ├── Navbar.tsx
│   │   │   ├── Hero.tsx
│   │   │   ├── UploadZone.tsx
│   │   │   ├── ScoreCard.tsx
│   │   │   ├── Button.tsx
│   │   │   └── ...other components
│   │   ├── hooks/
│   │   │   ├── useUpload.ts
│   │   │   ├── useAnalysis.ts
│   │   │   └── ...custom hooks
│   │   ├── lib/
│   │   │   ├── api.ts               # API client
│   │   │   └── utils.ts
│   │   └── types/
│   │       └── index.ts
│   ├── package.json
│   ├── tailwind.config.ts
│   ├── tsconfig.json
│   └── next.config.js
│
├── docker-compose.yml               # Docker setup (optional)
├── .env.example                     # Environment variables template
└── README.md                        # This file
```

## ⚙️ Configuration

### Backend Config

Edit `backend/config.py`:
```python
# Video processing
MAX_VIDEO_SIZE = 2 * 1024 * 1024 * 1024  # 2GB
SUPPORTED_FORMATS = ['mp4', 'mov', 'webm']
FRAME_SAMPLE_RATE = 5  # Analyze every 5th frame
TEMP_DIR = '/tmp/vod-tracker'  # Temp storage for frames

# API
API_HOST = '0.0.0.0'
API_PORT = 8000
CORS_ORIGINS = ['http://localhost:3000', 'http://localhost:5173']

# Processing
MAX_WORKERS = 4  # Parallel processing threads
TIMEOUT_SECONDS = 3600  # 1 hour max per video
```

### Frontend Config

Edit `frontend/.env.local`:
```
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_APP_NAME=Vod Tracker
NEXT_PUBLIC_ANALYTICS_ID=your-ga-id
```

## 🔧 Troubleshooting

### Issue: Backend won't start
```bash
# Make sure Python 3.9+ is installed
python3 --version

# Make sure all dependencies are installed
pip install -r requirements.txt

# Make sure port 8000 is not in use
lsof -i :8000  # macOS/Linux
netstat -ano | findstr :8000  # Windows
```

### Issue: Frontend won't load
```bash
# Clear node_modules and reinstall
rm -rf node_modules package-lock.json
npm install

# Clear Next.js cache
rm -rf .next
npm run dev
```

### Issue: Video upload fails
```bash
# Make sure FFmpeg is installed
ffmpeg -version

# Make sure temp directory exists and has write permissions
mkdir -p /tmp/vod-tracker
chmod 755 /tmp/vod-tracker

# Check available disk space
df -h  # macOS/Linux
```

### Issue: API connection errors
```bash
# Make sure backend is running
curl http://localhost:8000/health

# Check CORS settings if frontend can't reach backend
# Edit backend/config.py and add frontend URL to CORS_ORIGINS
```

## 🚢 Production Deployment

### Using Docker Compose (Recommended)

```bash
# Start both services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

### Manual Deployment

**Backend:**
```bash
cd backend
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:8000 app.main:app
```

**Frontend:**
```bash
cd frontend
npm run build
npm run start
```

## 📦 Building for Distribution

### Create Portable Package

**macOS:**
```bash
# Create app bundle (requires PyInstaller)
pip install pyinstaller
pyinstaller --onefile backend/main.py -n VodTracker
```

**Windows:**
```bash
# Create executable
pyinstaller --onefile backend/main.py -n VodTracker.exe
```

Then create a simple launcher script to start both backend and frontend.

## 🛠️ Development

### Running with Hot Reload

**Backend:**
```bash
cd backend
pip install uvicorn
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Frontend:**
```bash
cd frontend
npm run dev
```

### Running Tests

**Backend:**
```bash
cd backend
pip install pytest pytest-asyncio
pytest
```

**Frontend:**
```bash
cd frontend
npm test
```

### Linting & Formatting

**Backend:**
```bash
cd backend
pip install black flake8
black .
flake8 .
```

**Frontend:**
```bash
cd frontend
npm run lint
npm run format
```

## 📚 API Documentation

Once backend is running, visit:
```
http://localhost:8000/docs
```

This shows interactive API documentation with all available endpoints.

### Key Endpoints

- `POST /api/upload` - Upload video file
- `GET /api/analysis/{video_id}` - Get analysis results
- `GET /api/analysis/{video_id}/progress` - Get analysis progress
- `GET /api/benchmarks` - Get pro player benchmarks
- `POST /api/compare` - Compare against benchmarks

## 🎯 Next Steps

1. **Try the App**: Upload a Valorant video and see the analysis
2. **Customize**: Modify the UI colors, fonts, or layout in `frontend/tailwind.config.ts`
3. **Train Models**: Collect data and train the crosshair detection model
4. **Add Features**: Implement additional analysis features
5. **Share**: Deploy to a server for online access

## 🤝 Contributing

Found a bug? Want to improve something?
1. Create a GitHub issue describing the problem
2. Fork the repository
3. Create a feature branch
4. Make your changes
5. Submit a pull request

## 📝 License

This project is provided as-is for educational and personal use.

## 🆘 Support

**Having issues?**
1. Check the Troubleshooting section above
2. Check backend logs: `backend/logs/`
3. Check frontend console: Open DevTools (F12)
4. Review error messages carefully

## 📞 Contact

Have questions or suggestions? Feel free to reach out!

---

## 🚀 Performance Tips

- Use SSD for faster video processing
- Close other applications to free up RAM
- Process videos during off-peak hours
- Use a wired internet connection if uploading to cloud storage

## ⚡ Optimization

The app is optimized for:
- 30-45 minute videos
- 1080p-1440p resolution
- 60fps gameplay
- 4GB+ RAM systems

For longer videos or lower-end systems, processing may take longer.

---

**Enjoy analyzing your Valorant gameplay! 🎮✨**
