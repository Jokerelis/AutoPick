@echo off
setlocal
cd /d "%~dp0"

if not exist ".venv\Scripts\python.exe" (
    echo ERROR: Python virtual environment not found.
    echo Run: py -m venv .venv
    exit /b 1
)

if not exist ".env" (
    echo ERROR: .env file not found. Copy .env.example to .env and configure it.
    exit /b 1
)

if not exist "frontend\node_modules" (
    echo ERROR: Frontend dependencies not found.
    echo Run: cd frontend ^&^& npm install
    exit /b 1
)

if not exist "autopick.db" (
    echo Creating demo database...
    .venv\Scripts\python.exe -m app.seed
    if errorlevel 1 (
        echo ERROR: Database initialization failed.
        exit /b 1
    )
)

start "AutoPick API" cmd /k ".venv\Scripts\python.exe -m uvicorn app.main:app --reload"
start "AutoPick Frontend" /D "%~dp0frontend" cmd /k "npm run dev"

echo AutoPick started in two terminal windows.
echo Frontend: http://localhost:5173
echo API docs: http://127.0.0.1:8000/docs
