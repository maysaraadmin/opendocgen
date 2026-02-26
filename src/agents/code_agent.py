"""
Code agent for code generation and execution.
"""

from typing import Any, Dict, List

from .base_agent import BaseAgent
from ..tools.analysis_tools.code_executor import CodeExecutor
from ..tools.analysis_tools.code_generator import CodeGenerator


class CodeAgent(BaseAgent):
    """Agent specialized in code generation and execution."""
    
    def __init__(self, **kwargs):
        """Initialize code agent."""
        super().__init__(
            name="Code Agent",
            role="Code Generation and Execution Specialist",
            goal="Generate, execute, and optimize code to support document generation and data analysis tasks",
            backstory=(
                "You are an expert software developer with extensive experience in multiple programming languages, "
                "data analysis, and automation. You excel at writing clean, efficient, and well-documented code. "
                "You are proficient in Python, JavaScript, data analysis libraries, and various frameworks. "
                "You always follow best practices, write comprehensive tests, and ensure code security and performance."
            ),
            **kwargs
        )
        
        # Initialize code tools
        self.code_executor = CodeExecutor()
        self.code_generator = CodeGenerator()
        
        # Add tools to agent
        self.add_tool(self.code_executor)
        self.add_tool(self.code_generator)
    
    async def execute_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a code-related task."""
        task_type = task.get("type", "generate")
        
        if task_type == "generate":
            return await self._generate_code(task)
        elif task_type == "execute":
            return await self._execute_code(task)
        elif task_type == "debug":
            return await self._debug_code(task)
        elif task_type == "optimize":
            return await self._optimize_code(task)
        elif task_type == "test":
            return await self._generate_tests(task)
        elif task_type == "document":
            return await self._document_code(task)
        else:
            raise ValueError(f"Unknown task type: {task_type}")
    
    async def _generate_code(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Generate code based on requirements."""
        requirements = task.get("requirements", "")
        language = task.get("language", "python")
        context = task.get("context", {})
        examples = task.get("examples", [])
        
        if not requirements:
            raise ValueError("Requirements are required for code generation")
        
        # Create code generation prompt
        prompt = self._create_code_generation_prompt(
            requirements, language, context, examples
        )
        
        # Generate code
        generated_code = await self.think(prompt)
        
        # Validate and format code
        formatted_code = await self.code_generator.format_code(generated_code, language)
        
        return {
            "type": "generated_code",
            "language": language,
            "requirements": requirements,
            "generated_code": formatted_code,
            "lines_of_code": len(formatted_code.split('\n')),
            "estimated_complexity": self._estimate_complexity(formatted_code)
        }
    
    async def _execute_code(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Execute code and return results."""
        code = task.get("code")
        language = task.get("language", "python")
        inputs = task.get("inputs", {})
        timeout = task.get("timeout", 30)
        
        if not code:
            raise ValueError("Code is required for execution")
        
        # Execute code
        execution_result = await self.code_executor.execute_code(
            code, language, inputs, timeout
        )
        
        # Analyze execution results
        analysis = await self._analyze_execution_results(execution_result)
        
        return {
            "type": "execution_result",
            "language": language,
            "code": code,
            "execution_result": execution_result,
            "analysis": analysis,
            "success": execution_result.get("status") == "success"
        }
    
    async def _debug_code(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Debug code and provide fixes."""
        code = task.get("code")
        error_message = task.get("error_message", "")
        language = task.get("language", "python")
        
        if not code:
            raise ValueError("Code is required for debugging")
        
        # Create debugging prompt
        prompt = f"""
        Debug the following {language} code that has an error:
        
        Code:
        ```{language}
        {code}
        ```
        
        Error Message:
        {error_message}
        
        Please provide:
        1. Root cause analysis
        2. Fixed code
        3. Explanation of the fix
        4. Prevention recommendations
        """
        
        debug_response = await self.think(prompt)
        
        # Extract fixed code (in a real implementation, this would be more sophisticated)
        fixed_code = await self._extract_fixed_code(debug_response, code)
        
        # Test the fix
        test_result = None
        if fixed_code and fixed_code != code:
            test_result = await self.code_executor.execute_code(fixed_code, language)
        
        return {
            "type": "debug_result",
            "language": language,
            "original_code": code,
            "error_message": error_message,
            "fixed_code": fixed_code,
            "debug_analysis": debug_response,
            "test_result": test_result,
            "fix_successful": test_result and test_result.get("status") == "success"
        }
    
    async def _optimize_code(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Optimize code for performance and readability."""
        code = task.get("code")
        optimization_type = task.get("optimization_type", "performance")
        language = task.get("language", "python")
        
        if not code:
            raise ValueError("Code is required for optimization")
        
        # Create optimization prompt
        prompt = f"""
        Optimize the following {language} code for {optimization_type}:
        
        Code:
        ```{language}
        {code}
        ```
        
        Please provide:
        1. Optimized code
        2. Performance improvements
        3. Readability enhancements
        4. Trade-offs and considerations
        """
        
        optimization_response = await self.think(prompt)
        
        # Extract optimized code
        optimized_code = await self._extract_optimized_code(optimization_response, code)
        
        # Benchmark if possible
        benchmark_results = None
        if optimized_code and optimized_code != code:
            benchmark_results = await self._benchmark_code(code, optimized_code, language)
        
        return {
            "type": "optimization_result",
            "language": language,
            "optimization_type": optimization_type,
            "original_code": code,
            "optimized_code": optimized_code,
            "optimization_analysis": optimization_response,
            "benchmark_results": benchmark_results,
            "improvement_estimated": benchmark_results and benchmark_results.get("improvement", 0)
        }
    
    async def _generate_tests(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Generate unit tests for code."""
        code = task.get("code")
        test_framework = task.get("test_framework", "pytest")
        language = task.get("language", "python")
        coverage_target = task.get("coverage_target", 80)
        
        if not code:
            raise ValueError("Code is required for test generation")
        
        # Create test generation prompt
        prompt = f"""
        Generate comprehensive unit tests for the following {language} code using {test_framework}:
        
        Code:
        ```{language}
        {code}
        ```
        
        Target coverage: {coverage_target}%
        
        Please provide:
        1. Complete test suite
        2. Test cases for edge cases
        3. Mock implementations if needed
        4. Test documentation
        """
        
        test_response = await self.think(prompt)
        
        # Extract test code
        test_code = await self._extract_test_code(test_response)
        
        # Run tests if possible
        test_results = None
        if test_code:
            test_results = await self.code_executor.run_tests(test_code, test_framework)
        
        return {
            "type": "generated_tests",
            "language": language,
            "test_framework": test_framework,
            "original_code": code,
            "test_code": test_code,
            "test_analysis": test_response,
            "test_results": test_results,
            "coverage_achieved": test_results and test_results.get("coverage", 0)
        }
    
    async def _document_code(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Generate documentation for code."""
        code = task.get("code")
        doc_type = task.get("doc_type", "comprehensive")
        language = task.get("language", "python")
        format_type = task.get("format_type", "markdown")
        
        if not code:
            raise ValueError("Code is required for documentation")
        
        # Create documentation prompt
        prompt = f"""
        Generate {doc_type} documentation for the following {language} code in {format_type} format:
        
        Code:
        ```{language}
        {code}
        ```
        
        Please provide:
        1. Function/class descriptions
        2. Parameter documentation
        3. Return value documentation
        4. Usage examples
        5. Error handling information
        """
        
        documentation = await self.think(prompt)
        
        return {
            "type": "generated_documentation",
            "language": language,
            "doc_type": doc_type,
            "format_type": format_type,
            "original_code": code,
            "documentation": documentation,
            "sections_generated": self._count_documentation_sections(documentation)
        }
    
    def _create_code_generation_prompt(
        self, requirements: str, language: str, context: Dict, examples: List[str]
    ) -> str:
        """Create a code generation prompt."""
        prompt = f"""
        Generate {language} code that meets the following requirements:
        
        Requirements:
        {requirements}
        
        Context:
        {context}
        
        Examples:
        {chr(10).join(examples) if examples else "No examples provided"}
        
        Please ensure the code is:
        1. Well-documented with comments and docstrings
        2. Follows best practices and coding standards
        3. Includes error handling where appropriate
        4. Efficient and readable
        5. Testable and maintainable
        """
        
        return prompt
    
    def _estimate_complexity(self, code: str) -> str:
        """Estimate code complexity."""
        lines = len(code.split('\n'))
        
        if lines < 20:
            return "Low"
        elif lines < 50:
            return "Medium"
        elif lines < 100:
            return "High"
        else:
            return "Very High"
    
    async def _analyze_execution_results(self, result: Dict) -> Dict[str, Any]:
        """Analyze code execution results."""
        analysis = {
            "status": result.get("status", "unknown"),
            "execution_time": result.get("execution_time", 0),
            "memory_usage": result.get("memory_usage", 0),
            "output_size": len(str(result.get("output", ""))),
            "has_errors": "error" in result.get("output", "").lower()
        }
        
        # Generate insights
        if analysis["execution_time"] > 5:
            analysis["performance_note"] = "Execution took longer than expected"
        if analysis["memory_usage"] > 1000000:  # 1MB
            analysis["memory_note"] = "High memory usage detected"
        if analysis["has_errors"]:
            analysis["error_note"] = "Execution produced errors"
        
        return analysis
    
    async def _extract_fixed_code(self, debug_response: str, original_code: str) -> str:
        """Extract fixed code from debug response."""
        # In a real implementation, this would use more sophisticated parsing
        lines = debug_response.split('\n')
        code_lines = []
        in_code_block = False
        
        for line in lines:
            if line.strip().startswith('```'):
                in_code_block = not in_code_block
                continue
            if in_code_block:
                code_lines.append(line)
        
        return '\n'.join(code_lines) if code_lines else original_code
    
    async def _extract_optimized_code(self, optimization_response: str, original_code: str) -> str:
        """Extract optimized code from optimization response."""
        # Similar to _extract_fixed_code
        lines = optimization_response.split('\n')
        code_lines = []
        in_code_block = False
        
        for line in lines:
            if line.strip().startswith('```'):
                in_code_block = not in_code_block
                continue
            if in_code_block:
                code_lines.append(line)
        
        return '\n'.join(code_lines) if code_lines else original_code
    
    async def _benchmark_code(self, original: str, optimized: str, language: str) -> Dict[str, Any]:
        """Benchmark original vs optimized code."""
        try:
            # Execute both versions
            original_result = await self.code_executor.execute_code(original, language)
            optimized_result = await self.code_executor.execute_code(optimized, language)
            
            original_time = original_result.get("execution_time", 0)
            optimized_time = optimized_result.get("execution_time", 0)
            
            improvement = ((original_time - optimized_time) / original_time * 100) if original_time > 0 else 0
            
            return {
                "original_time": original_time,
                "optimized_time": optimized_time,
                "improvement_percent": improvement,
                "faster": optimized_time < original_time
            }
        except Exception:
            return {
                "original_time": 0,
                "optimized_time": 0,
                "improvement_percent": 0,
                "faster": False,
                "error": "Benchmarking failed"
            }
    
    async def _extract_test_code(self, test_response: str) -> str:
        """Extract test code from test generation response."""
        lines = test_response.split('\n')
        code_lines = []
        in_code_block = False
        
        for line in lines:
            if line.strip().startswith('```'):
                in_code_block = not in_code_block
                continue
            if in_code_block:
                code_lines.append(line)
        
        return '\n'.join(code_lines) if code_lines else ""
    
    def _count_documentation_sections(self, documentation: str) -> int:
        """Count the number of documentation sections."""
        # Count headings
        headings = 0
        for line in documentation.split('\n'):
            if line.strip().startswith('#'):
                headings += 1
        return headings
