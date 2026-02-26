"""
File management utilities for OpenDocGen.
"""

import os
import shutil
from pathlib import Path
from typing import Any, Dict, List, Optional, Union
import asyncio
import aiofiles


class FileManager:
    """Handles file operations for document processing."""
    
    def __init__(self, base_path: Optional[str] = None):
        """Initialize file manager."""
        self.base_path = Path(base_path) if base_path else Path.cwd()
        self.supported_formats = ['.txt', '.md', '.pdf', '.docx', '.html', '.json', '.csv']
    
    async def read_file(self, file_path: str) -> Dict[str, Any]:
        """Read file content asynchronously."""
        try:
            path = Path(file_path)
            if not path.exists():
                return {"error": f"File not found: {file_path}"}
            
            async with aiofiles.open(file_path, 'r', encoding='utf-8') as f:
                content = await f.read()
            
            return {
                "success": True,
                "content": content,
                "size": path.stat().st_size,
                "format": path.suffix,
                "path": str(path.absolute()),
            }
            
        except Exception as e:
            return {"error": f"Failed to read file: {str(e)}"}
    
    async def write_file(self, file_path: str, content: str, overwrite: bool = True) -> Dict[str, Any]:
        """Write file content asynchronously."""
        try:
            path = Path(file_path)
            
            # Create directory if it doesn't exist
            path.parent.mkdir(parents=True, exist_ok=True)
            
            # Check if file exists and overwrite is False
            if path.exists() and not overwrite:
                return {"error": f"File already exists: {file_path}"}
            
            async with aiofiles.open(file_path, 'w', encoding='utf-8') as f:
                await f.write(content)
            
            return {
                "success": True,
                "path": str(path.absolute()),
                "size": len(content.encode('utf-8')),
                "format": path.suffix,
            }
            
        except Exception as e:
            return {"error": f"Failed to write file: {str(e)}"}
    
    async def delete_file(self, file_path: str) -> Dict[str, Any]:
        """Delete file asynchronously."""
        try:
            path = Path(file_path)
            if not path.exists():
                return {"error": f"File not found: {file_path}"}
            
            path.unlink()
            
            return {
                "success": True,
                "message": f"File deleted: {file_path}",
            }
            
        except Exception as e:
            return {"error": f"Failed to delete file: {str(e)}"}
    
    async def list_files(self, directory: str = None, pattern: str = "*") -> Dict[str, Any]:
        """List files in directory asynchronously."""
        try:
            base_dir = Path(directory) if directory else self.base_path
            
            if not base_dir.exists():
                return {"error": f"Directory not found: {directory}"}
            
            files = []
            for file_path in base_dir.glob(pattern):
                if file_path.is_file():
                    files.append({
                        "name": file_path.name,
                        "path": str(file_path.absolute()),
                        "size": file_path.stat().st_size,
                        "format": file_path.suffix,
                        "modified": file_path.stat().st_mtime,
                    })
            
            return {
                "success": True,
                "files": files,
                "count": len(files),
                "directory": str(base_dir.absolute()),
            }
            
        except Exception as e:
            return {"error": f"Failed to list files: {str(e)}"}
    
    async def create_directory(self, directory_path: str) -> Dict[str, Any]:
        """Create directory asynchronously."""
        try:
            path = Path(directory_path)
            path.mkdir(parents=True, exist_ok=True)
            
            return {
                "success": True,
                "path": str(path.absolute()),
                "message": f"Directory created: {directory_path}",
            }
            
        except Exception as e:
            return {"error": f"Failed to create directory: {str(e)}"}
    
    async def copy_file(self, source: str, destination: str) -> Dict[str, Any]:
        """Copy file asynchronously."""
        try:
            source_path = Path(source)
            dest_path = Path(destination)
            
            if not source_path.exists():
                return {"error": f"Source file not found: {source}"}
            
            # Create destination directory if it doesn't exist
            dest_path.parent.mkdir(parents=True, exist_ok=True)
            
            shutil.copy2(source_path, dest_path)
            
            return {
                "success": True,
                "source": str(source_path.absolute()),
                "destination": str(dest_path.absolute()),
                "size": dest_path.stat().st_size,
            }
            
        except Exception as e:
            return {"error": f"Failed to copy file: {str(e)}"}
    
    async def move_file(self, source: str, destination: str) -> Dict[str, Any]:
        """Move file asynchronously."""
        try:
            source_path = Path(source)
            dest_path = Path(destination)
            
            if not source_path.exists():
                return {"error": f"Source file not found: {source}"}
            
            # Create destination directory if it doesn't exist
            dest_path.parent.mkdir(parents=True, exist_ok=True)
            
            shutil.move(str(source_path), str(dest_path))
            
            return {
                "success": True,
                "source": str(source_path.absolute()),
                "destination": str(dest_path.absolute()),
                "message": f"File moved from {source} to {destination}",
            }
            
        except Exception as e:
            return {"error": f"Failed to move file: {str(e)}"}
    
    def get_file_info(self, file_path: str) -> Dict[str, Any]:
        """Get file information."""
        try:
            path = Path(file_path)
            if not path.exists():
                return {"error": f"File not found: {file_path}"}
            
            stat = path.stat()
            
            return {
                "success": True,
                "name": path.name,
                "path": str(path.absolute()),
                "size": stat.st_size,
                "format": path.suffix,
                "created": stat.st_ctime,
                "modified": stat.st_mtime,
                "is_file": path.is_file(),
                "is_directory": path.is_dir(),
                "parent": str(path.parent.absolute()),
            }
            
        except Exception as e:
            return {"error": f"Failed to get file info: {str(e)}"}
    
    def is_supported_format(self, file_path: str) -> bool:
        """Check if file format is supported."""
        return Path(file_path).suffix.lower() in self.supported_formats
    
    def get_supported_formats(self) -> List[str]:
        """Get list of supported file formats."""
        return self.supported_formats
    
    async def clean_directory(self, directory: str, keep_hidden: bool = False) -> Dict[str, Any]:
        """Clean directory by removing all files."""
        try:
            path = Path(directory)
            if not path.exists():
                return {"error": f"Directory not found: {directory}"}
            
            removed_files = []
            for item in path.iterdir():
                item_path = path / item
                
                # Skip hidden files if requested
                if not keep_hidden and item.startswith('.'):
                    continue
                
                if item_path.is_file():
                    item_path.unlink()
                    removed_files.append(str(item_path))
                elif item_path.is_dir():
                    shutil.rmtree(item_path)
                    removed_files.append(str(item_path))
            
            return {
                "success": True,
                "removed_files": removed_files,
                "count": len(removed_files),
                "directory": str(path.absolute()),
            }
            
        except Exception as e:
            return {"error": f"Failed to clean directory: {str(e)}"}
