// Desktopová verze IMP 2: otevře hru v okně (F11 = celá obrazovka, F12 = vývojářské nástroje)
const { app, BrowserWindow } = require('electron');
const path = require('path');

function createWindow() {
  const win = new BrowserWindow({
    width: 1280,
    height: 720,
    backgroundColor: '#000000',
    autoHideMenuBar: true,
    title: 'IMP 2 – Temné patro',
    webPreferences: { backgroundThrottling: false }
  });
  win.loadFile(path.join(__dirname, 'game', 'index.html'));
  win.webContents.on('before-input-event', (e, input) => {
    if (input.type !== 'keyDown') return;
    if (input.key === 'F11') win.setFullScreen(!win.isFullScreen());
    if (input.key === 'F12') win.webContents.toggleDevTools();
  });
}

app.whenReady().then(createWindow);
app.on('window-all-closed', () => app.quit());
