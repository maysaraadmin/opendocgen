#!/bin/bash

# OpenDocGen Model Download Script
echo "📥 Downloading AI models for OpenDocGen..."

# Check if Ollama is installed
if ! command -v ollama &> /dev/null; then
    echo "❌ Ollama not found. Please install Ollama first:"
    echo "   curl -fsSL https://ollama.ai/install.sh | sh"
    exit 1
fi

# Check if Ollama is running
if ! curl -s http://localhost:11434/api/tags > /dev/null 2>&1; then
    echo "🚀 Starting Ollama..."
    ollama serve &
    sleep 5
fi

# List of models to download
models=(
    "llama3.2"
    "mistral"
    "codellama"
    "nomic-embed-text"
)

echo "📋 Models to download:"
for model in "${models[@]}"; do
    echo "  - $model"
done

echo ""
echo "⬇️  Starting downloads..."

# Download each model
for model in "${models[@]}"; do
    echo "📥 Downloading $model..."
    if ollama pull "$model"; then
        echo "✅ $model downloaded successfully"
    else
        echo "❌ Failed to download $model"
    fi
done

# Show available models
echo ""
echo "📋 Available models:"
ollama list

echo ""
echo "✅ Model download complete!"
echo ""
echo "You can now use these models with OpenDocGen:"
echo "  opendocgen generate --model llama3.2 \"Your topic here\""
