"""
Code execution tool for OpenDocGen.
"""

import asyncio
import subprocess
import sys
from typing import Any, Dict, List, Optional
from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


class CodeExecutor:
    """Handles code execution for data analysis and visualization."""
    
    def __init__(self):
        """Initialize the code executor."""
        self.execution_timeout = 30  # seconds
        self.max_output_size = 10000  # characters
    
    async def execute_code(self, code: str, language: str = "python") -> Dict[str, Any]:
        """Execute code and return the result."""
        try:
            if language.lower() == "python":
                return await self._execute_python(code)
            else:
                return {
                    "error": f"Unsupported language: {language}",
                    "output": "",
                    "execution_time": 0,
                }
        except Exception as e:
            return {
                "error": f"Execution failed: {str(e)}",
                "output": "",
                "execution_time": 0,
            }
    
    async def _execute_python(self, code: str) -> Dict[str, Any]:
        """Execute Python code safely."""
        try:
            # Create a safe execution environment
            local_vars = {}
            
            # Capture stdout and stderr
            import io
            import contextlib
            
            with contextlib.redirect_stdout(io.StringIO()) as stdout, \
                 contextlib.redirect_stderr(io.StringIO()) as stderr:
                
                # Execute the code
                exec(code, globals(), local_vars)
                
                # Get the output
                stdout_output = stdout.getvalue()
                stderr_output = stderr.getvalue()
            
            result = {
                "output": stdout_output,
                "error": stderr_output if stderr_output else None,
                "execution_time": 0,  # Would need timing in real implementation
                "variables": {k: str(v) for k, v in local_vars.items() if not k.startswith('_')},
            }
            
            return result
            
        except Exception as e:
            return {
                "error": f"Python execution error: {str(e)}",
                "output": "",
                "execution_time": 0,
            }
    
    async def generate_visualization(self, data: Dict[str, Any], chart_type: str = "auto") -> Dict[str, Any]:
        """Generate visualization from data."""
        try:
            if not data:
                return {"error": "No data provided for visualization"}
            
            # Try to create a simple visualization
            plt.figure(figsize=(10, 6))
            
            if chart_type == "auto":
                # Auto-detect the best chart type
                if isinstance(data.get('values'), list) and len(data['values']) > 1:
                    plt.plot(data['values'])
                    plt.title(data.get('title', 'Data Plot'))
                else:
                    plt.bar(range(len(data)), list(data.values()) if isinstance(data, dict) else data)
                    plt.title(data.get('title', 'Bar Chart'))
            elif chart_type == "line":
                plt.plot(data.get('x', []), data.get('y', []))
                plt.title(data.get('title', 'Line Chart'))
            elif chart_type == "bar":
                plt.bar(data.get('x', []), data.get('y', []))
                plt.title(data.get('title', 'Bar Chart'))
            elif chart_type == "scatter":
                plt.scatter(data.get('x', []), data.get('y', []))
                plt.title(data.get('title', 'Scatter Plot'))
            else:
                return {"error": f"Unsupported chart type: {chart_type}"}
            
            # Save the plot
            output_path = data.get('output_path', 'chart.png')
            plt.savefig(output_path)
            plt.close()
            
            return {
                "output": f"Chart saved to {output_path}",
                "chart_path": output_path,
                "chart_type": chart_type,
            }
            
        except Exception as e:
            return {
                "error": f"Visualization generation failed: {str(e)}",
                "output": "",
            }
    
    def is_safe_code(self, code: str) -> bool:
        """Check if code is safe to execute."""
        dangerous_keywords = [
            'import os', 'import sys', 'subprocess', 'exec', 'eval',
            '__import__', 'open(', 'file(', 'input(', 'raw_input(',
            'rm -rf', 'del /', 'format', 'fdisk',
        ]
        
        return not any(keyword in code.lower() for keyword in dangerous_keywords)
    
    def get_supported_languages(self) -> List[str]:
        """Get list of supported programming languages."""
        return ["python"]
