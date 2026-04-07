@echo off
echo ===== Starting Stock Dashboard Setup =====

:: Go to backend
cd /d "%~dp0backend"

echo --- Seeding Database ---
if exist venv\Scripts\activate.bat (
    call venv\Scripts\activate.bat
)
python -m app.seed

echo --- Starting Backend Server ---
start cmd /k "if exist venv\Scripts\activate.bat (call venv\Scripts\activate.bat) & python -m uvicorn app.main:app --reload"

:: Go to frontend
cd /d "%~dp0frontend"

:: Install dependencies if not installed
if not exist "node_modules" (
    echo --- Installing Frontend Dependencies ---
    call npm install
    call npm install axios chart.js react-chartjs-2
)

echo --- Starting Frontend ---
start cmd /k "npm start"

echo ===== Stock Dashboard Running! =====
