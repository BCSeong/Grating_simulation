@echo off
echo ============================================
echo  Grating Simulator - EXE Build
echo ============================================
echo.

cd /d "%~dp0"

if not exist "venv\Scripts\python.exe" (
    echo [ERROR] Virtual environment not found.
    echo Please run 'install.bat' first.
    pause
    exit /b 1
)

echo [1/3] Installing PyInstaller...
venv\Scripts\pip.exe install pyinstaller
if errorlevel 1 (
    echo [ERROR] Failed to install PyInstaller.
    pause
    exit /b 1
)

echo.
echo [2/3] Building EXE (onedir mode)...
venv\Scripts\pyinstaller.exe --name "GratingSimulator" --windowed --onedir ^
    --exclude-module torch ^
    --exclude-module torchvision ^
    --exclude-module torchaudio ^
    --noconfirm ^
    run.py

if errorlevel 1 (
    echo [ERROR] Build failed. See above for details.
    pause
    exit /b 1
)

echo.
echo ============================================
echo  [3/3] Build complete!
echo  Output: dist\GratingSimulator\GratingSimulator.exe
echo ============================================
echo.
echo You can distribute the entire 'dist\GratingSimulator' folder.
echo.
pause
