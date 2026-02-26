FROM ollama/ollama:latest

# Install additional tools
RUN apt-get update && apt-get install -y \
    curl \
    wget \
    && rm -rf /var/lib/apt/lists/*

# Create a directory for models
RUN mkdir -p /root/.ollama

# Expose the port
EXPOSE 11434

# Set environment variables
ENV OLLAMA_HOST=0.0.0.0

# Start Ollama server
CMD ["ollama", "serve"]
