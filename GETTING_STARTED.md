# Getting Started Guide

Welcome to the Valorant Crosshair Placement Analyzer! This guide will walk you through setting up and running the application.

## 📋 Prerequisites

Before you begin, make sure you have the following installed:

1. **Python 3.9+** - Download from https://www.python.org/
2. **Node.js 18+** - Download from https://nodejs.org/
3. **FFmpeg** - Download from https://ffmpeg.org/download.html (optional but recommended)

### Verify Installation

Open your terminal and check:

```bash
python3 --version    # Should show Python 3.9+
node --version      # Should show Node 18+
npm --version       # Should show npm 9+
ffmpeg -version     # Should show FFmpeg version
```

## 🚀 Quick Start (Recommended)

### Option 1: Automatic Setup (macOS/Linux)

```bash
# Make setup script executable
chmod +x setup.sh

# Run setup
./setup.sh
```

### Option 2: Automatic Setup (Windows)

```bash
# Run setup
setup.bat
```

### Option 3: Manual Setup

#### Step 1: Backend Setup

```bash
# Navigate to backend directory
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

Backend will start at: **http://localhost:8000**

Check it's working:
- Visit http://localhost:8000/health in your browser
- Or visit http://localhost:8000/docs for API documentation

#### Step 2: Frontend Setup (New Terminal)

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Start frontend development server
npm run dev
```

Frontend will start at: **http://localhost:3000**

## 🌐 Access the Application

Once both servers are running:

1. Open your browser
2. Go to **http://localhost:3000**
3. You should see the Valorant Crosshair Analyzer home page
4. Click "Upload Video" to get started

## 🐳 Docker Setup (Easy Alternative)

If you prefer Docker:

```bash
# Make sure Docker is running, then:
docker-compose up

# Or in background:
docker-compose up -d
```

Then visit: http://localhost:3000

To stop:
```bash
docker-compose down
```

## 📝 Configuration

### Backend Configuration

Edit `backend/config.py` to customize:
- Video processing settings
- API port and host
- CORS origins
- Logging level

### Frontend Configuration

Edit `frontend/.env.local`:
```
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## 🎮 How to Use

1. **Upload**: Go to Upload page and drop your Valorant video
2. **Wait**: Let the analysis complete (check progress with notifications)
3. **Review**: See your placement scores and weak areas
4. **Improve**: Follow the improvement plan recommendations

## ❌ Troubleshooting

### Backend won't start
```bash
# Check Python installation
python3 --version

# Try reinstalling dependencies
pip install -r requirements.txt

# Make sure port 8000 is free
# macOS/Linux:
lsof -i :8000
# Windows:
netstat -ano | findstr :8000
```

### Frontend won't start
```bash
# Clear cache and reinstall
rm -rf node_modules package-lock.json
npm install

# Clear Next.js cache
rm -rf .next

# Start again
npm run dev
```

### "Cannot connect to backend" error
```bash
# Make sure backend is running first
# Check backend URL in frontend/.env.local
# Make sure it matches your backend address

# Try:
curl http://localhost:8000/health
```

### Video upload fails
```bash
# Check temp directory exists
mkdir -p /tmp/vod-tracker

# Check disk space
df -h

# Make sure ffmpeg is installed
ffmpeg -version
```

## 📚 Project Structure

```
vod-tracker/
├── backend/              # Python FastAPI backend
│   ├── app/
│   │   ├── api/         # API routes and models
│   │   └── analysis/    # Analysis engine
│   ├── requirements.txt
│   └── main.py
├── frontend/            # React/Next.js frontend
│   ├── src/
│   │   ├── app/        # Pages
│   │   └── components/ # React components
│   └── package.json
└── README.md
```

## 🔧 Development

### Backend Development

```bash
cd backend
source venv/bin/activate
pip install -r requirements.txt

# Development with auto-reload
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend Development

```bash
cd frontend
npm run dev
```

### Run Tests

```bash
# Backend tests
cd backend
pip install pytest pytest-asyncio
pytest

# Frontend tests
cd frontend
npm test
```

## 📦 Building for Production

### Backend

```bash
cd backend
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:8000 app.main:app
```

### Frontend

```bash
cd frontend
npm run build
npm run start
```

## 🌍 Deploying to the Cloud

### Option 1: Docker (Recommended)

```bash
# Build and push to Docker Hub
docker build -t yourusername/vod-tracker:latest .
docker push yourusername/vod-tracker:latest

# Or deploy with docker-compose
docker-compose up -d
```

### Option 2: Vercel (Frontend) + Railway (Backend)

**Frontend:**
1. Push `frontend/` to GitHub
2. Connect to Vercel
3. Deploy

**Backend:**
1. Push `backend/` to GitHub
2. Connect to Railway
3. Set environment variables
4. Deploy

## 📞 Getting Help

1. Check the troubleshooting section above
2. Check API docs: http://localhost:8000/docs
3. Check logs: `backend/logs/app.log`
4. Open browser DevTools (F12) for frontend errors

## 🎯 Next Steps

- Customize colors and fonts in `frontend/tailwind.config.ts`
- Add your own crosshair detection models in `backend/app/ml_models/`
- Integrate with databases for saving analyses
- Deploy to your own server

## 📝 Notes

- First analysis may be slower as models are loaded
- Processing time depends on video length (roughly 10 min per 30-min video)
- Requires 4GB+ RAM for smooth operation
- Videos are temporarily stored in `/tmp/vod-tracker/`

---

**Enjoy analyzing your Valorant gameplay! 🎮✨**
