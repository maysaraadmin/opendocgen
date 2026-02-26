"""
Main entry point for OpenDocGen.
"""

import asyncio
import logging
from contextlib import asynccontextmanager
from pathlib import Path

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from rich.console import Console
from rich.logging import RichHandler

from .api.routes import agents, documents, files, health, tasks
from .config import get_settings, create_directories
from .core.orchestrator import Orchestrator
from .utils.logger import setup_logging

# Setup logging
setup_logging()
logger = logging.getLogger(__name__)
console = Console()

# Global orchestrator instance
orchestrator: Orchestrator = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager."""
    global orchestrator
    
    settings = get_settings()
    
    # Create necessary directories
    create_directories()
    
    # Initialize orchestrator
    console.print("🚀 Initializing OpenDocGen...", style="bold blue")
    orchestrator = Orchestrator()
    await orchestrator.initialize()
    
    console.print("✅ OpenDocGen initialized successfully!", style="bold green")
    
    yield
    
    # Cleanup
    console.print("🔄 Shutting down OpenDocGen...", style="bold yellow")
    if orchestrator:
        await orchestrator.cleanup()
    console.print("✅ Shutdown complete!", style="bold green")


def create_app() -> FastAPI:
    """Create FastAPI application."""
    settings = get_settings()
    
    app = FastAPI(
        title=settings.app_name,
        version=settings.app_version,
        description="Open-source autonomous document generation agent",
        lifespan=lifespan,
    )
    
    # Add CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Include routers
    app.include_router(health.router, prefix="/health", tags=["health"])
    app.include_router(agents.router, prefix="/api/v1/agents", tags=["agents"])
    app.include_router(tasks.router, prefix="/api/v1/tasks", tags=["tasks"])
    app.include_router(documents.router, prefix="/api/v1/documents", tags=["documents"])
    app.include_router(files.router, prefix="/api/v1/files", tags=["files"])
    
    return app


app = create_app()
