"""
Web tools for OpenDocGen agents.
"""

from .searxng_search import SearxNGSearch
from .browserless_scrape import BrowserlessScrape
from .download_manager import DownloadManager

__all__ = ["SearxNGSearch", "BrowserlessScrape", "DownloadManager"]
