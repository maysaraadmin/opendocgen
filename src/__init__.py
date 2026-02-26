"""
OpenDocGen - AI-powered Document Generation System

A comprehensive framework for automated document generation using AI agents,
specialized tools, and advanced workflows.
"""

__version__ = "0.1.0"
__author__ = "OpenDocGen Team"
__email__ = "team@opendocgen.com"

from .main import OpenDocGen
from .config import Config

__all__ = ["OpenDocGen", "Config"]
