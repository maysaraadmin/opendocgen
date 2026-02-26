@echo off
REM OpenDocGen Development Start Script for Windows

echo 🚀 Starting OpenDocGen development environment...

REM Check if .env file exists
if not exist .env (
    echo ⚠️  .env file not found. Running setup first...
    call scripts\setup.bat
)

REM Check if Ollama is running
curl -s http://localhost:11434/api/tags >nul 2>&1
if errorlevel 1 (
    echo ⚠️  Ollama is not running. Starting Ollama...
    ollama serve
    timeout /t 5 >nul
    echo ✅ Ollama started
)

REM Check if default model is available
ollama list | findstr "llama3.2" >nul 2>&1
if errorlevel 1 (
    echo 📥 Downloading default model (llama3.2)...
    ollama pull llama3.2
    echo ✅ Model downloaded
)

REM Start the development server
echo 🌐 Starting development server...
set PYTHONPATH=%PYTHONPATH%;%CD%
set OPENDOCGEN_ENV=development

REM Run the CLI serve command with development settings
opendocgen serve --host 0.0.0.0 --port 8000 --reload --log-level debug
