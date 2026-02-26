"""
Analysis agent for data analysis and insights generation.
"""

from typing import Any, Dict, List

import pandas as pd

from .base_agent import BaseAgent
from ..tools.analysis_tools.code_executor import CodeExecutor
from ..tools.analysis_tools.data_visualizer import DataVisualizer
from ..tools.analysis_tools.statistical_tools import StatisticalTools


class AnalysisAgent(BaseAgent):
    """Agent specialized in data analysis and insights generation."""
    
    def __init__(self, **kwargs):
        """Initialize analysis agent."""
        super().__init__(
            name="Analysis Agent",
            role="Data Analysis Specialist",
            goal="Analyze data, generate insights, and create visualizations to support document generation",
            backstory=(
                "You are an expert data analyst with strong skills in statistical analysis, data visualization, "
                "and pattern recognition. You excel at extracting meaningful insights from complex datasets, "
                "identifying trends, and presenting findings in a clear and compelling manner. You are proficient "
                "in various analytical techniques and always ensure the accuracy and reliability of your analysis."
            ),
            **kwargs
        )
        
        # Initialize analysis tools
        self.code_executor = CodeExecutor()
        self.visualizer = DataVisualizer()
        self.stats_tools = StatisticalTools()
        
        # Add tools to agent
        self.add_tool(self.code_executor)
        self.add_tool(self.visualizer)
        self.add_tool(self.stats_tools)
    
    async def execute_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Execute an analysis task."""
        task_type = task.get("type", "statistical")
        
        if task_type == "statistical":
            return await self._perform_statistical_analysis(task)
        elif task_type == "visualization":
            return await self._create_visualizations(task)
        elif task_type == "code_analysis":
            return await self._analyze_code(task)
        elif task_type == "data_processing":
            return await self._process_data(task)
        elif task_type == "comprehensive_analysis":
            return await self._comprehensive_analysis(task)
        else:
            raise ValueError(f"Unknown task type: {task_type}")
    
    async def _perform_statistical_analysis(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Perform statistical analysis."""
        data = task.get("data")
        analysis_type = task.get("analysis_type", "descriptive")
        
        if not data:
            raise ValueError("Data is required for statistical analysis")
        
        # Convert to DataFrame if needed
        if isinstance(data, list):
            df = pd.DataFrame(data)
        elif isinstance(data, dict):
            df = pd.DataFrame([data])
        else:
            df = data
        
        # Perform analysis based on type
        if analysis_type == "descriptive":
            results = await self.stats_tools.descriptive_analysis(df)
        elif analysis_type == "correlation":
            results = await self.stats_tools.correlation_analysis(df)
        elif analysis_type == "regression":
            results = await self.stats_tools.regression_analysis(df, task.get("target_column"))
        else:
            results = await self.stats_tools.custom_analysis(df, task.get("custom_code"))
        
        return {
            "type": "statistical_analysis",
            "analysis_type": analysis_type,
            "results": results,
            "data_shape": df.shape,
            "columns": list(df.columns)
        }
    
    async def _create_visualizations(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Create data visualizations."""
        data = task.get("data")
        chart_types = task.get("chart_types", ["bar"])
        
        if not data:
            raise ValueError("Data is required for visualization")
        
        # Convert to DataFrame
        if isinstance(data, list):
            df = pd.DataFrame(data)
        elif isinstance(data, dict):
            df = pd.DataFrame([data])
        else:
            df = data
        
        visualizations = []
        for chart_type in chart_types:
            try:
                chart_path = await self.visualizer.create_chart(
                    df, chart_type, task.get("chart_config", {})
                )
                visualizations.append({
                    "chart_type": chart_type,
                    "chart_path": chart_path,
                    "status": "success"
                })
            except Exception as e:
                visualizations.append({
                    "chart_type": chart_type,
                    "error": str(e),
                    "status": "error"
                })
        
        return {
            "type": "visualizations",
            "charts": visualizations,
            "total_charts": len(chart_types),
            "successful_charts": len([v for v in visualizations if v["status"] == "success"])
        }
    
    async def _analyze_code(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze code and provide insights."""
        code = task.get("code")
        language = task.get("language", "python")
        
        if not code:
            raise ValueError("Code is required for code analysis")
        
        # Execute code and analyze results
        execution_result = await self.code_executor.execute_code(code, language)
        
        # Generate analysis prompt
        analysis_prompt = f"""
        Analyze the following {language} code and its execution results:
        
        Code:
        ```{language}
        {code}
        ```
        
        Execution Results:
        {execution_result}
        
        Please provide:
        1. Code quality assessment
        2. Performance considerations
        3. Potential improvements
        4. Security considerations
        5. Best practices recommendations
        """
        
        analysis = await self.think(analysis_prompt)
        
        return {
            "type": "code_analysis",
            "language": language,
            "execution_result": execution_result,
            "analysis": analysis,
            "recommendations": self._generate_code_recommendations(code, execution_result)
        }
    
    async def _process_data(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Process and transform data."""
        data = task.get("data")
        operations = task.get("operations", [])
        
        if not data:
            raise ValueError("Data is required for data processing")
        
        # Convert to DataFrame
        if isinstance(data, list):
            df = pd.DataFrame(data)
        elif isinstance(data, dict):
            df = pd.DataFrame([data])
        else:
            df = data
        
        processed_data = df.copy()
        operations_performed = []
        
        for operation in operations:
            op_type = operation.get("type")
            
            try:
                if op_type == "filter":
                    condition = operation.get("condition")
                    processed_data = processed_data.query(condition)
                elif op_type == "group":
                    group_by = operation.get("group_by")
                    agg_func = operation.get("agg_func")
                    processed_data = processed_data.groupby(group_by).agg(agg_func).reset_index()
                elif op_type == "sort":
                    sort_by = operation.get("sort_by")
                    ascending = operation.get("ascending", True)
                    processed_data = processed_data.sort_values(sort_by, ascending=ascending)
                elif op_type == "rename":
                    columns = operation.get("columns")
                    processed_data = processed_data.rename(columns=columns)
                elif op_type == "drop":
                    columns = operation.get("columns")
                    processed_data = processed_data.drop(columns=columns)
                
                operations_performed.append({
                    "type": op_type,
                    "status": "success"
                })
            except Exception as e:
                operations_performed.append({
                    "type": op_type,
                    "error": str(e),
                    "status": "error"
                })
        
        return {
            "type": "data_processing",
            "original_shape": df.shape,
            "processed_shape": processed_data.shape,
            "operations": operations_performed,
            "processed_data": processed_data.to_dict("records")
        }
    
    async def _comprehensive_analysis(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Perform comprehensive data analysis."""
        data = task.get("data")
        analysis_goals = task.get("goals", [])
        
        if not data:
            raise ValueError("Data is required for comprehensive analysis")
        
        # Step 1: Statistical analysis
        stats_results = await self._perform_statistical_analysis({
            "data": data,
            "analysis_type": "descriptive"
        })
        
        # Step 2: Create visualizations
        viz_results = await self._create_visualizations({
            "data": data,
            "chart_types": ["bar", "line", "scatter"]
        })
        
        # Step 3: Data processing if needed
        processed_results = None
        if task.get("enable_processing", False):
            processed_results = await self._process_data({
                "data": data,
                "operations": task.get("processing_operations", [])
            })
        
        # Step 4: Generate insights
        insights_prompt = f"""
        Based on the following analysis results, provide comprehensive insights and recommendations:
        
        Statistical Analysis:
        {stats_results}
        
        Visualizations:
        {viz_results}
        
        Analysis Goals:
        {analysis_goals}
        
        Please provide:
        1. Key findings and patterns
        2. Data quality assessment
        3. Statistical significance
        4. Business insights
        5. Recommendations for further analysis
        """
        
        insights = await self.think(insights_prompt)
        
        return {
            "type": "comprehensive_analysis",
            "statistical_analysis": stats_results,
            "visualizations": viz_results,
            "data_processing": processed_results,
            "insights": insights,
            "recommendations": self._generate_analysis_recommendations(stats_results, viz_results)
        }
    
    def _generate_code_recommendations(self, code: str, execution_result: Any) -> List[str]:
        """Generate code improvement recommendations."""
        recommendations = []
        
        # Basic code analysis
        if len(code.split('\n')) > 50:
            recommendations.append("Consider breaking down the code into smaller functions")
        
        if "import" not in code.lower():
            recommendations.append("Consider adding necessary imports")
        
        if "print(" in code:
            recommendations.append("Consider using logging instead of print statements")
        
        # Execution result analysis
        if execution_result and "error" in str(execution_result).lower():
            recommendations.append("Fix execution errors before proceeding")
        
        recommendations.extend([
            "Add error handling and validation",
            "Include docstrings and comments",
            "Consider performance optimizations",
            "Add unit tests for critical functionality"
        ])
        
        return recommendations
    
    def _generate_analysis_recommendations(self, stats_results: Dict, viz_results: Dict) -> List[str]:
        """Generate analysis recommendations."""
        recommendations = []
        
        # Based on statistical results
        if stats_results.get("results"):
            recommendations.append("Review statistical significance of findings")
        
        # Based on visualization results
        successful_viz = len([v for v in viz_results.get("charts", []) if v["status"] == "success"])
        if successful_viz < len(viz_results.get("charts", [])):
            recommendations.append("Address visualization errors for complete analysis")
        
        recommendations.extend([
            "Validate findings with domain experts",
            "Consider additional data sources for context",
            "Perform sensitivity analysis if applicable",
            "Document assumptions and limitations",
            "Create executive summary of key findings"
        ])
        
        return recommendations
