# Docker Image Versions

This document specifies the exact versions of Docker images used in OpenDocGen to ensure reproducible builds.

## Core Application Images

| Service | Image | Version | Status |
|---------|-------|---------|---------|
| **OpenDocGen** | python | 3.11-slim | ✅ Already downloaded |
| **Ollama** | ollama/ollama | latest | ✅ Already downloaded (8.99GB) |
| **SearXNG** | searxng/searxng | latest | ✅ Downloaded (377MB) |
| **Browserless** | browserless/chrome | latest | ✅ Downloaded (4.51GB) |
| **ChromaDB** | chromadb/chroma | latest | ✅ Already downloaded (805MB) |
| **Redis** | redis | 7-alpine | ✅ Already downloaded (61.2MB) |

## Currently Available Images

From your local Docker registry:
- ✅ `ollama/ollama:latest` - 8.99GB (Large LLM server)
- ✅ `chromadb/chroma:latest` - 805MB (Vector database)
- ✅ `redis:7-alpine` - 61.2MB (Caching)
- ✅ `python:3.11-slim` - 188MB (Application runtime)
- ✅ `searxng/searxng:latest` - 377MB (Search engine)
- ✅ `browserless/chrome:latest` - 4.51GB (Browser automation)

## All Images Ready! 🎉

All required Docker images are now downloaded and ready to use. No additional downloads needed.

## Total Download Summary

**Downloaded just now:**
- **SearXNG**: 377MB
- **Browserless**: 4.51GB

**Previously available:**
- **Ollama**: 8.99GB
- **ChromaDB**: 805MB
- **Redis**: 61.2MB
- **Python**: 188MB

**Total local storage**: ~15GB of Docker images

## Ready to Start

You can now start OpenDocGen immediately:
```bash
# Start all services
docker-compose -f docker/docker-compose.yml up -d

# Or start development setup
docker-compose -f docker/docker-compose.dev.yml up -d

# Or start GPU-enabled setup
docker-compose -f docker/docker-compose.gpu.yml up -d
```

## GPU Support Images

| Service | Base Image | CUDA Version | Status |
|---------|------------|--------------|---------|
| **OpenDocGen GPU** | nvidia/cuda | 12.1.1-runtime | ⬇️ Need to download |
| **Ollama GPU** | nvidia/cuda | 12.1.1-runtime | ⬇️ Need to download |

## Fast Start Commands

Since you already have most images, you can start quickly:

```bash
# Download only the missing images
docker pull searxng/searxng:latest
docker pull browserless/chrome:2.2.2

# Start the services (no need to pull existing images)
docker-compose -f docker/docker-compose.yml up -d

# Or start development setup
docker-compose -f docker/docker-compose.dev.yml up -d
```

## Storage Savings

Using existing images saves approximately:
- **Ollama**: 8.99GB (already downloaded)
- **ChromaDB**: 805MB (already downloaded)
- **Redis**: 61.2MB (already downloaded)
- **Python**: 188MB (already downloaded)

**Total saved**: ~10GB of downloads
