"""
Data visualization tool for OpenDocGen.
"""

import asyncio
from typing import Any, Dict, List, Optional
import io
import base64

try:
    import matplotlib.pyplot as plt
    import seaborn as sns
    import pandas as pd
    VISUALIZATION_AVAILABLE = True
except ImportError:
    VISUALIZATION_AVAILABLE = False
    plt = None
    sns = None
    pd = None


class DataVisualizer:
    """Handles data visualization for analysis results."""
    
    def __init__(self):
        """Initialize the data visualizer."""
        self.available = VISUALIZATION_AVAILABLE
        self.supported_charts = ["line", "bar", "scatter", "histogram", "heatmap", "pie"]
    
    async def create_chart(self, data: Dict[str, Any], chart_type: str = "auto", **kwargs) -> Dict[str, Any]:
        """Create a chart from data."""
        if not self.available:
            return {
                "error": "Visualization libraries not available",
                "chart_base64": None,
            }
        
        try:
            # Convert data to DataFrame if possible
            df = self._convert_to_dataframe(data)
            if df is None:
                return {
                    "error": "Invalid data format for visualization",
                    "chart_base64": None,
                }
            
            # Create the plot
            plt.figure(figsize=kwargs.get('figsize', (10, 6)))
            
            if chart_type == "auto":
                chart_type = self._detect_chart_type(df)
            else:
                chart_type = chart_type
            
            # Generate the chart based on type
            if chart_type == "line":
                self._create_line_chart(df, **kwargs)
            elif chart_type == "bar":
                self._create_bar_chart(df, **kwargs)
            elif chart_type == "scatter":
                self._create_scatter_chart(df, **kwargs)
            elif chart_type == "histogram":
                self._create_histogram(df, **kwargs)
            elif chart_type == "heatmap":
                self._create_heatmap(df, **kwargs)
            elif chart_type == "pie":
                self._create_pie_chart(df, **kwargs)
            else:
                return {
                    "error": f"Unsupported chart type: {chart_type}",
                    "chart_base64": None,
                }
            
            # Save plot to base64
            buffer = io.BytesIO()
            plt.savefig(buffer, format='png', dpi=300, bbox_inches='tight')
            buffer.seek(0)
            chart_base64 = base64.b64encode(buffer.getvalue()).decode()
            plt.close()
            
            return {
                "success": True,
                "chart_type": chart_type,
                "chart_base64": chart_base64,
                "data_summary": self._summarize_data(df),
            }
            
        except Exception as e:
            return {
                "error": f"Chart creation failed: {str(e)}",
                "chart_base64": None,
            }
    
    def _convert_to_dataframe(self, data: Dict[str, Any]) -> Optional[Any]:
        """Convert data dictionary to pandas DataFrame."""
        try:
            if pd and isinstance(data, dict):
                # Try to create DataFrame from dict
                if all(isinstance(v, list) for v in data.values()):
                    return pd.DataFrame(data)
                else:
                    # For single values, create a simple DataFrame
                    return pd.DataFrame(list(data.items()), columns=['key', 'value'])
            return None
        except:
            return None
    
    def _detect_chart_type(self, df) -> str:
        """Auto-detect the best chart type for the data."""
        try:
            if df is None or df.empty:
                return "bar"
            
            # Simple heuristics for chart type detection
            numeric_columns = df.select_dtypes(include=['number']).columns.tolist()
            
            if len(numeric_columns) >= 2:
                return "scatter"  # Good for correlation
            elif len(numeric_columns) == 1:
                return "histogram"  # Good for distribution
            else:
                return "bar"  # Default to bar
        except:
            return "bar"
    
    def _create_line_chart(self, df, **kwargs):
        """Create a line chart."""
        x_col = kwargs.get('x_column', df.columns[0] if len(df.columns) > 0 else 'index')
        y_cols = [col for col in df.columns if col != x_col]
        
        for col in y_cols:
            plt.plot(df[x_col], df[col], label=col, marker='o')
        
        plt.xlabel(kwargs.get('x_label', x_col))
        plt.ylabel(kwargs.get('y_label', 'Values'))
        plt.title(kwargs.get('title', 'Line Chart'))
        plt.legend()
        plt.grid(True, alpha=0.3)
    
    def _create_bar_chart(self, df, **kwargs):
        """Create a bar chart."""
        x_col = kwargs.get('x_column', df.columns[0] if len(df.columns) > 0 else 'index')
        y_col = kwargs.get('y_column', df.columns[1] if len(df.columns) > 1 else df.columns[0])
        
        plt.bar(df[x_col], df[y_col])
        plt.xlabel(kwargs.get('x_label', x_col))
        plt.ylabel(kwargs.get('y_label', y_col))
        plt.title(kwargs.get('title', 'Bar Chart'))
        plt.xticks(rotation=45)
    
    def _create_scatter_chart(self, df, **kwargs):
        """Create a scatter plot."""
        x_col = kwargs.get('x_column', df.columns[0] if len(df.columns) > 0 else 'index')
        y_col = kwargs.get('y_column', df.columns[1] if len(df.columns) > 1 else df.columns[0])
        
        plt.scatter(df[x_col], df[y_col], alpha=0.6)
        plt.xlabel(kwargs.get('x_label', x_col))
        plt.ylabel(kwargs.get('y_label', y_col))
        plt.title(kwargs.get('title', 'Scatter Plot'))
        plt.grid(True, alpha=0.3)
    
    def _create_histogram(self, df, **kwargs):
        """Create a histogram."""
        col = kwargs.get('column', df.select_dtypes(include=['number']).columns[0] if len(df.select_dtypes(include=['number']).columns) > 0 else df.columns[0])
        
        plt.hist(df[col], bins=kwargs.get('bins', 30), alpha=0.7)
        plt.xlabel(kwargs.get('x_label', col))
        plt.ylabel(kwargs.get('y_label', 'Frequency'))
        plt.title(kwargs.get('title', 'Histogram'))
        plt.grid(True, alpha=0.3)
    
    def _create_heatmap(self, df, **kwargs):
        """Create a heatmap."""
        # Select only numeric columns
        numeric_df = df.select_dtypes(include=['number'])
        if numeric_df.empty:
            return
        
        correlation_matrix = numeric_df.corr()
        
        sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', center=0)
        plt.title(kwargs.get('title', 'Correlation Heatmap'))
    
    def _create_pie_chart(self, df, **kwargs):
        """Create a pie chart."""
        col = kwargs.get('column', df.columns[0] if len(df.columns) > 0 else df.columns[0])
        
        # For pie chart, we need value counts
        if df[col].dtype in ['object', 'category']:
            value_counts = df[col].value_counts()
            plt.pie(value_counts.values, labels=value_counts.index, autopct='%1.1f%%')
        else:
            # For numeric data, create ranges
            df[col] = pd.cut(df[col], bins=5, labels=['Very Low', 'Low', 'Medium', 'High', 'Very High'])
            value_counts = df[col].value_counts()
            plt.pie(value_counts.values, labels=value_counts.index, autopct='%1.1f%%')
        
        plt.title(kwargs.get('title', 'Pie Chart'))
    
    def _summarize_data(self, df) -> Dict[str, Any]:
        """Summarize the dataset."""
        try:
            summary = {
                "rows": len(df),
                "columns": list(df.columns),
                "dtypes": df.dtypes.to_dict(),
                "null_counts": df.isnull().sum().to_dict(),
                "numeric_summary": df.describe().to_dict() if len(df.select_dtypes(include=['number']).columns) > 0 else {},
            }
            return summary
        except:
            return {"error": "Failed to summarize data"}
    
    def get_supported_charts(self) -> List[str]:
        """Get list of supported chart types."""
        return self.supported_charts
    
    def is_available(self) -> bool:
        """Check if visualization libraries are available."""
        return self.available
