const { app, BrowserWindow, Menu, ipcMain } = require('electron');
const { spawn } = require('child_process');
const path = require('path');
const isDev = require('electron-is-dev');

let mainWindow;
let backendProcess;

// Start backend server
function startBackendServer() {
  return new Promise((resolve, reject) => {
    try {
      if (isDev) {
        // In development, backend runs separately
        console.log('Development mode: Ensure backend is running on port 8000');
        setTimeout(() => resolve(), 1000);
      } else {
        // In production, start embedded backend
        const backendPath = path.join(__dirname, '..', '..', 'backend', 'main.py');
        console.log('Starting backend:', backendPath);
        
        backendProcess = spawn('python', [backendPath], {
          stdio: 'pipe',
          detached: false,
        });

        backendProcess.stdout.on('data', (data) => {
          console.log(`[Backend] ${data}`);
        });

        backendProcess.stderr.on('data', (data) => {
          console.error(`[Backend Error] ${data}`);
        });

        backendProcess.on('error', (err) => {
          console.error('Failed to start backend:', err);
          reject(err);
        });

        // Give backend time to start
        setTimeout(() => resolve(), 3000);
      }
    } catch (error) {
      console.error('Error starting backend:', error);
      reject(error);
    }
  });
}

function createWindow() {
  mainWindow = new BrowserWindow({
    width: 1400,
    height: 900,
    minWidth: 800,
    minHeight: 600,
    webPreferences: {
      nodeIntegration: false,
      contextIsolation: true,
      preload: path.join(__dirname, 'preload.js'),
    },
    icon: path.join(__dirname, 'assets/icon.png'),
  });

  const startUrl = isDev
    ? 'http://localhost:3000'
    : `file://${path.join(__dirname, '../out/index.html')}`;

  mainWindow.loadURL(startUrl);

  if (isDev) {
    mainWindow.webContents.openDevTools();
  }

  mainWindow.on('closed', () => {
    mainWindow = null;
  });
}

app.on('ready', async () => {
  try {
    await startBackendServer();
    createWindow();
  } catch (error) {
    console.error('Failed to start app:', error);
    app.quit();
  }
});

app.on('window-all-closed', () => {
  // Kill backend process
  if (backendProcess) {
    backendProcess.kill();
  }
  if (process.platform !== 'darwin') {
    app.quit();
  }
});

app.on('activate', () => {
  if (mainWindow === null) {
    createWindow();
  }
});

// IPC Handlers
ipcMain.handle('get-app-version', () => app.getVersion());
ipcMain.handle('get-app-path', () => app.getAppPath());

// Menu
const template = [
  {
    label: 'File',
    submenu: [
      {
        label: 'Exit',
        accelerator: 'CmdOrCtrl+Q',
        click: () => {
          if (backendProcess) {
            backendProcess.kill();
          }
          app.quit();
        },
      },
    ],
  },
  {
    label: 'Edit',
    submenu: [
      { role: 'undo' },
      { role: 'redo' },
      { type: 'separator' },
      { role: 'cut' },
      { role: 'copy' },
      { role: 'paste' },
    ],
  },
  {
    label: 'View',
    submenu: [
      { role: 'reload' },
      { role: 'forceReload' },
      { role: 'toggleDevTools' },
      { type: 'separator' },
      { role: 'resetZoom' },
      { role: 'zoomIn' },
      { role: 'zoomOut' },
    ],
  },
  {
    label: 'Help',
    submenu: [
      {
        label: 'About Vod Tracker',
        click: () => {
          console.log('Valorant Crosshair Analyzer v1.0.0');
        },
      },
      {
        label: 'Documentation',
        click: () => {
          require('electron').shell.openExternal('https://github.com/yourname/vod-tracker');
        },
      },
    ],
  },
];

const menu = Menu.buildFromTemplate(template);
Menu.setApplicationMenu(menu);

