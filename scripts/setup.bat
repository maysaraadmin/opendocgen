@echo off
REM OpenDocGen Setup Script for Windows

echo 🔧 Setting up OpenDocGen environment...

REM Create .env file if it doesn't exist
if not exist .env (
    if exist .env.example (
        copy .env.example .env >nul
        echo ✅ Created .env file from .env.example
    ) else (
        echo ⚠️  .env.example not found, creating basic .env file
        (
            echo # OpenDocGen Environment Configuration
            echo APP_NAME=OpenDocGen
            echo APP_VERSION=0.1.0
            echo DEBUG=false
            echo LOG_LEVEL=INFO
            echo.
            echo # API Configuration
            echo API_HOST=0.0.0.0
            echo API_PORT=8000
            echo.
            echo # LLM Configuration
            echo OLLAMA_BASE_URL=http://localhost:11434
            echo DEFAULT_MODEL=llama2
            echo.
            echo # Search Configuration
            echo SEARXNG_URL=http://localhost:8080
            echo BROWSERLESS_URL=http://localhost:3000
            echo.
            echo # Security
            echo SECRET_KEY=your-secret-key-here-change-in-production
            echo ENABLE_AUTH=false
        ) > .env
        echo ✅ Created basic .env file
    )
) else (
    echo ℹ️  .env file already exists
)

REM Create necessary directories
echo 📁 Creating directories...
if not exist data mkdir data
if not exist data\uploads mkdir data\uploads
if not exist data\downloads mkdir data\downloads
if not exist data\output mkdir data\output
if not exist data\output\documents mkdir data\output\documents
if not exist data\output\drafts mkdir data\output\drafts
if not exist data\output\charts mkdir data\output\charts
if not exist data\output\exports mkdir data\output\exports
if not exist data\cache mkdir data\cache
if not exist data\logs mkdir data\logs
if not exist data\backups mkdir data\backups
if not exist tests\fixtures mkdir tests\fixtures
if not exist tests\fixtures\sample_documents mkdir tests\fixtures\sample_documents
if not exist tests\fixtures\sample_data mkdir tests\fixtures\sample_data
if not exist config mkdir config
if not exist config\prompts mkdir config\prompts
if not exist config\environments mkdir config\environments

REM Create basic config files if they don't exist
if not exist config\config.yaml (
    (
        echo # OpenDocGen Configuration
        echo app:
        echo   name: "OpenDocGen"
        echo   version: "0.1.0"
        echo   debug: false
        echo.
        echo api:
        echo   host: "0.0.0.0"
        echo   port: 8000
        echo.
        echo llm:
        echo   default_model: "llama2"
        echo   ollama_base_url: "http://localhost:11434"
        echo.
        echo agents:
        echo   max_iterations: 50
        echo   timeout: 300
    ) > config\config.yaml
    echo ✅ Created config\config.yaml
)

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed or not in PATH
    pause
    exit /b 1
)

REM Install dependencies if requested
if "%1"=="--install" (
    echo 📦 Installing dependencies...
    pip install -e .
    echo ✅ Dependencies installed
)

echo ✅ Setup complete!
echo.
echo Next steps:
echo 1. Review and update .env file if needed
echo 2. Run 'make dev-install' to install development dependencies
echo 3. Run 'make models' to download AI models
echo 4. Run 'make dev' to start the development server
pause
