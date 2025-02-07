const { app, BrowserWindow, protocol, shell } = require('electron');
const path = require('path');
const express = require('express');
const cors = require('cors');
const bodyParser = require('body-parser');
require('dotenv').config({ path: path.resolve(__dirname, '../backend/.env') });

let mainWindow;
let isDev;
const expressApp = express();
const PORT = process.env.PORT || 5000;
let deepLinkUrl = null; // Simpan URL dari deep link jika aplikasi belum terbuka

// Registrasi protokol app://
app.setAsDefaultProtocolClient('app');

// Middleware Express
expressApp.use(cors({
  origin: ['http://localhost:3000', 'app://'],
  credentials: true,
}));
expressApp.use(bodyParser.json());
expressApp.use('/api', require(path.resolve(__dirname, '../backend/routes/auth')));

// Registrasi skema protokol
protocol.registerSchemesAsPrivileged([
  {
    scheme: 'app',
    privileges: {
      standard: true,
      secure: true,
      allowServiceWorkers: true,
      supportFetchAPI: true,
      corsEnabled: true
    },
  },
]);

// Dynamic Import untuk electron-is-dev
(async () => {
  try {
    const { default: isDevImported } = await import('electron-is-dev');
    isDev = isDevImported;
    app.whenReady().then(createWindow);
  } catch (err) {
    console.error('Error importing electron-is-dev:', err);
    isDev = false;
    app.whenReady().then(createWindow);
  }
})();

function createWindow() {
  mainWindow = new BrowserWindow({
    width: 1200,
    height: 800,
    webPreferences: {
      nodeIntegration: true,
      contextIsolation: false,
      enableRemoteModule: true,
    },
  });

  mainWindow.webContents.openDevTools(); // Buka DevTools secara otomatis

  // Modifikasi register protokol
  protocol.registerFileProtocol('app', (request, callback) => {
    const url = request.url.substr(6); // Hapus 'app://' dari URL
    const decodedUrl = decodeURI(url);
    
    if (decodedUrl.includes('reset-password')) {
      // Jika URL adalah reset password, arahkan ke halaman reset password
      const token = decodedUrl.split('reset-password/')[1];
      const finalUrl = path.join(__dirname, '../build/index.html');
      callback({ path: finalUrl });
      
      // Setelah window load, redirect ke route yang tepat
      mainWindow.webContents.once('did-finish-load', () => {
        mainWindow.webContents.executeJavaScript(`
          window.location.hash = '/reset-password/${token}';
        `);
      });
    } else {
      // Untuk URL lain, tangani seperti biasa
      const filePath = path.join(__dirname, '../build', decodedUrl);
      callback({ path: filePath });
    }
  });

  // Load aplikasi
  const startUrl = isDev
    ? 'http://localhost:3000'
    : `file://${path.join(__dirname, '../build/index.html')}`;

  mainWindow.loadURL(startUrl);

  // Jika ada deep linking yang tertunda, muat setelah window siap
  if (deepLinkUrl) {
    handleDeepLink(deepLinkUrl);
  }

  // Setup handler untuk membuka link
  mainWindow.webContents.setWindowOpenHandler(({ url }) => {
    if (url.startsWith('app://')) {
      return { action: 'allow' };
    } else {
      shell.openExternal(url);
      return { action: 'deny' };
    }
  });

  // Handle navigasi untuk app://
  mainWindow.webContents.on('will-navigate', (event, url) => {
    if (url.startsWith('app://')) {
      event.preventDefault();
      mainWindow.loadURL(url);
    }
  });

  // Jalankan server Express
  const server = expressApp.listen(PORT, () => {
    console.log(`Server berjalan di port ${PORT}`);
  });

  mainWindow.on('closed', () => {
    server.close();
    mainWindow = null;
  });
}

// Fungsi untuk menangani deep link
function handleDeepLink(url) {
  if (!url || !url.includes('reset-password')) return;
  
  const token = url.split('reset-password/')[1];
  if (!token) return;

  // Pastikan window sudah siap sebelum navigasi
  if (!mainWindow || !mainWindow.webContents.isLoading()) {
    mainWindow.webContents.executeJavaScript(`
      window.location.hash = '/reset-password/${token}';
    `);
  } else {
    mainWindow.webContents.once('did-finish-load', () => {
      mainWindow.webContents.executeJavaScript(`
        window.location.hash = '/reset-password/${token}';
      `);
    });
  }
}

// Handle deep linking saat aplikasi sedang berjalan
app.on('open-url', (event, url) => {
  event.preventDefault();
  console.log('Received deep link:', url);
  if (mainWindow) {
    mainWindow.loadURL(url);
  } else {
    deepLinkUrl = url; // Simpan URL untuk dibuka nanti
  }
});

// Event handler untuk Windows deep linking
if (process.platform === 'win32') {
  // Handle deep linking saat aplikasi sudah berjalan
  app.on('second-instance', (event, argv) => {
    if (mainWindow) {
      const deepLink = argv.find(arg => arg.startsWith('app://'));
      if (deepLink) {
        handleDeepLink(deepLink);
        mainWindow.focus();
      }
    }
  });

  // Handle deep linking saat aplikasi pertama kali dibuka
  const gotTheLock = app.requestSingleInstanceLock();
  if (!gotTheLock) {
    app.quit();
  } else {
    app.on('ready', () => {
      const deepLink = process.argv.find(arg => arg.startsWith('app://'));
      if (deepLink) {
        deepLinkUrl = deepLink;
      }
    });
  }
}

// Event handlers lainnya
app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') {
    app.quit();
  }
});

app.on('activate', () => {
  if (mainWindow === null) {
    createWindow();
  }
});

// Error handling
process.on('uncaughtException', (err) => {
  console.error('Uncaught Exception:', err);
});

process.on('unhandledRejection', (reason, promise) => {
  console.error('Unhandled Rejection at:', promise, 'reason:', reason);
});