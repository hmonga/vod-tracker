# 🎮 Valorant Crosshair Analyzer - Windows Installer Guide

Your app is now available as a downloadable Windows installer (.exe)! No command line needed.

## 📥 Download & Install

### Step 1: Download the Installer

You have **2 options**:

#### Option A: Download from GitHub Releases (Recommended)
1. Go to: https://github.com/yourname/vod-tracker/releases
2. Find the latest release
3. Download: `Vod-Tracker-Setup-1.0.0.exe` (~150-200MB)

#### Option B: Download Pre-built Installer
- Latest build available in GitHub Artifacts
- Go to Actions → Latest workflow run → "latest-installer" artifact

### Step 2: Run the Installer

1. **Double-click** `Vod-Tracker-Setup-1.0.0.exe`
2. Windows may show security warning → Click **"More info"** → **"Run anyway"**
3. Follow the installation wizard:
   - Choose installation location (default: `C:\Program Files\Vod Tracker`)
   - Create Start Menu shortcuts
   - Create Desktop shortcut (optional)
4. Click **"Finish"** when done

### Step 3: Launch the App

**Choose one:**

- **Double-click** the Desktop shortcut
- **Start Menu** → Search "Vod Tracker" → Click it
- **Program Files** → Vod Tracker folder → Run executable

The app will launch automatically and open a window.

## ✅ What Happens Next

1. **Backend starts** automatically (runs in background)
2. **Frontend loads** in the app window
3. **You see the home page** with upload option
4. Ready to analyze!

## 🎯 Using the App

1. Click **"Upload Video"**
2. **Drag and drop** your Valorant video OR click to browse
3. **Wait** for analysis (progress shows in real-time)
4. **View results** with detailed breakdown
5. **Download report** as PDF or JSON

## 🛑 Troubleshooting

### App won't start
```
→ Check: Windows Defender might have blocked it
  - Go to Security & run anyway
→ Try: Restart your computer
→ Check: You have 4GB+ RAM available
```

### "Backend not responding" error
```
→ The backend service is embedded in the .exe
→ If error persists, reinstall the app
→ Clear temp files: Delete %AppData%\Vod Tracker
```

### Installer won't run
```
→ Disable antivirus temporarily
→ Run as Administrator (right-click → Run as administrator)
→ Download from GitHub again (might be corrupted)
```

### Can't upload video
```
→ Ensure video is: .mp4, .mov, .webm, .avi, or .mkv
→ Check file size (max 2GB)
→ Check disk space (need at least 1GB free)
```

## 📂 Where Files are Stored

- **Installation**: `C:\Program Files\Vod Tracker`
- **User data**: `%AppData%\Vod Tracker`
- **Temp files**: `%AppData%\Vod Tracker\temp`
- **Logs**: `%AppData%\Vod Tracker\logs`

## 🔧 Uninstall

1. **Control Panel** → **Programs and Features**
2. Find **"Vod Tracker"**
3. Click **"Uninstall"**
4. Follow wizard
5. Done!

Or use: **Settings** → **Apps** → **Apps & features** → Search "Vod Tracker" → Uninstall

## 🚀 Advanced: Build Your Own Installer

If you want to rebuild the installer:

```bash
# On Windows (in project root):
build-installer.bat
```

Output: `frontend\dist\Vod Tracker Setup 1.0.0.exe`

Or manually:
```bash
cd frontend
npm install
npm run build:desktop
```

## 📱 Requirements

- **OS**: Windows 10 or later (64-bit or 32-bit)
- **RAM**: 4GB minimum (8GB recommended)
- **Disk**: 500MB free (for installation + temp files)
- **Internet**: Required for initial setup only

## 🔒 Security & Privacy

- ✅ App runs locally on your PC
- ✅ Videos are analyzed on your machine
- ✅ No cloud upload by default
- ✅ No personal data collection
- ✅ Backend is embedded, no external services

## 💻 System Integration

The installer includes:
- ✅ Desktop shortcut
- ✅ Start Menu entry
- ✅ Uninstall support
- ✅ System PATH updates
- ✅ Quick launch support

## 📊 Version Updates

When new versions are released:
1. Download the new `.exe` installer
2. Run it (new version will replace old)
3. Or use built-in update checker (coming soon)

## 🆘 Still Having Issues?

1. Check logs: `%AppData%\Vod Tracker\logs\app.log`
2. Try uninstall → reinstall
3. Make sure antivirus/firewall allows the app
4. Report issue on GitHub with logs attached

## 🎮 You're All Set!

Just download, install, and run. That's it! 

Enjoy analyzing your Valorant crosshair placement! 🎯✨

---

**Need Help?** Visit: https://github.com/yourname/vod-tracker/issues
