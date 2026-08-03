# 🚀 GitHub Release & Installer Setup

This guide shows how to set up GitHub releases so your app is automatically distributed as a `.exe` installer.

## 📋 Prerequisites

- GitHub account
- Project pushed to GitHub
- GitHub Actions enabled (default)

## 🔧 Setup Steps

### Step 1: Create a GitHub Personal Access Token

1. Go to: https://github.com/settings/tokens
2. Click **"Generate new token"** → **"Generate new token (classic)"**
3. Give it a name: `GITHUB_TOKEN`
4. Check these permissions:
   - `repo` (full control of private repos)
   - `workflow` (Update GitHub Actions)
5. Click **"Generate token"**
6. **Copy the token** (you'll only see it once!)

### Step 2: Add Token to Your Repository

1. Go to your repo: https://github.com/yourname/vod-tracker
2. **Settings** → **Secrets and variables** → **Actions**
3. Click **"New repository secret"**
4. Name: `GITHUB_TOKEN`
5. Paste the token you copied
6. Click **"Add secret"**

### Step 3: Update Workflow File

The workflow file is already created at `.github/workflows/build-release.yml`

Edit it and make sure your repo URL is correct:

```yaml
# Check these match your GitHub username/repo:
# https://github.com/YOUR_USERNAME/vod-tracker
```

### Step 4: Push to GitHub

```bash
git add .
git commit -m "Add Electron installer and GitHub Actions workflow"
git push origin main
```

### Step 5: Watch the Build

1. Go to your repo: https://github.com/yourname/vod-tracker
2. Click **"Actions"** tab
3. See the workflow running
4. Wait for **"Build and Release Installer"** to complete
5. Once done, artifacts available under the workflow run

## 📦 Create a Release

### Option A: GitHub Releases (Recommended for Users)

1. Go to: https://github.com/yourname/vod-tracker/releases
2. Click **"Create a new release"**
3. Set tag: `v1.0.0`
4. Title: `Vod Tracker v1.0.0`
5. Description:
   ```
   Download the installer (.exe) below to install on Windows.
   
   ### What's New
   - Initial release
   - Full crosshair analysis
   - Modern UI
   - Real-time progress tracking
   
   ### Installation
   1. Download: `Vod-Tracker-Setup-1.0.0.exe`
   2. Double-click to install
   3. Follow wizard
   4. Launch from Start Menu
   ```
6. Click **"Publish release"**
7. Workflow triggers automatically → Builds installer
8. Installer uploaded to release page

### Option B: Automatic Builds on Push

Every time you push to `main` branch:
1. Workflow builds automatically
2. Installer available in Artifacts
3. Latest available for download

## 🎯 Users Download Process

### For Your Users:

1. Go to: **https://github.com/yourname/vod-tracker/releases**
2. Find latest release
3. Download `.exe` file
4. Double-click to install
5. Done!

## 🔄 Update Process

When you make changes:

```bash
# Make changes
git add .
git commit -m "Your changes"
git push origin main
```

Then:

```bash
# Create new release
git tag v1.0.1
git push origin v1.0.1
```

GitHub Actions automatically:
1. ✅ Builds new installer
2. ✅ Tests it
3. ✅ Uploads to release

## ⚙️ Customize Build

Edit `.github/workflows/build-release.yml` to change:

- Build triggers
- Publishing behavior
- Artifact retention
- Release drafts
- Pre-releases

## 🆘 Troubleshooting

### Build fails
- Check: Node.js version in workflow (should be 18)
- Check: All files committed to git
- Look at: Actions → workflow run → logs

### Can't find installer
- Go to: https://github.com/yourname/vod-tracker/actions
- Find the workflow run
- Look for "Artifacts" section
- Download from there

### Token not working
- Regenerate token in GitHub Settings
- Update in repo secrets
- Retry the build

## 📊 Distribution Options

### Option 1: GitHub Releases (Free)
✅ Recommended - users download directly
✅ Free
✅ Automatic updates easy to track

### Option 2: SourceForge (Free)
- Upload to SourceForge
- Get more download statistics
- Need SourceForge account

### Option 3: Your Website
- Upload `.exe` to your site
- Link from README

## 📝 README Update

Update your README.md to include:

```markdown
## Download (Windows)

**Latest Version: 1.0.0**

### Installation
1. [Download Installer](https://github.com/yourname/vod-tracker/releases)
2. Run the `.exe` file
3. Follow installation wizard
4. Launch from Start Menu

See [INSTALLER_GUIDE.md](INSTALLER_GUIDE.md) for detailed instructions.
```

## 🎉 You're Done!

Your app is now available for download as a professional Windows installer!

### What Happens Next:
1. ✅ Users download `.exe`
2. ✅ They install it like any other app
3. ✅ App runs with embedded backend
4. ✅ No technical knowledge needed!

---

## 📚 Advanced: Customize Installer

Edit `frontend/package.json` build config to:

- Change app name
- Change icon
- Add auto-updates
- Set installation paths
- Add registry entries

See the `"build"` section in `package.json`

---

**Your app is ready for distribution! 🚀**
