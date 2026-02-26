"""
Agent configuration models.
"""

from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class AgentConfig(BaseModel):
    """Agent configuration model."""
    
    name: str
    role: str
    goal: str
    backstory: str
    tools: List[str] = Field(default_factory=list)
    llm_model: Optional[str] = None
    verbose: bool = True
    allow_delegation: bool = True
    custom_config: Dict[str, Any] = Field(default_factory=dict)
