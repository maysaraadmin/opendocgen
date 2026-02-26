#!/bin/bash

# OpenDocGen Setup Script
echo "🔧 Setting up OpenDocGen environment..."

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    if [ -f .env.example ]; then
        cp .env.example .env
        echo "✅ Created .env file from .env.example"
    else
        echo "⚠️  .env.example not found, creating basic .env file"
        cat > .env << EOF
# OpenDocGen Environment Configuration
APP_NAME=OpenDocGen
APP_VERSION=0.1.0
DEBUG=false
LOG_LEVEL=INFO

# API Configuration
API_HOST=0.0.0.0
API_PORT=8000

# LLM Configuration
OLLAMA_BASE_URL=http://localhost:11434
DEFAULT_MODEL=llama2

# Search Configuration
SEARXNG_URL=http://localhost:8080
BROWSERLESS_URL=http://localhost:3000

# Security
SECRET_KEY=your-secret-key-here-change-in-production
ENABLE_AUTH=false
EOF
        echo "✅ Created basic .env file"
    fi
else
    echo "ℹ️  .env file already exists"
fi

# Create necessary directories
echo "📁 Creating directories..."
mkdir -p data/uploads data/downloads data/output data/cache data/logs data/backups
mkdir -p data/output/documents data/output/drafts data/output/charts data/output/exports
mkdir -p tests/fixtures/sample_documents tests/fixtures/sample_data

# Create config directory if it doesn't exist
mkdir -p config/prompts config/environments

# Create basic config files if they don't exist
if [ ! -f config/config.yaml ]; then
    cat > config/config.yaml << EOF
# OpenDocGen Configuration
app:
  name: "OpenDocGen"
  version: "0.1.0"
  debug: false

api:
  host: "0.0.0.0"
  port: 8000

llm:
  default_model: "llama2"
  ollama_base_url: "http://localhost:11434"

agents:
  max_iterations: 50
  timeout: 300
EOF
    echo "✅ Created config/config.yaml"
fi

# Check if Python is available
if ! command -v python3 &> /dev/null && ! command -v python &> /dev/null; then
    echo "❌ Python is not installed or not in PATH"
    exit 1
fi

# Install dependencies if not already installed
if [ "$1" = "--install" ]; then
    echo "📦 Installing dependencies..."
    pip install -e .
    echo "✅ Dependencies installed"
fi

echo "✅ Setup complete!"
echo ""
echo "Next steps:"
echo "1. Review and update .env file if needed"
echo "2. Run 'make dev-install' to install development dependencies"
echo "3. Run 'make models' to download AI models"
echo "4. Run 'make dev' to start the development server"
