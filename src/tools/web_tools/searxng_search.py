"""
SearXNG search tool for web research.
"""

import asyncio
import logging
from typing import Any, Dict, List, Optional

import httpx

from ...config import get_settings

logger = logging.getLogger(__name__)


class SearxNGSearch:
    """Tool for searching the web using SearXNG."""
    
    def __init__(self, base_url: Optional[str] = None):
        """Initialize SearXNG search tool."""
        settings = get_settings()
        self.base_url = base_url or settings.searxng_url
        self.session = None
    
    async def _get_session(self) -> httpx.AsyncClient:
        """Get HTTP session."""
        if self.session is None:
            self.session = httpx.AsyncClient(timeout=30.0)
        return self.session
    
    async def search(
        self,
        query: str,
        num_results: int = 10,
        language: str = "en",
        time_range: Optional[str] = None,
        safe_search: str = "moderate"
    ) -> List[Dict[str, Any]]:
        """
        Search using SearXNG.
        
        Args:
            query: Search query
            num_results: Number of results to return
            language: Language code
            time_range: Time range filter (day, week, month, year)
            safe_search: Safe search level (off, moderate, strict)
        
        Returns:
            List of search results
        """
        session = await self._get_session()
        
        params = {
            "q": query,
            "format": "json",
            "engines": "google,duckduckgo,bing,qwant,wikipedia",
            "language": language,
            "safesearch": safe_search,
            "pageno": 1
        }
        
        if time_range:
            params["time_range"] = time_range
        
        try:
            response = await session.get(f"{self.base_url}/search", params=params)
            response.raise_for_status()
            
            data = response.json()
            
            # Process results
            results = []
            for result in data.get("results", [])[:num_results]:
                processed_result = {
                    "title": result.get("title", ""),
                    "url": result.get("url", ""),
                    "content": result.get("content", ""),
                    "engine": result.get("engine", ""),
                    "score": result.get("score", 0.0),
                    "publishedDate": result.get("publishedDate"),
                    "template": result.get("template", "")
                }
                results.append(processed_result)
            
            logger.info(f"Found {len(results)} results for query: {query}")
            return results
            
        except httpx.HTTPError as e:
            logger.error(f"HTTP error during search: {e}")
            raise RuntimeError(f"Search failed: {e}")
        except Exception as e:
            logger.error(f"Unexpected error during search: {e}")
            raise RuntimeError(f"Search failed: {e}")
    
    async def search_images(
        self,
        query: str,
        num_results: int = 10,
        size: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Search for images using SearXNG.
        
        Args:
            query: Search query
            num_results: Number of results to return
            size: Image size filter (small, medium, large, huge)
        
        Returns:
            List of image search results
        """
        session = await self._get_session()
        
        params = {
            "q": query,
            "format": "json",
            "categories": "images",
            "engines": "google,duckduckgo,bing,qwant",
            "pageno": 1
        }
        
        if size:
            params["image_size"] = size
        
        try:
            response = await session.get(f"{self.base_url}/search", params=params)
            response.raise_for_status()
            
            data = response.json()
            
            # Process image results
            results = []
            for result in data.get("results", [])[:num_results]:
                processed_result = {
                    "title": result.get("title", ""),
                    "url": result.get("url", ""),
                    "img_src": result.get("img_src", ""),
                    "thumbnail": result.get("thumbnail", ""),
                    "engine": result.get("engine", ""),
                    "score": result.get("score", 0.0),
                    "resolution": result.get("resolution", "")
                }
                results.append(processed_result)
            
            logger.info(f"Found {len(results)} image results for query: {query}")
            return results
            
        except httpx.HTTPError as e:
            logger.error(f"HTTP error during image search: {e}")
            raise RuntimeError(f"Image search failed: {e}")
        except Exception as e:
            logger.error(f"Unexpected error during image search: {e}")
            raise RuntimeError(f"Image search failed: {e}")
    
    async def search_videos(
        self,
        query: str,
        num_results: int = 10
    ) -> List[Dict[str, Any]]:
        """
        Search for videos using SearXNG.
        
        Args:
            query: Search query
            num_results: Number of results to return
        
        Returns:
            List of video search results
        """
        session = await self._get_session()
        
        params = {
            "q": query,
            "format": "json",
            "categories": "videos",
            "engines": "youtube,dailymotion,vimeo",
            "pageno": 1
        }
        
        try:
            response = await session.get(f"{self.base_url}/search", params=params)
            response.raise_for_status()
            
            data = response.json()
            
            # Process video results
            results = []
            for result in data.get("results", [])[:num_results]:
                processed_result = {
                    "title": result.get("title", ""),
                    "url": result.get("url", ""),
                    "content": result.get("content", ""),
                    "iframe_src": result.get("iframe_src", ""),
                    "engine": result.get("engine", ""),
                    "score": result.get("score", 0.0),
                    "length": result.get("length", "")
                }
                results.append(processed_result)
            
            logger.info(f"Found {len(results)} video results for query: {query}")
            return results
            
        except httpx.HTTPError as e:
            logger.error(f"HTTP error during video search: {e}")
            raise RuntimeError(f"Video search failed: {e}")
        except Exception as e:
            logger.error(f"Unexpected error during video search: {e}")
            raise RuntimeError(f"Video search failed: {e}")
    
    async def get_suggestions(self, query: str) -> List[str]:
        """
        Get search suggestions for a query.
        
        Args:
            query: Partial search query
        
        Returns:
            List of search suggestions
        """
        session = await self._get_session()
        
        params = {
            "q": query,
            "format": "json",
            "autocomplete": "1"
        }
        
        try:
            response = await session.get(f"{self.base_url}/autocompleter", params=params)
            response.raise_for_status()
            
            suggestions = response.json()
            return suggestions if isinstance(suggestions, list) else []
            
        except httpx.HTTPError as e:
            logger.error(f"HTTP error getting suggestions: {e}")
            return []
        except Exception as e:
            logger.error(f"Unexpected error getting suggestions: {e}")
            return []
    
    async def get_engines(self) -> List[Dict[str, Any]]:
        """
        Get available search engines.
        
        Returns:
            List of available engines
        """
        session = await self._get_session()
        
        try:
            response = await session.get(f"{self.base_url}/config", params={"format": "json"})
            response.raise_for_status()
            
            data = response.json()
            engines = []
            
            for engine_name, engine_info in data.get("engines", {}).items():
                if engine_info.get("enabled", False):
                    engines.append({
                        "name": engine_name,
                        "categories": engine_info.get("categories", []),
                        "shortcut": engine_info.get("shortcut", ""),
                        "engine_type": engine_info.get("engine", "")
                    })
            
            return engines
            
        except httpx.HTTPError as e:
            logger.error(f"HTTP error getting engines: {e}")
            return []
        except Exception as e:
            logger.error(f"Unexpected error getting engines: {e}")
            return []
    
    async def close(self):
        """Close HTTP session."""
        if self.session:
            await self.session.aclose()
            self.session = None
    
    async def __aenter__(self):
        """Async context manager entry."""
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        await self.close()
