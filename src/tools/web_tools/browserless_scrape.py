"""
Browserless scraping tool for web content extraction.
"""

import asyncio
import logging
from typing import Any, Dict, List, Optional

import httpx
from bs4 import BeautifulSoup

from ...config import get_settings

logger = logging.getLogger(__name__)


class BrowserlessScrape:
    """Tool for scraping web content using Browserless."""
    
    def __init__(self, base_url: Optional[str] = None):
        """Initialize Browserless scraping tool."""
        settings = get_settings()
        self.base_url = base_url or settings.browserless_url
        self.session = None
    
    async def _get_session(self) -> httpx.AsyncClient:
        """Get HTTP session."""
        if self.session is None:
            self.session = httpx.AsyncClient(timeout=60.0)
        return self.session
    
    async def scrape(
        self,
        url: str,
        wait_for: Optional[str] = None,
        selector: Optional[str] = None,
        screenshot: bool = False,
        pdf: bool = False,
        javascript: bool = True,
        user_agent: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Scrape content from a URL.
        
        Args:
            url: URL to scrape
            wait_for: CSS selector to wait for
            selector: CSS selector to extract content from
            screenshot: Whether to capture screenshot
            pdf: Whether to generate PDF
            javascript: Whether to enable JavaScript
            user_agent: Custom user agent string
        
        Returns:
            Scraped content and metadata
        """
        session = await self._get_session()
        
        # Prepare request payload
        payload = {
            "url": url,
            "elements": [{
                "selector": selector or "body"
            }],
            "waitFor": wait_for,
            "javascript": javascript,
            "stealth": True,
            "ignoreHTTPSErrors": True
        }
        
        if user_agent:
            payload["userAgent"] = user_agent
        
        try:
            # Make request to Browserless
            response = await session.post(
                f"{self.base_url}/content",
                json=payload
            )
            response.raise_for_status()
            
            data = response.json()
            
            # Extract content
            content = ""
            if data and "data" in data and len(data["data"]) > 0:
                content = data["data"][0].get("text", "")
            
            # Parse with BeautifulSoup for better extraction
            if content:
                soup = BeautifulSoup(content, 'html.parser')
                
                # Remove script and style elements
                for script in soup(["script", "style"]):
                    script.decompose()
                
                # Extract clean text
                clean_content = soup.get_text(separator='\n', strip=True)
                
                # Extract metadata
                metadata = self._extract_metadata(soup)
                
                result = {
                    "url": url,
                    "title": metadata.get("title", ""),
                    "content": clean_content,
                    "html": content,
                    "metadata": metadata,
                    "word_count": len(clean_content.split()),
                    "status": "success"
                }
            else:
                result = {
                    "url": url,
                    "content": "",
                    "html": "",
                    "metadata": {},
                    "word_count": 0,
                    "status": "no_content"
                }
            
            # Add screenshot if requested
            if screenshot:
                screenshot_data = await self._capture_screenshot(url)
                result["screenshot"] = screenshot_data
            
            # Add PDF if requested
            if pdf:
                pdf_data = await self._generate_pdf(url)
                result["pdf"] = pdf_data
            
            logger.info(f"Successfully scraped {url}")
            return result
            
        except httpx.HTTPError as e:
            logger.error(f"HTTP error scraping {url}: {e}")
            return {
                "url": url,
                "error": str(e),
                "status": "error"
            }
        except Exception as e:
            logger.error(f"Unexpected error scraping {url}: {e}")
            return {
                "url": url,
                "error": str(e),
                "status": "error"
            }
    
    async def scrape_multiple(
        self,
        urls: List[str],
        concurrent: int = 3,
        **kwargs
    ) -> List[Dict[str, Any]]:
        """
        Scrape multiple URLs concurrently.
        
        Args:
            urls: List of URLs to scrape
            concurrent: Number of concurrent requests
            **kwargs: Additional arguments for scrape method
        
        Returns:
            List of scrape results
        """
        semaphore = asyncio.Semaphore(concurrent)
        
        async def scrape_with_semaphore(url: str) -> Dict[str, Any]:
            async with semaphore:
                return await self.scrape(url, **kwargs)
        
        tasks = [scrape_with_semaphore(url) for url in urls]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Convert exceptions to error results
        processed_results = []
        for url, result in zip(urls, results):
            if isinstance(result, Exception):
                processed_results.append({
                    "url": url,
                    "error": str(result),
                    "status": "error"
                })
            else:
                processed_results.append(result)
        
        return processed_results
    
    async def _capture_screenshot(self, url: str) -> Optional[Dict[str, Any]]:
        """Capture screenshot of a URL."""
        session = await self._get_session()
        
        payload = {
            "url": url,
            "type": "png",
            "quality": 80,
            "fullPage": True,
            "clip": None
        }
        
        try:
            response = await session.post(
                f"{self.base_url}/screenshot",
                json=payload
            )
            response.raise_for_status()
            
            # Return screenshot data (base64 encoded)
            return {
                "data": response.text,
                "format": "png"
            }
            
        except Exception as e:
            logger.error(f"Error capturing screenshot of {url}: {e}")
            return None
    
    async def _generate_pdf(self, url: str) -> Optional[Dict[str, Any]]:
        """Generate PDF of a URL."""
        session = await self._get_session()
        
        payload = {
            "url": url,
            "format": "A4",
            "printBackground": True,
            "landscape": False
        }
        
        try:
            response = await session.post(
                f"{self.base_url}/pdf",
                json=payload
            )
            response.raise_for_status()
            
            # Return PDF data (base64 encoded)
            return {
                "data": response.text,
                "format": "pdf"
            }
            
        except Exception as e:
            logger.error(f"Error generating PDF of {url}: {e}")
            return None
    
    def _extract_metadata(self, soup: BeautifulSoup) -> Dict[str, Any]:
        """Extract metadata from BeautifulSoup object."""
        metadata = {}
        
        # Title
        title_tag = soup.find('title')
        metadata["title"] = title_tag.get_text().strip() if title_tag else ""
        
        # Meta description
        desc_tag = soup.find('meta', attrs={'name': 'description'})
        metadata["description"] = desc_tag.get('content', '') if desc_tag else ""
        
        # Meta keywords
        keywords_tag = soup.find('meta', attrs={'name': 'keywords'})
        metadata["keywords"] = keywords_tag.get('content', '') if keywords_tag else ""
        
        # Open Graph tags
        og_tags = {}
        for tag in soup.find_all('meta', property=lambda x: x and x.startswith('og:')):
            og_tags[tag['property']] = tag.get('content', '')
        metadata["open_graph"] = og_tags
        
        # Twitter Card tags
        twitter_tags = {}
        for tag in soup.find_all('meta', attrs={'name': lambda x: x and x.startswith('twitter:')}):
            twitter_tags[tag['name']] = tag.get('content', '')
        metadata["twitter_card"] = twitter_tags
        
        # Language
        html_tag = soup.find('html')
        metadata["language"] = html_tag.get('lang', '') if html_tag else ""
        
        # Canonical URL
        canonical_tag = soup.find('link', rel='canonical')
        metadata["canonical_url"] = canonical_tag.get('href', '') if canonical_tag else ""
        
        # Author
        author_tag = soup.find('meta', attrs={'name': 'author'})
        metadata["author"] = author_tag.get('content', '') if author_tag else ""
        
        # Published date
        pub_date_tags = [
            soup.find('meta', attrs={'name': 'article:published_time'}),
            soup.find('meta', attrs={'property': 'article:published_time'}),
            soup.find('meta', attrs={'name': 'date'}),
            soup.find('meta', attrs={'property': 'date'})
        ]
        
        for tag in pub_date_tags:
            if tag and tag.get('content'):
                metadata["published_date"] = tag.get('content')
                break
        
        return metadata
    
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
