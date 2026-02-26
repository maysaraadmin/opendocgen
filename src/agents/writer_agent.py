"""
Writer agent for document composition and content generation.
"""

from typing import Any, Dict, List

from .base_agent import BaseAgent
from ..tools.document_tools.template_manager import TemplateManager
from ..tools.utility_tools.text_processors import TextProcessors


class WriterAgent(BaseAgent):
    """Agent specialized in document composition and content generation."""
    
    def __init__(self, **kwargs):
        """Initialize writer agent."""
        super().__init__(
            name="Writer Agent",
            role="Document Composition Specialist",
            goal="Create well-structured, coherent, and professional documents based on research findings and analysis results",
            backstory=(
                "You are an expert writer with extensive experience in technical writing, business communication, "
                "and content creation. You excel at organizing complex information into clear, engaging, and "
                "well-structured documents. You have a deep understanding of different writing styles, document "
                "formats, and audience requirements. You are meticulous about grammar, style, and clarity."
            ),
            **kwargs
        )
        
        # Initialize writing tools
        self.template_manager = TemplateManager()
        self.text_processor = TextProcessors()
        
        # Add tools to agent
        self.add_tool(self.template_manager)
        self.add_tool(self.text_processor)
    
    async def execute_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a writing task."""
        task_type = task.get("type", "generate")
        
        if task_type == "generate":
            return await self._generate_content(task)
        elif task_type == "format":
            return await self._format_document(task)
        elif task_type == "edit":
            return await self._edit_content(task)
        elif task_type == "summarize":
            return await self._summarize_content(task)
        elif task_type == "comprehensive_document":
            return await self._create_comprehensive_document(task)
        else:
            raise ValueError(f"Unknown task type: {task_type}")
    
    async def _generate_content(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Generate content based on requirements."""
        content_type = task.get("content_type", "general")
        topic = task.get("topic")
        requirements = task.get("requirements", [])
        research_data = task.get("research_data", {})
        analysis_data = task.get("analysis_data", {})
        
        if not topic:
            raise ValueError("Topic is required for content generation")
        
        # Create generation prompt
        prompt = self._create_generation_prompt(
            content_type, topic, requirements, research_data, analysis_data
        )
        
        # Generate content
        content = await self.think(prompt)
        
        # Process and enhance content
        processed_content = await self.text_processor.enhance_content(content)
        
        return {
            "type": "generated_content",
            "content_type": content_type,
            "topic": topic,
            "content": processed_content,
            "word_count": len(processed_content.split()),
            "requirements_met": self._check_requirements(requirements, processed_content)
        }
    
    async def _format_document(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Format document according to specified style."""
        content = task.get("content")
        format_type = task.get("format_type", "business_report")
        style_guide = task.get("style_guide", {})
        
        if not content:
            raise ValueError("Content is required for formatting")
        
        # Apply formatting
        formatted_content = await self.text_processor.format_content(
            content, format_type, style_guide
        )
        
        # Generate table of contents if needed
        toc = None
        if task.get("include_toc", False):
            toc = await self._generate_toc(formatted_content)
        
        return {
            "type": "formatted_document",
            "format_type": format_type,
            "formatted_content": formatted_content,
            "table_of_contents": toc,
            "formatting_applied": self._get_formatting_rules(format_type)
        }
    
    async def _edit_content(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Edit and improve content."""
        content = task.get("content")
        edit_type = task.get("edit_type", "comprehensive")
        focus_areas = task.get("focus_areas", [])
        
        if not content:
            raise ValueError("Content is required for editing")
        
        # Apply edits based on type
        if edit_type == "grammar":
            edited_content = await self.text_processor.fix_grammar(content)
        elif edit_type == "style":
            edited_content = await self.text_processor.improve_style(content)
        elif edit_type == "clarity":
            edited_content = await self.text_processor.improve_clarity(content)
        elif edit_type == "comprehensive":
            edited_content = await self.text_processor.comprehensive_edit(content, focus_areas)
        else:
            edited_content = content
        
        # Generate edit summary
        edit_summary = await self._generate_edit_summary(content, edited_content)
        
        return {
            "type": "edited_content",
            "edit_type": edit_type,
            "original_content": content,
            "edited_content": edited_content,
            "edit_summary": edit_summary,
            "improvements_made": self._count_improvements(content, edited_content)
        }
    
    async def _summarize_content(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Summarize content."""
        content = task.get("content")
        summary_type = task.get("summary_type", "executive")
        max_length = task.get("max_length", 300)
        
        if not content:
            raise ValueError("Content is required for summarization")
        
        # Create summary prompt
        prompt = f"""
        Create a {summary_type} summary of the following content. 
        Maximum length: {max_length} words.
        
        Content:
        {content}
        
        Please provide:
        1. Key points and findings
        2. Main conclusions
        3. Important recommendations
        4. Next steps or implications
        """
        
        summary = await self.think(prompt)
        
        # Extract key points
        key_points = await self.text_processor.extract_key_points(content)
        
        return {
            "type": "summary",
            "summary_type": summary_type,
            "summary": summary,
            "key_points": key_points,
            "original_length": len(content.split()),
            "summary_length": len(summary.split()),
            "compression_ratio": len(summary.split()) / len(content.split())
        }
    
    async def _create_comprehensive_document(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Create a comprehensive document from research and analysis."""
        topic = task.get("topic")
        document_type = task.get("document_type", "research_report")
        research_data = task.get("research_data", {})
        analysis_data = task.get("analysis_data", {})
        template = task.get("template", "research_paper")
        
        if not topic:
            raise ValueError("Topic is required for comprehensive document")
        
        # Load template
        template_content = await self.template_manager.get_template(template)
        
        # Generate each section
        sections = {}
        section_order = self._get_section_order(document_type)
        
        for section in section_order:
            section_content = await self._generate_section(
                section, topic, research_data, analysis_data, template_content
            )
            sections[section] = section_content
        
        # Assemble document
        document = await self._assemble_document(sections, template_content)
        
        # Format document
        formatted_document = await self._format_document({
            "content": document,
            "format_type": document_type,
            "include_toc": True
        })
        
        return {
            "type": "comprehensive_document",
            "document_type": document_type,
            "topic": topic,
            "sections": sections,
            "document": formatted_document["formatted_content"],
            "table_of_contents": formatted_document["table_of_contents"],
            "metadata": {
                "word_count": len(document.split()),
                "section_count": len(sections),
                "template_used": template
            }
        }
    
    def _create_generation_prompt(
        self, content_type: str, topic: str, requirements: List[str],
        research_data: Dict, analysis_data: Dict
    ) -> str:
        """Create a content generation prompt."""
        prompt = f"""
        Generate {content_type} content about: {topic}
        
        Requirements:
        {chr(10).join(f"- {req}" for req in requirements)}
        
        Research Data:
        {research_data}
        
        Analysis Data:
        {analysis_data}
        
        Please ensure the content is:
        1. Well-structured and coherent
        2. Factually accurate based on the provided data
        3. Appropriate for the target audience
        4. Engaging and informative
        5. Properly cited where applicable
        """
        
        return prompt
    
    async def _generate_toc(self, content: str) -> Dict[str, Any]:
        """Generate table of contents."""
        # Extract headings
        headings = await self.text_processor.extract_headings(content)
        
        # Create TOC structure
        toc = []
        for heading in headings:
            toc.append({
                "title": heading["text"],
                "level": heading["level"],
                "page": heading.get("page", 1)
            })
        
        return {
            "title": "Table of Contents",
            "entries": toc,
            "total_entries": len(toc)
        }
    
    def _check_requirements(self, requirements: List[str], content: str) -> List[str]:
        """Check if requirements are met in the content."""
        met_requirements = []
        
        for req in requirements:
            # Simple keyword matching for requirement checking
            req_keywords = req.lower().split()
            content_lower = content.lower()
            
            if any(keyword in content_lower for keyword in req_keywords):
                met_requirements.append(req)
        
        return met_requirements
    
    def _get_formatting_rules(self, format_type: str) -> List[str]:
        """Get formatting rules for a given format type."""
        rules = {
            "business_report": [
                "Professional headings",
                "Consistent font sizing",
                "Proper spacing",
                "Page numbers",
                "Header/footer"
            ],
            "academic_paper": [
                "Citation format",
                "Abstract section",
                "References section",
                "Formal tone",
                "Structured sections"
            ],
            "technical_doc": [
                "Code formatting",
                "Technical diagrams",
                "API documentation",
                "Examples",
                "Troubleshooting section"
            ]
        }
        
        return rules.get(format_type, ["Basic formatting applied"])
    
    async def _generate_edit_summary(self, original: str, edited: str) -> Dict[str, Any]:
        """Generate a summary of edits made."""
        # Simple comparison - in a real implementation, this would be more sophisticated
        original_words = original.split()
        edited_words = edited.split()
        
        changes = {
            "words_added": len(edited_words) - len(original_words),
            "words_removed": max(0, len(original_words) - len(edited_words)),
            "total_changes": abs(len(edited_words) - len(original_words))
        }
        
        # Generate summary prompt
        summary_prompt = f"""
        Summarize the key improvements made in this edit:
        
        Original: {original[:500]}...
        Edited: {edited[:500]}...
        
        Focus on:
        1. Clarity improvements
        2. Grammar corrections
        3. Style enhancements
        4. Structural changes
        """
        
        summary = await self.think(summary_prompt)
        
        return {
            "changes": changes,
            "summary": summary
        }
    
    def _count_improvements(self, original: str, edited: str) -> int:
        """Count the number of improvements made."""
        # Simple heuristic based on length difference
        return abs(len(edited) - len(original))
    
    def _get_section_order(self, document_type: str) -> List[str]:
        """Get the order of sections for a document type."""
        section_orders = {
            "research_report": [
                "executive_summary",
                "introduction",
                "methodology",
                "findings",
                "analysis",
                "conclusions",
                "recommendations",
                "appendices"
            ],
            "business_report": [
                "executive_summary",
                "introduction",
                "market_analysis",
                "findings",
                "recommendations",
                "implementation_plan",
                "conclusions"
            ],
            "technical_doc": [
                "overview",
                "installation",
                "configuration",
                "usage",
                "api_reference",
                "troubleshooting",
                "faq"
            ]
        }
        
        return section_orders.get(document_type, ["introduction", "main_content", "conclusions"])
    
    async def _generate_section(
        self, section: str, topic: str, research_data: Dict, analysis_data: Dict, template: Dict
    ) -> str:
        """Generate content for a specific section."""
        section_prompt = f"""
        Write the {section.replace('_', ' ').title()} section for a document about: {topic}
        
        Research Data:
        {research_data}
        
        Analysis Data:
        {analysis_data}
        
        Template guidance:
        {template.get(section, {})}
        
        Make sure this section is:
        1. Comprehensive and detailed
        2. Well-structured with clear subheadings
        3. Supported by the provided data
        4. Appropriate for the document type
        """
        
        return await self.think(section_prompt)
    
    async def _assemble_document(self, sections: Dict[str, str], template: Dict) -> str:
        """Assemble sections into a complete document."""
        document_parts = []
        
        # Add title page
        title_page = template.get("title_page", "# Document Title\n\nGenerated by OpenDocGen")
        document_parts.append(title_page)
        
        # Add sections in order
        for section_name, section_content in sections.items():
            section_title = section_name.replace('_', ' ').title()
            document_parts.append(f"\n\n# {section_title}\n\n{section_content}")
        
        # Add references if available
        if "references" in template:
            document_parts.append(f"\n\n# References\n\n{template['references']}")
        
        return "\n".join(document_parts)
