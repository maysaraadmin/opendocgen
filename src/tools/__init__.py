"""
Tools module for OpenDocGen agents.
"""

# Web tools
from .web_tools.searxng_search import SearxNGSearch
from .web_tools.browserless_scrape import BrowserlessScrape
from .web_tools.download_manager import DownloadManager

# Document tools
from .document_tools.unstructured_parser import UnstructuredParser
from .document_tools.local_parser import LocalParser
from .document_tools.template_manager import TemplateManager

# Analysis tools
from .analysis_tools.code_executor import CodeExecutor
from .analysis_tools.code_generator import CodeGenerator
from .analysis_tools.data_visualizer import DataVisualizer
from .analysis_tools.statistical_tools import StatisticalTools

# Utility tools
from .utility_tools.file_manager import FileManager
from .utility_tools.text_processors import TextProcessors

__all__ = [
    # Web tools
    "SearxNGSearch",
    "BrowserlessScrape", 
    "DownloadManager",
    
    # Document tools
    "UnstructuredParser",
    "LocalParser",
    "TemplateManager",
    
    # Analysis tools
    "CodeExecutor",
    "CodeGenerator",
    "DataVisualizer",
    "StatisticalTools",
    
    # Utility tools
    "FileManager",
    "TextProcessors",
]
