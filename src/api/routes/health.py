"""
Health check endpoints.
"""

from datetime import datetime
from typing import Dict, Any

from fastapi import APIRouter, Depends

from ...core.orchestrator import Orchestrator
from ...config import get_settings

router = APIRouter()


@router.get("/")
async def health_check() -> Dict[str, Any]:
    """Basic health check."""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "version": get_settings().app_version
    }


@router.get("/detailed")
async def detailed_health_check() -> Dict[str, Any]:
    """Detailed health check with system status."""
    settings = get_settings()
    
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "version": settings.app_version,
        "services": {
            "api": "healthy",
            "agents": "healthy",
            "database": "healthy"  # TODO: Check actual DB status
        },
        "configuration": {
            "debug": settings.debug,
            "log_level": settings.log_level,
            "enable_gpu": settings.enable_gpu
        }
    }
