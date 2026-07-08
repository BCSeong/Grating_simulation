@echo off
echo ============================================
echo  Grating Simulator - EXE Build (with torch)
echo ============================================
echo.

cd /d "%~dp0"

if not exist "venv\Scripts\python.exe" (
    echo [ERROR] Virtual environment not found.
    echo Please run 'install.bat' first.
    pause
    exit /b 1
)

echo [1/4] Installing PyInstaller...
venv\Scripts\pip.exe install pyinstaller
if errorlevel 1 (
    echo [ERROR] Failed to install PyInstaller.
    pause
    exit /b 1
)

echo.
echo [2/4] Installing CPU-only torch (keeps build size small)...
echo   NOTE: This replaces any existing torch installation in venv.
echo   To restore CUDA torch later, run:
echo     venv\Scripts\pip install torch torchvision --index-url https://download.pytorch.org/whl/cu128
echo.
venv\Scripts\pip.exe install torch torchvision --index-url https://download.pytorch.org/whl/cpu
if errorlevel 1 (
    echo [ERROR] Failed to install CPU-only torch.
    pause
    exit /b 1
)

echo.
echo [3/4] Building EXE (onedir mode, with CPU torch)...
venv\Scripts\pyinstaller.exe --name "GratingSimulator" --windowed --onedir ^
    --exclude-module torchaudio ^
    --exclude-module tkinter ^
    --noconfirm ^
    run.py

if errorlevel 1 (
    echo [ERROR] Build failed. See above for details.
    pause
    exit /b 1
)

echo.
echo ============================================
echo  [4/4] Build complete!
echo  Output: dist\GratingSimulator\GratingSimulator.exe
echo ============================================
echo.
echo You can distribute the entire 'dist\GratingSimulator' folder.
echo Scheimpflug simulator will use torch CPU (no GPU acceleration).
echo.
pause
