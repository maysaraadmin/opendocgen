"""
Research workflow for comprehensive document generation.
"""

import logging
from typing import Any, Dict

from ..models.task import Task

logger = logging.getLogger(__name__)


class ResearchWorkflow:
    """Workflow for research → analysis → writing process."""
    
    def __init__(self, agents: Dict[str, Any]):
        """Initialize research workflow."""
        self.agents = agents
        self.description = "Research, analyze, and write comprehensive documents"
    
    async def execute(self, task: Task) -> Dict[str, Any]:
        """Execute the research workflow."""
        logger.info(f"Starting research workflow for task {task.id}")
        
        try:
            # Step 1: Research
            research_data = await self._research_phase(task)
            
            # Step 2: Analysis
            analysis_data = await self._analysis_phase(research_data)
            
            # Step 3: Writing
            document_data = await self._writing_phase(task, research_data, analysis_data)
            
            # Step 4: Review
            review_data = await self._review_phase(document_data)
            
            result = {
                "type": "research_workflow_result",
                "research": research_data,
                "analysis": analysis_data,
                "document": document_data,
                "review": review_data,
                "status": "completed"
            }
            
            logger.info(f"Research workflow completed for task {task.id}")
            return result
            
        except Exception as e:
            logger.error(f"Research workflow failed for task {task.id}: {e}")
            raise
    
    async def _research_phase(self, task: Task) -> Dict[str, Any]:
        """Execute research phase."""
        research_agent = self.agents["research"]
        
        research_task = {
            "type": "comprehensive_research",
            "topic": task.data.get("topic", ""),
            "requirements": task.data.get("requirements", [])
        }
        
        return await research_agent.execute_task(research_task)
    
    async def _analysis_phase(self, research_data: Dict[str, Any]) -> Dict[str, Any]:
        """Execute analysis phase."""
        analysis_agent = self.agents["analysis"]
        
        analysis_task = {
            "type": "comprehensive_analysis",
            "data": research_data.get("search_results", {}),
            "goals": ["Extract insights", "Identify patterns", "Generate statistics"]
        }
        
        return await analysis_agent.execute_task(analysis_task)
    
    async def _writing_phase(
        self,
        task: Task,
        research_data: Dict[str, Any],
        analysis_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Execute writing phase."""
        writer_agent = self.agents["writer"]
        
        writing_task = {
            "type": "comprehensive_document",
            "topic": task.data.get("topic", ""),
            "document_type": task.data.get("document_type", "research_report"),
            "research_data": research_data,
            "analysis_data": analysis_data,
            "template": task.data.get("template", "research_paper")
        }
        
        return await writer_agent.execute_task(writing_task)
    
    async def _review_phase(self, document_data: Dict[str, Any]) -> Dict[str, Any]:
        """Execute review phase."""
        reviewer_agent = self.agents["reviewer"]
        
        review_task = {
            "type": "comprehensive_review",
            "content": document_data.get("document", "")
        }
        
        return await reviewer_agent.execute_task(review_task)
