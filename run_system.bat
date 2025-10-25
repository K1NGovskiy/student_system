@echo off
chcp 65001 >nul
title Student Performance Management System
echo ============================================
echo   STUDENT PERFORMANCE SYSTEM LAUNCHER
echo ============================================

:: Check Python installation
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python not found! Please install Python 3.10+.
    pause
    exit /b
)

:: Start backend server
echo.
echo [1/3] Starting FastAPI backend...
start cmd /k "python main.py"

:: Small delay to let backend start
timeout /t 3 >nul

:: Start frontend HTTP server
echo.
echo [2/3] Starting frontend server on port 8080...
cd frontend
start cmd /k "python -m http.server 8080"

:: Open browser
timeout /t 2 >nul
echo [3/3] Opening system in browser...
start http://localhost:8080/index.html

echo.
echo ============================================
echo System started successfully!
echo You can now use the web interface.
echo Close both windows to stop the system.
echo ============================================
pause
exit
