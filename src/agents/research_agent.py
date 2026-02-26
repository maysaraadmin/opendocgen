"""
Research agent for web search and information gathering.
"""

from typing import Any, Dict, List

from .base_agent import BaseAgent
from ..tools.web_tools.searxng_search import SearxNGSearch
from ..tools.web_tools.browserless_scrape import BrowserlessScrape
from ..tools.web_tools.download_manager import DownloadManager


class ResearchAgent(BaseAgent):
    """Agent specialized in web research and information gathering."""
    
    def __init__(self, **kwargs):
        """Initialize research agent."""
        super().__init__(
            name="Research Agent",
            role="Research Specialist",
            goal="Conduct comprehensive web research to gather accurate, relevant, and up-to-date information for document generation",
            backstory=(
                "You are an expert researcher with years of experience in finding and synthesizing information "
                "from various web sources. You excel at identifying credible sources, extracting key information, "
                "and organizing research findings in a structured manner. You are thorough, analytical, and always "
                "verify the credibility of your sources."
            ),
            **kwargs
        )
        
        # Initialize research tools
        self.search_tool = SearxNGSearch()
        self.scrape_tool = BrowserlessScrape()
        self.download_tool = DownloadManager()
        
        # Add tools to agent
        self.add_tool(self.search_tool)
        self.add_tool(self.scrape_tool)
        self.add_tool(self.download_tool)
    
    async def execute_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a research task."""
        task_type = task.get("type", "search")
        
        if task_type == "search":
            return await self._perform_search(task)
        elif task_type == "scrape":
            return await self._scrape_content(task)
        elif task_type == "download":
            return await self._download_content(task)
        elif task_type == "comprehensive_research":
            return await self._comprehensive_research(task)
        else:
            raise ValueError(f"Unknown task type: {task_type}")
    
    async def _perform_search(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Perform web search."""
        query = task.get("query")
        num_results = task.get("num_results", 10)
        
        if not query:
            raise ValueError("Search query is required")
        
        results = await self.search_tool.search(query, num_results=num_results)
        
        return {
            "type": "search_results",
            "query": query,
            "results": results,
            "num_results": len(results)
        }
    
    async def _scrape_content(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Scrape content from URLs."""
        urls = task.get("urls", [])
        if isinstance(urls, str):
            urls = [urls]
        
        scraped_content = []
        for url in urls:
            try:
                content = await self.scrape_tool.scrape(url)
                scraped_content.append({
                    "url": url,
                    "content": content,
                    "status": "success"
                })
            except Exception as e:
                scraped_content.append({
                    "url": url,
                    "error": str(e),
                    "status": "error"
                })
        
        return {
            "type": "scraped_content",
            "content": scraped_content,
            "total_urls": len(urls),
            "successful_scrapes": len([c for c in scraped_content if c["status"] == "success"])
        }
    
    async def _download_content(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Download content from URLs."""
        urls = task.get("urls", [])
        if isinstance(urls, str):
            urls = [urls]
        
        download_path = task.get("download_path", "./data/downloads")
        
        downloaded_files = []
        for url in urls:
            try:
                file_path = await self.download_tool.download(url, download_path)
                downloaded_files.append({
                    "url": url,
                    "file_path": file_path,
                    "status": "success"
                })
            except Exception as e:
                downloaded_files.append({
                    "url": url,
                    "error": str(e),
                    "status": "error"
                })
        
        return {
            "type": "downloaded_files",
            "files": downloaded_files,
            "total_urls": len(urls),
            "successful_downloads": len([f for f in downloaded_files if f["status"] == "success"])
        }
    
    async def _comprehensive_research(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Perform comprehensive research on a topic."""
        topic = task.get("topic")
        if not topic:
            raise ValueError("Research topic is required")
        
        # Step 1: Initial search
        search_results = await self._perform_search({
            "query": topic,
            "num_results": 15
        })
        
        # Step 2: Scrape top results
        top_urls = [result["url"] for result in search_results["results"][:5]]
        scraped_content = await self._scrape_content({"urls": top_urls})
        
        # Step 3: Synthesize information
        synthesis_prompt = f"""
        Based on the following research results and scraped content, provide a comprehensive summary of the topic: {topic}
        
        Search Results:
        {search_results}
        
        Scraped Content:
        {scraped_content}
        
        Please provide:
        1. Key findings and insights
        2. Important facts and statistics
        3. Credible sources and references
        4. Areas that need further research
        5. Overall assessment of the information quality
        """
        
        synthesis = await self.think(synthesis_prompt)
        
        return {
            "type": "comprehensive_research",
            "topic": topic,
            "search_results": search_results,
            "scraped_content": scraped_content,
            "synthesis": synthesis,
            "recommendations": self._generate_recommendations(search_results, scraped_content)
        }
    
    def _generate_recommendations(self, search_results: Dict, scraped_content: Dict) -> List[str]:
        """Generate research recommendations."""
        recommendations = []
        
        # Analyze search quality
        if len(search_results.get("results", [])) < 5:
            recommendations.append("Consider broadening search terms or using alternative search queries")
        
        # Analyze content quality
        successful_scrapes = len([c for c in scraped_content.get("content", []) if c["status"] == "success"])
        if successful_scrapes < len(search_results.get("results", [])) // 2:
            recommendations.append("Many sources could not be scraped - consider manual review of important sources")
        
        # General recommendations
        recommendations.extend([
            "Verify information from multiple sources",
            "Check the publication dates for timeliness",
            "Look for authoritative sources and expert opinions",
            "Consider searching for academic papers or official reports"
        ])
        
        return recommendations
