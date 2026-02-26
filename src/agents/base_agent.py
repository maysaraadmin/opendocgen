"""
Base agent class for OpenDocGen agents.
"""

import asyncio
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional

from crewai import Agent
try:
    from langchain_core.language_models.base import BaseLanguageModel
except ImportError:
    # Fallback for older langchain versions
    from langchain.llms.base import BaseLLM as BaseLanguageModel

from ..config import get_settings
from ..llm.ollama_manager import OllamaManager


class BaseAgent(ABC):
    """Abstract base class for all agents."""
    
    def __init__(
        self,
        name: str,
        role: str,
        goal: str,
        backstory: str,
        tools: Optional[List[Any]] = None,
        llm: Optional[BaseLanguageModel] = None,
        verbose: bool = True,
        allow_delegation: bool = True,
        **kwargs
    ):
        """Initialize base agent."""
        self.name = name
        self.role = role
        self.goal = goal
        self.backstory = backstory
        self.tools = tools or []
        self.verbose = verbose
        self.allow_delegation = allow_delegation
        
        settings = get_settings()
        
        # Initialize LLM if not provided
        if llm is None:
            self.llm_manager = OllamaManager()
            self.llm = self.llm_manager.get_llm(settings.default_model)
        else:
            self.llm = llm
            self.llm_manager = None
        
        # Create CrewAI agent
        self.agent = Agent(
            role=self.role,
            goal=self.goal,
            backstory=self.backstory,
            tools=self.tools,
            llm=self.llm,
            verbose=self.verbose,
            allow_delegation=self.allow_delegation,
            **kwargs
        )
    
    @abstractmethod
    async def execute_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a specific task."""
        pass
    
    async def initialize(self) -> None:
        """Initialize the agent."""
        if self.llm_manager:
            await self.llm_manager.initialize()
    
    async def cleanup(self) -> None:
        """Cleanup resources."""
        if self.llm_manager:
            await self.llm_manager.cleanup()
    
    def get_agent(self) -> Agent:
        """Get the CrewAI agent instance."""
        return self.agent
    
    def add_tool(self, tool: Any) -> None:
        """Add a tool to the agent."""
        self.tools.append(tool)
        self.agent.tools = self.tools
    
    def remove_tool(self, tool: Any) -> None:
        """Remove a tool from the agent."""
        if tool in self.tools:
            self.tools.remove(tool)
            self.agent.tools = self.tools
    
    def update_llm(self, llm: BaseLanguageModel) -> None:
        """Update the agent's LLM."""
        self.llm = llm
        self.agent.llm = llm
    
    async def think(self, prompt: str) -> str:
        """Make the agent think about a prompt."""
        try:
            response = await asyncio.to_thread(self.llm.invoke, prompt)
            return str(response)
        except Exception as e:
            raise RuntimeError(f"Error in agent thinking: {e}")
    
    def __str__(self) -> str:
        """String representation."""
        return f"{self.__class__.__name__}(name='{self.name}', role='{self.role}')"
    
    def __repr__(self) -> str:
        """Detailed string representation."""
        return (
            f"{self.__class__.__name__}("
            f"name='{self.name}', "
            f"role='{self.role}', "
            f"goal='{self.goal[:50]}...', "
            f"tools_count={len(self.tools)})"
        )
