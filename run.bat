@echo off
echo Starting Smart Examination Platform...
npm run dev
if %ERRORLEVEL% neq 0 (
    echo.
    echo ❌ The application failed to start or was stopped with an error.
    pause
)
