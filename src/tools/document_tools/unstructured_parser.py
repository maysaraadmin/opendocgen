"""
Unstructured document parser for OpenDocGen.
"""

import os
from typing import Any, Dict, List, Optional

try:
    from unstructured.partition.auto import partition
    from unstructured.staging.base import initialize
except ImportError:
    print("Warning: unstructured not installed. Using mock implementation.")
    partition = None
    initialize = None


class UnstructuredParser:
    """Handles document parsing using unstructured library."""
    
    def __init__(self):
        """Initialize the parser."""
        self.initialized = False
        if initialize:
            try:
                initialize()
                self.initialized = True
            except Exception as e:
                print(f"Failed to initialize unstructured: {e}")
    
    async def parse_document(self, file_path: str) -> Dict[str, Any]:
        """Parse a document and extract its content."""
        if not partition:
            return {
                "error": "unstructured not available",
                "content": "",
                "metadata": {},
            }
        
        try:
            # Partition the document
            elements = partition(file_path)
            
            # Extract text content
            content = "\n".join([str(element) for element in elements])
            
            # Extract metadata
            metadata = {
                "file_type": elements[0].type if elements else "unknown",
                "element_count": len(elements),
                "languages": list(set([element.metadata.get("languages", []) for element in elements])),
            }
            
            return {
                "content": content,
                "metadata": metadata,
                "elements": [{"type": str(type(element)), "text": str(element)} for element in elements],
            }
            
        except Exception as e:
            return {
                "error": f"Failed to parse document: {str(e)}",
                "content": "",
                "metadata": {},
            }
    
    def is_supported(self, file_path: str) -> bool:
        """Check if the file type is supported."""
        if not partition:
            return False
        
        supported_extensions = ['.pdf', '.docx', '.txt', '.md', '.html', '.pptx', '.xlsx']
        file_ext = os.path.splitext(file_path)[1].lower()
        return file_ext in supported_extensions
    
    def get_supported_formats(self) -> List[str]:
        """Get list of supported file formats."""
        return ['.pdf', '.docx', '.txt', '.md', '.html', '.pptx', '.xlsx']
