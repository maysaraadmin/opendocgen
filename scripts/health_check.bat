@echo off
REM OpenDocGen Health Check Script for Windows

echo 🏥 Checking OpenDocGen service health...

REM Check if Docker is running
docker info >nul 2>&1
if errorlevel 1 (
    echo ❌ Docker is not running
    pause
    exit /b 1
)

REM Check OpenDocGen API
echo 🔍 Checking OpenDocGen API...
curl -s -o nul -w "%%{http_code}" http://localhost:8000/health | findstr "200" >nul
if errorlevel 1 (
    echo ❌ OpenDocGen API is unhealthy
) else (
    echo ✅ OpenDocGen API is healthy
)

REM Check Ollama
echo 🔍 Checking Ollama port 11434...
netstat -an | findstr ":11434" >nul
if errorlevel 1 (
    echo ❌ Ollama port is closed
) else (
    echo ✅ Ollama port is open
)

REM Check SearXNG (optional)
echo 🔍 Checking SearXNG...
curl -s -o nul -w "%%{http_code}" http://localhost:8080 >nul
if errorlevel 1 (
    echo ⚠️  SearXNG not running ^(optional^)
) else (
    echo ✅ SearXNG is running
)

REM Check Browserless (optional)
echo 🔍 Checking Browserless port 3000...
netstat -an | findstr ":3000" >nul
if errorlevel 1 (
    echo ⚠️  Browserless not running ^(optional^)
) else (
    echo ✅ Browserless port is open
)

REM Check ChromaDB (optional)
echo 🔍 Checking ChromaDB port 8001...
netstat -an | findstr ":8001" >nul
if errorlevel 1 (
    echo ⚠️  ChromaDB not running ^(optional^)
) else (
    echo ✅ ChromaDB port is open
)

echo.
echo 📊 Health Check Complete!
echo.
echo 🌐 Access points:
echo    - OpenDocGen API: http://localhost:8000
echo    - API Docs: http://localhost:8000/docs
echo    - Ollama: http://localhost:11434
echo.
echo 🔧 Troubleshooting:
echo    - Run 'make docker-logs' to check service logs
echo    - Run 'make docker-down && make docker-up' to restart services
pause
