@echo off
echo Starting Smart Examination Platform...

echo.
echo =========================================
echo Starting Backend (FastAPI)...
echo =========================================

:: Check if virtual environment exists, if not create it
if not exist "venv\Scripts\activate.bat" (
    echo Creating Python virtual environment...
    python -m venv venv
)

:: Install requirements and start backend in a new window
echo Starting backend server in a new window...
start "Smart Exam - Backend" cmd /k "venv\Scripts\activate.bat && pip install -r requirements.txt && python main.py"

echo.
echo =========================================
echo Starting Frontend (React)...
echo =========================================

:: Install node modules and start frontend in a new window
echo Starting frontend server in a new window...
start "Smart Exam - Frontend" cmd /k "npm install && npm run dev"

echo.
echo Servers are starting up! 
echo Two new terminal windows have been opened.
echo You can close this window now.
pause
