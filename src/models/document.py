"""
Document models for OpenDocGen.
"""

from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional
from uuid import uuid4

from pydantic import BaseModel, Field


class DocumentType(str, Enum):
    """Document types."""
    RESEARCH_REPORT = "research_report"
    BUSINESS_REPORT = "business_report"
    TECHNICAL_DOC = "technical_doc"
    PROPOSAL = "proposal"
    ACADEMIC_PAPER = "academic_paper"
    CUSTOM = "custom"


class Document(BaseModel):
    """Document model."""
    
    id: str = Field(default_factory=lambda: str(uuid4()))
    title: str
    type: DocumentType
    content: str
    metadata: Dict[str, Any] = Field(default_factory=dict)
    sections: List[str] = Field(default_factory=list)
    word_count: int = 0
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Config:
        use_enum_values = True
    
    def calculate_word_count(self):
        """Calculate word count of the document."""
        self.word_count = len(self.content.split())
        return self.word_count
