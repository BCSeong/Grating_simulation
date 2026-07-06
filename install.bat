@echo off
echo ============================================
echo  Grating Simulator - Environment Setup
echo ============================================
echo.

where python >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not found in PATH.
    echo Please install Python 3.9+ and add it to PATH.
    pause
    exit /b 1
)

echo [1/3] Creating virtual environment...
python -m venv venv
if errorlevel 1 (
    echo [ERROR] Failed to create virtual environment.
    pause
    exit /b 1
)

echo [2/3] Activating virtual environment...
call venv\Scripts\activate.bat

echo [3/4] Installing dependencies...
pip install -r requirements.txt
if errorlevel 1 (
    echo [ERROR] Failed to install dependencies.
    pause
    exit /b 1
)

echo.
echo [4/4] PyTorch (GPU acceleration, optional)
echo.
echo Do you want to install PyTorch with CUDA support?
echo   1) Yes - install PyTorch with CUDA 12.8
echo   2) Yes - install PyTorch CPU-only
echo   3) Skip (Scheimpflug pipeline will use numpy fallback)
echo.
set /p TORCH_CHOICE="Enter choice (1/2/3): "

if "%TORCH_CHOICE%"=="1" (
    echo Installing PyTorch with CUDA 12.8...
    pip install torch torchvision --index-url https://download.pytorch.org/whl/cu128
) else if "%TORCH_CHOICE%"=="2" (
    echo Installing PyTorch CPU-only...
    pip install torch torchvision --index-url https://download.pytorch.org/whl/cpu
) else (
    echo Skipping PyTorch installation.
)

echo.
echo ============================================
echo  Setup complete!
echo  Run 'run.bat' to start the application.
echo ============================================
pause
