"""
Local document parser for OpenDocGen.
"""

import os
import mimetypes
from typing import Any, Dict, List, Optional

from .unstructured_parser import UnstructuredParser


class LocalParser:
    """Handles local document parsing."""
    
    def __init__(self):
        """Initialize the parser."""
        self.unstructured_parser = UnstructuredParser()
    
    async def parse_document(self, file_path: str) -> Dict[str, Any]:
        """Parse a document and extract its content."""
        # Try unstructured first
        if self.unstructured_parser.is_supported(file_path):
            return await self.unstructured_parser.parse_document(file_path)
        
        # Fallback to basic parsing
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            return {
                "content": content,
                "metadata": {
                    "file_type": self._get_file_type(file_path),
                    "file_size": os.path.getsize(file_path),
                    "encoding": "utf-8",
                },
                "elements": [{"type": "text", "text": content}],
            }
        except Exception as e:
            return {
                "error": f"Failed to parse document: {str(e)}",
                "content": "",
                "metadata": {},
            }
    
    def _get_file_type(self, file_path: str) -> str:
        """Get file type based on extension."""
        mime_type, _ = mimetypes.guess_type(file_path)
        if mime_type:
            return mime_type.split('/')[0] if '/' in mime_type else mime_type
        return os.path.splitext(file_path)[1][1:].lower()
    
    def is_supported(self, file_path: str) -> bool:
        """Check if the file type is supported."""
        supported_extensions = ['.pdf', '.docx', '.txt', '.md', '.html', '.pptx', '.xlsx', '.csv', '.json']
        file_ext = os.path.splitext(file_path)[1].lower()
        return file_ext in supported_extensions
    
    def get_supported_formats(self) -> List[str]:
        """Get list of supported file formats."""
        return ['.pdf', '.docx', '.txt', '.md', '.html', '.pptx', '.xlsx', '.csv', '.json']
