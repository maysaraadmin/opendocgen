"""
Task models for OpenDocGen.
"""

from datetime import datetime
from enum import Enum
from typing import Any, Dict, Optional
from uuid import uuid4

from pydantic import BaseModel, Field


class TaskType(str, Enum):
    """Task types."""
    RESEARCH = "research"
    ANALYSIS = "analysis"
    WRITING = "writing"
    CODE = "code"
    REVIEW = "review"
    GENERATE = "generate"


class TaskStatus(str, Enum):
    """Task status."""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class Task(BaseModel):
    """Task model."""
    
    id: str = Field(default_factory=lambda: str(uuid4()))
    type: TaskType
    agent: Optional[str] = None
    workflow: Optional[str] = None
    data: Dict[str, Any] = Field(default_factory=dict)
    status: TaskStatus = TaskStatus.PENDING
    result: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Config:
        use_enum_values = True
    
    def update_timestamp(self):
        """Update the updated_at timestamp."""
        self.updated_at = datetime.utcnow()
