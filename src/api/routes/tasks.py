"""
Task management endpoints.
"""

import uuid
from typing import Dict, Any, List

from fastapi import APIRouter, Depends, HTTPException

from ...core.orchestrator import Orchestrator
from ...models.task import Task, TaskType, TaskStatus

router = APIRouter()


async def get_orchestrator() -> Orchestrator:
    """Get orchestrator instance."""
    return Orchestrator()


@router.post("/")
async def create_task(
    task_data: Dict[str, Any],
    orchestrator: Orchestrator = Depends(get_orchestrator)
) -> Dict[str, Any]:
    """Create and execute a new task."""
    try:
        # Create task
        task = Task(
            id=str(uuid.uuid4()),
            type=TaskType(task_data.get("type", "research")),
            agent=task_data.get("agent"),
            workflow=task_data.get("workflow"),
            data=task_data.get("data", {})
        )
        
        # Execute task
        result = await orchestrator.execute_task(task)
        
        return {
            "task_id": task.id,
            "status": task.status.value,
            "result": result
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{task_id}")
async def get_task_status(
    task_id: str,
    orchestrator: Orchestrator = Depends(get_orchestrator)
) -> Dict[str, Any]:
    """Get status of a specific task."""
    try:
        status = await orchestrator.get_task_status(task_id)
        
        if not status:
            raise HTTPException(status_code=404, detail=f"Task '{task_id}' not found")
        
        return status
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{task_id}")
async def cancel_task(
    task_id: str,
    orchestrator: Orchestrator = Depends(get_orchestrator)
) -> Dict[str, Any]:
    """Cancel a running task."""
    try:
        success = await orchestrator.cancel_task(task_id)
        
        if not success:
            raise HTTPException(status_code=404, detail=f"Task '{task_id}' not found or not running")
        
        return {"message": f"Task '{task_id}' cancelled successfully"}
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
