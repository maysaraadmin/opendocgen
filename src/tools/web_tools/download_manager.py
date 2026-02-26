"""
Download manager for file downloads from web sources.
"""

import asyncio
import logging
import os
import urllib.parse
from pathlib import Path
from typing import Any, Dict, List, Optional

import aiofiles
import httpx

from ...config import get_settings

logger = logging.getLogger(__name__)


class DownloadManager:
    """Tool for managing file downloads from web sources."""
    
    def __init__(self, download_dir: Optional[Path] = None):
        """Initialize download manager."""
        settings = get_settings()
        self.download_dir = download_dir or settings.downloads_dir
        self.session = None
        
        # Ensure download directory exists
        self.download_dir.mkdir(parents=True, exist_ok=True)
    
    async def _get_session(self) -> httpx.AsyncClient:
        """Get HTTP session."""
        if self.session is None:
            self.session = httpx.AsyncClient(
                timeout=60.0,
                follow_redirects=True,
                headers={
                    "User-Agent": "OpenDocGen/1.0 (Document Generation Bot)"
                }
            )
        return self.session
    
    async def download(
        self,
        url: str,
        save_path: Optional[Path] = None,
        filename: Optional[str] = None,
        overwrite: bool = False,
        chunk_size: int = 8192
    ) -> Dict[str, Any]:
        """
        Download a file from a URL.
        
        Args:
            url: URL to download from
            save_path: Directory to save the file (uses default if None)
            filename: Custom filename (extracted from URL if None)
            overwrite: Whether to overwrite existing files
            chunk_size: Download chunk size in bytes
        
        Returns:
            Download result with file path and metadata
        """
        session = await self._get_session()
        
        # Determine save path
        target_dir = save_path or self.download_dir
        target_dir.mkdir(parents=True, exist_ok=True)
        
        # Determine filename
        if not filename:
            filename = self._extract_filename(url)
        
        file_path = target_dir / filename
        
        # Check if file exists
        if file_path.exists() and not overwrite:
            return {
                "url": url,
                "file_path": str(file_path),
                "status": "exists",
                "message": "File already exists and overwrite is disabled"
            }
        
        try:
            # Start download
            async with session.stream("GET", url) as response:
                response.raise_for_status()
                
                # Get file size
                total_size = int(response.headers.get("content-length", 0))
                
                # Create file
                async with aiofiles.open(file_path, 'wb') as file:
                    downloaded = 0
                    
                    async for chunk in response.aiter_bytes(chunk_size=chunk_size):
                        await file.write(chunk)
                        downloaded += len(chunk)
                        
                        # Log progress for large files
                        if total_size > 0 and downloaded % (1024 * 1024) == 0:  # Every MB
                            progress = (downloaded / total_size) * 100
                            logger.info(f"Downloading {url}: {progress:.1f}% complete")
            
            # Get file info
            file_info = await self._get_file_info(file_path)
            
            result = {
                "url": url,
                "file_path": str(file_path),
                "filename": filename,
                "file_size": downloaded,
                "content_type": response.headers.get("content-type", ""),
                "file_info": file_info,
                "status": "success"
            }
            
            logger.info(f"Successfully downloaded {url} to {file_path}")
            return result
            
        except httpx.HTTPError as e:
            logger.error(f"HTTP error downloading {url}: {e}")
            
            # Clean up partial file
            if file_path.exists():
                file_path.unlink()
            
            return {
                "url": url,
                "error": str(e),
                "status": "error"
            }
        except Exception as e:
            logger.error(f"Unexpected error downloading {url}: {e}")
            
            # Clean up partial file
            if file_path.exists():
                file_path.unlink()
            
            return {
                "url": url,
                "error": str(e),
                "status": "error"
            }
    
    async def download_multiple(
        self,
        urls: List[str],
        concurrent: int = 3,
        **kwargs
    ) -> List[Dict[str, Any]]:
        """
        Download multiple files concurrently.
        
        Args:
            urls: List of URLs to download
            concurrent: Number of concurrent downloads
            **kwargs: Additional arguments for download method
        
        Returns:
            List of download results
        """
        semaphore = asyncio.Semaphore(concurrent)
        
        async def download_with_semaphore(url: str) -> Dict[str, Any]:
            async with semaphore:
                return await self.download(url, **kwargs)
        
        tasks = [download_with_semaphore(url) for url in urls]
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
    
    async def download_from_page(
        self,
        page_url: str,
        file_types: List[str] = None,
        max_files: int = 50
    ) -> List[Dict[str, Any]]:
        """
        Download all files of specified types from a web page.
        
        Args:
            page_url: URL of the web page
            file_types: List of file extensions to download
            max_files: Maximum number of files to download
        
        Returns:
            List of download results
        """
        # Import here to avoid circular imports
        from .browserless_scrape import BrowserlessScrape
        
        if file_types is None:
            file_types = ['.pdf', '.doc', '.docx', '.txt', '.csv', '.xlsx', '.ppt', '.pptx']
        
        # Scrape page for links
        scraper = BrowserlessScrape()
        
        try:
            scrape_result = await scraper.scrape(page_url)
            
            if scrape_result.get("status") != "success":
                return [{
                    "url": page_url,
                    "error": "Failed to scrape page",
                    "status": "error"
                }]
            
            # Extract file URLs
            file_urls = self._extract_file_urls(
                scrape_result.get("html", ""),
                page_url,
                file_types
            )
            
            # Limit number of files
            file_urls = file_urls[:max_files]
            
            # Download files
            download_results = await self.download_multiple(file_urls)
            
            return download_results
            
        finally:
            await scraper.close()
    
    def _extract_filename(self, url: str) -> str:
        """Extract filename from URL."""
        parsed = urllib.parse.urlparse(url)
        path = parsed.path
        
        # Get filename from path
        filename = os.path.basename(path)
        
        # If no filename, use domain
        if not filename:
            filename = parsed.netloc.replace('.', '_')
        
        # Clean filename
        filename = "".join(c for c in filename if c.isalnum() or c in ('-', '_', '.'))
        
        # Ensure filename has extension
        if '.' not in filename:
            filename += '.html'
        
        return filename
    
    async def _get_file_info(self, file_path: Path) -> Dict[str, Any]:
        """Get file information."""
        try:
            stat = file_path.stat()
            
            return {
                "size": stat.st_size,
                "created": stat.st_ctime,
                "modified": stat.st_mtime,
                "extension": file_path.suffix.lower(),
                "is_text": self._is_text_file(file_path),
                "mime_type": self._guess_mime_type(file_path)
            }
        except Exception as e:
            logger.error(f"Error getting file info for {file_path}: {e}")
            return {}
    
    def _is_text_file(self, file_path: Path) -> bool:
        """Check if file is likely a text file."""
        text_extensions = {
            '.txt', '.csv', '.json', '.xml', '.html', '.htm', '.md',
            '.py', '.js', '.css', '.log', '.yaml', '.yml', '.ini',
            '.cfg', '.conf', '.rtf', '.tex'
        }
        
        return file_path.suffix.lower() in text_extensions
    
    def _guess_mime_type(self, file_path: Path) -> str:
        """Guess MIME type based on file extension."""
        mime_types = {
            '.pdf': 'application/pdf',
            '.doc': 'application/msword',
            '.docx': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
            '.xls': 'application/vnd.ms-excel',
            '.xlsx': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            '.ppt': 'application/vnd.ms-powerpoint',
            '.pptx': 'application/vnd.openxmlformats-officedocument.presentationml.presentation',
            '.txt': 'text/plain',
            '.csv': 'text/csv',
            '.json': 'application/json',
            '.xml': 'application/xml',
            '.html': 'text/html',
            '.htm': 'text/html',
            '.md': 'text/markdown',
            '.png': 'image/png',
            '.jpg': 'image/jpeg',
            '.jpeg': 'image/jpeg',
            '.gif': 'image/gif',
            '.zip': 'application/zip',
            '.rar': 'application/x-rar-compressed'
        }
        
        return mime_types.get(file_path.suffix.lower(), 'application/octet-stream')
    
    def _extract_file_urls(
        self,
        html: str,
        base_url: str,
        file_types: List[str]
    ) -> List[str]:
        """Extract file URLs from HTML content."""
        from bs4 import BeautifulSoup
        
        soup = BeautifulSoup(html, 'html.parser')
        urls = []
        
        # Find all links
        for link in soup.find_all('a', href=True):
            href = link['href']
            
            # Check if link ends with any of the file types
            for file_type in file_types:
                if href.lower().endswith(file_type.lower()):
                    # Convert relative URLs to absolute
                    if href.startswith('/'):
                        parsed_base = urllib.parse.urlparse(base_url)
                        href = f"{parsed_base.scheme}://{parsed_base.netloc}{href}"
                    elif not href.startswith(('http://', 'https://')):
                        href = urllib.parse.urljoin(base_url, href)
                    
                    urls.append(href)
                    break
        
        # Remove duplicates
        return list(dict.fromkeys(urls))
    
    async def cleanup(self, max_age_days: int = 30) -> Dict[str, Any]:
        """
        Clean up old downloaded files.
        
        Args:
            max_age_days: Maximum age of files to keep in days
        
        Returns:
            Cleanup statistics
        """
        import time
        
        current_time = time.time()
        max_age_seconds = max_age_days * 24 * 60 * 60
        
        deleted_files = []
        deleted_size = 0
        
        try:
            for file_path in self.download_dir.rglob('*'):
                if file_path.is_file():
                    file_age = current_time - file_path.stat().st_mtime
                    
                    if file_age > max_age_seconds:
                        file_size = file_path.stat().st_size
                        file_path.unlink()
                        
                        deleted_files.append(str(file_path))
                        deleted_size += file_size
            
            return {
                "deleted_files": len(deleted_files),
                "deleted_size": deleted_size,
                "deleted_file_list": deleted_files
            }
            
        except Exception as e:
            logger.error(f"Error during cleanup: {e}")
            return {
                "deleted_files": 0,
                "deleted_size": 0,
                "error": str(e)
            }
    
    async def get_downloads_info(self) -> Dict[str, Any]:
        """Get information about downloaded files."""
        total_files = 0
        total_size = 0
        file_types = {}
        
        try:
            for file_path in self.download_dir.rglob('*'):
                if file_path.is_file():
                    total_files += 1
                    file_size = file_path.stat().st_size
                    total_size += file_size
                    
                    ext = file_path.suffix.lower()
                    file_types[ext] = file_types.get(ext, 0) + 1
            
            return {
                "total_files": total_files,
                "total_size": total_size,
                "download_dir": str(self.download_dir),
                "file_types": file_types
            }
            
        except Exception as e:
            logger.error(f"Error getting downloads info: {e}")
            return {
                "total_files": 0,
                "total_size": 0,
                "error": str(e)
            }
    
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
