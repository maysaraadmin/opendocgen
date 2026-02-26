"""
Agent management endpoints.
"""

from typing import List, Dict, Any

from fastapi import APIRouter, Depends, HTTPException

from ...core.orchestrator import Orchestrator

router = APIRouter()


async def get_orchestrator() -> Orchestrator:
    """Get orchestrator instance."""
    # In a real implementation, this would be injected from app state
    return Orchestrator()


@router.get("/")
async def list_agents(orchestrator: Orchestrator = Depends(get_orchestrator)) -> List[Dict[str, Any]]:
    """List all available agents."""
    try:
        agents = await orchestrator.get_available_agents()
        return agents
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{agent_name}")
async def get_agent_info(
    agent_name: str,
    orchestrator: Orchestrator = Depends(get_orchestrator)
) -> Dict[str, Any]:
    """Get information about a specific agent."""
    try:
        agents = await orchestrator.get_available_agents()
        
        for agent in agents:
            if agent["name"] == agent_name:
                return agent
        
        raise HTTPException(status_code=404, detail=f"Agent '{agent_name}' not found")
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
