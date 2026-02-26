"""
Ollama LLM Manager for OpenDocGen.
"""

import asyncio
from typing import Any, Dict, List, Optional

from langchain_ollama import OllamaLLM
from langchain_core.language_models.base import BaseLanguageModel

from ..config import get_settings


class OllamaManager:
    """Manages Ollama LLM interactions."""
    
    def __init__(self):
        """Initialize the Ollama manager."""
        self.settings = get_settings()
        self._llm: Optional[BaseLanguageModel] = None
        self._models_cache: Dict[str, Any] = {}
    
    async def initialize(self):
        """Initialize the Ollama LLM."""
        try:
            self._llm = OllamaLLM(
                model=self.settings.default_model,
                base_url=self.settings.ollama_base_url,
                temperature=0.7,
                max_tokens=2048,
            )
            return True
        except Exception as e:
            print(f"Failed to initialize Ollama: {e}")
            return False
    
    def get_llm(self, model: str = None) -> Optional[BaseLanguageModel]:
        """Get the initialized LLM instance."""
        if model and model != self.settings.default_model:
            # Create a new LLM instance for the specified model
            return OllamaLLM(
                model=model,
                base_url=self.settings.ollama_base_url,
                temperature=0.7,
                max_tokens=2048,
            )
        return self._llm
    
    async def generate_response(
        self, 
        prompt: str, 
        **kwargs
    ) -> str:
        """Generate a response using the LLM."""
        if not self._llm:
            await self.initialize()
        
        try:
            response = await self._llm.ainvoke(prompt)
            return response.content if hasattr(response, 'content') else str(response)
        except Exception as e:
            print(f"Error generating response: {e}")
            return f"Error: {str(e)}"
    
    def get_available_models(self) -> List[str]:
        """Get list of available models."""
        return [
            self.settings.default_model,
            self.settings.alternate_model,
            self.settings.code_model,
            self.settings.embedding_model,
        ]
    
    def switch_model(self, model_name: str) -> bool:
        """Switch to a different model."""
        try:
            self._llm = OllamaLLM(
                model=model_name,
                base_url=self.settings.ollama_base_url,
                temperature=0.7,
                max_tokens=2048,
            )
            return True
        except Exception as e:
            print(f"Failed to switch to model {model_name}: {e}")
            return False
