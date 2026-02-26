"""
Orchestrator for managing agent workflows and task execution.
"""

import asyncio
import logging
from typing import Any, Dict, List, Optional

from ..agents import (
    ResearchAgent, AnalysisAgent, WriterAgent, 
    CodeAgent, ReviewerAgent
)
from ..config import get_settings
from ..models.task import Task, TaskStatus
from ..workflows.research_workflow import ResearchWorkflow

logger = logging.getLogger(__name__)


class Orchestrator:
    """Main orchestrator for OpenDocGen operations."""
    
    def __init__(self):
        """Initialize orchestrator."""
        self.settings = get_settings()
        self.agents = {}
        self.workflows = {}
        self.running_tasks = {}
        self._initialized = False
    
    async def initialize(self):
        """Initialize all agents and workflows."""
        if self._initialized:
            return
        
        logger.info("Initializing OpenDocGen orchestrator...")
        
        # Initialize agents
        await self._initialize_agents()
        
        # Initialize workflows
        await self._initialize_workflows()
        
        self._initialized = True
        logger.info("Orchestrator initialized successfully")
    
    async def _initialize_agents(self):
        """Initialize all agents."""
        try:
            # Create agent instances
            self.agents = {
                "research": ResearchAgent(),
                "analysis": AnalysisAgent(),
                "writer": WriterAgent(),
                "code": CodeAgent(),
                "reviewer": ReviewerAgent()
            }
            
            # Initialize each agent
            for agent_name, agent in self.agents.items():
                await agent.initialize()
                logger.info(f"Initialized {agent_name} agent")
                
        except Exception as e:
            logger.error(f"Error initializing agents: {e}")
            raise
    
    async def _initialize_workflows(self):
        """Initialize predefined workflows."""
        try:
            self.workflows = {
                "research": ResearchWorkflow(self.agents)
            }
            
            logger.info(f"Initialized {len(self.workflows)} workflows")
            
        except Exception as e:
            logger.error(f"Error initializing workflows: {e}")
            raise
    
    async def execute_task(self, task: Task) -> Dict[str, Any]:
        """Execute a task using appropriate agents or workflows."""
        if not self._initialized:
            await self.initialize()
        
        task_id = task.id
        logger.info(f"Executing task {task_id}: {task.type}")
        
        try:
            # Check if task is already running
            if task_id in self.running_tasks:
                raise RuntimeError(f"Task {task_id} is already running")
            
            # Mark task as running
            task.status = TaskStatus.RUNNING
            self.running_tasks[task_id] = task
            
            # Execute based on task type
            if task.workflow:
                result = await self._execute_workflow(task)
            else:
                result = await self._execute_agent_task(task)
            
            # Mark task as completed
            task.status = TaskStatus.COMPLETED
            task.result = result
            
            # Remove from running tasks
            del self.running_tasks[task_id]
            
            logger.info(f"Task {task_id} completed successfully")
            return result
            
        except Exception as e:
            # Mark task as failed
            task.status = TaskStatus.FAILED
            task.error = str(e)
            
            # Remove from running tasks
            if task_id in self.running_tasks:
                del self.running_tasks[task_id]
            
            logger.error(f"Task {task_id} failed: {e}")
            raise
    
    async def _execute_workflow(self, task: Task) -> Dict[str, Any]:
        """Execute a predefined workflow."""
        workflow_name = task.workflow
        
        if workflow_name not in self.workflows:
            raise ValueError(f"Workflow '{workflow_name}' not found")
        
        workflow = self.workflows[workflow_name]
        return await workflow.execute(task)
    
    async def _execute_agent_task(self, task: Task) -> Dict[str, Any]:
        """Execute a task using a specific agent."""
        agent_name = task.agent
        
        if agent_name not in self.agents:
            raise ValueError(f"Agent '{agent_name}' not found")
        
        agent = self.agents[agent_name]
        return await agent.execute_task(task.data)
    
    async def get_task_status(self, task_id: str) -> Optional[Dict[str, Any]]:
        """Get status of a running task."""
        if task_id in self.running_tasks:
            task = self.running_tasks[task_id]
            return {
                "task_id": task_id,
                "status": task.status.value,
                "type": task.type,
                "created_at": task.created_at.isoformat(),
                "updated_at": task.updated_at.isoformat()
            }
        
        return None
    
    async def cancel_task(self, task_id: str) -> bool:
        """Cancel a running task."""
        if task_id in self.running_tasks:
            task = self.running_tasks[task_id]
            task.status = TaskStatus.CANCELLED
            del self.running_tasks[task_id]
            logger.info(f"Task {task_id} cancelled")
            return True
        
        return False
    
    async def get_available_agents(self) -> List[Dict[str, Any]]:
        """Get list of available agents."""
        agents_info = []
        
        for name, agent in self.agents.items():
            agents_info.append({
                "name": name,
                "role": agent.role,
                "goal": agent.goal,
                "tools_count": len(agent.tools)
            })
        
        return agents_info
    
    async def get_available_workflows(self) -> List[Dict[str, Any]]:
        """Get list of available workflows."""
        workflows_info = []
        
        for name, workflow in self.workflows.items():
            workflows_info.append({
                "name": name,
                "description": getattr(workflow, 'description', ''),
                "agents_used": getattr(workflow, 'agents', [])
            })
        
        return workflows_info
    
    async def cleanup(self):
        """Cleanup resources."""
        logger.info("Cleaning up orchestrator...")
        
        # Cancel all running tasks
        for task_id in list(self.running_tasks.keys()):
            await self.cancel_task(task_id)
        
        # Cleanup agents
        for agent_name, agent in self.agents.items():
            try:
                await agent.cleanup()
                logger.info(f"Cleaned up {agent_name} agent")
            except Exception as e:
                logger.error(f"Error cleaning up {agent_name} agent: {e}")
        
        self.agents.clear()
        self.workflows.clear()
        self._initialized = False
        
        logger.info("Orchestrator cleanup completed")
