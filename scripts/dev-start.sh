#!/bin/bash

# OpenDocGen Development Start Script
echo "🚀 Starting OpenDocGen development environment..."

# Check if .env file exists
if [ ! -f .env ]; then
    echo "⚠️  .env file not found. Running setup first..."
    ./scripts/setup.sh
fi

# Check if Ollama is running
if ! curl -s http://localhost:11434/api/tags > /dev/null 2>&1; then
    echo "⚠️  Ollama is not running. Starting Ollama..."
    if command -v ollama &> /dev/null; then
        ollama serve &
        sleep 5
        echo "✅ Ollama started"
    else
        echo "❌ Ollama not found. Please install Ollama first:"
        echo "   curl -fsSL https://ollama.ai/install.sh | sh"
        exit 1
    fi
fi

# Check if default model is available
if ! ollama list | grep -q "llama3.2"; then
    echo "📥 Downloading default model (llama3.2)..."
    ollama pull llama3.2
    echo "✅ Model downloaded"
fi

# Start the development server
echo "🌐 Starting development server..."
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
export OPENDOCGEN_ENV=development

# Run the CLI serve command with development settings
opendocgen serve --host 0.0.0.0 --port 8000 --reload --log-level debug
