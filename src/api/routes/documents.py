"""
Document management endpoints.
"""

from typing import Dict, Any, List

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from ...core.orchestrator import Orchestrator

router = APIRouter()


class DocumentRequest(BaseModel):
    """Request model for document generation."""
    topic: str
    document_type: str = "research_report"
    requirements: List[str] = []
    template: str = "research_paper"


async def get_orchestrator() -> Orchestrator:
    """Get orchestrator instance."""
    return Orchestrator()


@router.post("/generate")
async def generate_document(
    request: DocumentRequest,
    orchestrator: Orchestrator = Depends(get_orchestrator)
) -> Dict[str, Any]:
    """Generate a new document."""
    try:
        # Create comprehensive document task
        task_data = {
            "type": "comprehensive_document",
            "agent": "writer",
            "data": {
                "topic": request.topic,
                "document_type": request.document_type,
                "requirements": request.requirements,
                "template": request.template
            }
        }
        
        # Execute task
        from ...models.task import Task, TaskType
        import uuid
        
        task = Task(
            id=str(uuid.uuid4()),
            type=TaskType("generate"),
            agent="writer",
            data=task_data["data"]
        )
        
        result = await orchestrator.execute_task(task)
        
        return {
            "document_id": task.id,
            "status": "completed",
            "document": result
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/")
async def list_documents() -> List[Dict[str, Any]]:
    """List all generated documents."""
    # TODO: Implement document listing from storage
    return []


@router.get("/{document_id}")
async def get_document(document_id: str) -> Dict[str, Any]:
    """Get a specific document."""
    # TODO: Implement document retrieval from storage
    return {"document_id": document_id, "status": "not_found"}
