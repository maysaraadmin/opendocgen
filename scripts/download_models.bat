@echo off
REM OpenDocGen Model Download Script for Windows

echo 📥 Downloading AI models for OpenDocGen...

REM Check if Ollama is installed
ollama --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Ollama not found. Please install Ollama first:
    echo    iwr -useb https://ollama.ai/install.sh | iex
    pause
    exit /b 1
)

REM Check if Ollama is running
curl -s http://localhost:11434/api/tags >nul 2>&1
if errorlevel 1 (
    echo 🚀 Starting Ollama...
    start /b ollama serve
    timeout /t 5 >nul
)

REM Download models
echo 📥 Downloading llama3.2...
ollama pull llama3.2
if errorlevel 1 (
    echo ❌ Failed to download llama3.2
) else (
    echo ✅ llama3.2 downloaded successfully
)

echo 📥 Downloading mistral...
ollama pull mistral
if errorlevel 1 (
    echo ❌ Failed to download mistral
) else (
    echo ✅ mistral downloaded successfully
)

echo 📥 Downloading codellama...
ollama pull codellama
if errorlevel 1 (
    echo ❌ Failed to download codellama
) else (
    echo ✅ codellama downloaded successfully
)

echo 📥 Downloading nomic-embed-text...
ollama pull nomic-embed-text
if errorlevel 1 (
    echo ❌ Failed to download nomic-embed-text
) else (
    echo ✅ nomic-embed-text downloaded successfully
)

REM Show available models
echo.
echo 📋 Available models:
ollama list

echo.
echo ✅ Model download complete!
echo.
echo You can now use these models with OpenDocGen:
echo   opendocgen generate --model llama3.2 "Your topic here"
pause
