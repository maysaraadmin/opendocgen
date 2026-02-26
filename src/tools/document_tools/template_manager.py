"""
Template manager for document templates.
"""

import json
import logging
from pathlib import Path
from typing import Any, Dict, List, Optional

import yaml

from ...config import get_settings

logger = logging.getLogger(__name__)


class TemplateManager:
    """Tool for managing document templates."""
    
    def __init__(self, templates_dir: Optional[Path] = None):
        """Initialize template manager."""
        self.templates_dir = templates_dir or Path("./src/templates")
        self.templates = {}
        self._load_templates()
    
    def _load_templates(self):
        """Load all available templates."""
        template_files = {
            "business_report": "business_report.md",
            "research_paper": "research_paper.md", 
            "technical_doc": "technical_doc.md",
            "proposal": "proposal.md"
        }
        
        for template_name, filename in template_files.items():
            template_path = self.templates_dir / filename
            if template_path.exists():
                try:
                    with open(template_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    self.templates[template_name] = content
                    logger.info(f"Loaded template: {template_name}")
                except Exception as e:
                    logger.error(f"Error loading template {template_name}: {e}")
            else:
                # Create default template
                self.templates[template_name] = self._create_default_template(template_name)
                logger.info(f"Created default template: {template_name}")
    
    async def get_template(self, template_name: str) -> Dict[str, Any]:
        """Get a template by name."""
        if template_name not in self.templates:
            raise ValueError(f"Template '{template_name}' not found")
        
        template_content = self.templates[template_name]
        
        return {
            "name": template_name,
            "content": template_content,
            "sections": self._extract_sections(template_content),
            "variables": self._extract_variables(template_content)
        }
    
    async def render_template(
        self,
        template_name: str,
        variables: Dict[str, Any]
    ) -> str:
        """Render a template with variables."""
        template_data = await self.get_template(template_name)
        content = template_data["content"]
        
        # Simple template rendering
        for key, value in variables.items():
            placeholder = f"{{{{{key}}}}}"
            content = content.replace(placeholder, str(value))
        
        return content
    
    def _extract_sections(self, content: str) -> List[str]:
        """Extract section names from template."""
        sections = []
        lines = content.split('\n')
        
        for line in lines:
            if line.strip().startswith('#'):
                section_name = line.strip('#').strip().lower().replace(' ', '_')
                sections.append(section_name)
        
        return sections
    
    def _extract_variables(self, content: str) -> List[str]:
        """Extract variable placeholders from template."""
        import re
        
        # Find all {{variable}} patterns
        pattern = r'\{\{([^}]+)\}\}'
        matches = re.findall(pattern, content)
        
        return list(set(matches))
    
    def _create_default_template(self, template_name: str) -> str:
        """Create a default template."""
        templates = {
            "business_report": """# {{title}}

## Executive Summary
{{executive_summary}}

## Introduction
{{introduction}}

## Analysis
{{analysis}}

## Findings
{{findings}}

## Recommendations
{{recommendations}}

## Conclusion
{{conclusion}}
""",
            "research_paper": """# {{title}}

## Abstract
{{abstract}}

## Introduction
{{introduction}}

## Literature Review
{{literature_review}}

## Methodology
{{methodology}}

## Results
{{results}}

## Discussion
{{discussion}}

## Conclusion
{{conclusion}}

## References
{{references}}
""",
            "technical_doc": """# {{title}}

## Overview
{{overview}}

## Installation
{{installation}}

## Configuration
{{configuration}}

## Usage
{{usage}}

## API Reference
{{api_reference}}

## Troubleshooting
{{troubleshooting}}
""",
            "proposal": """# {{title}}

## Executive Summary
{{executive_summary}}

## Problem Statement
{{problem_statement}}

## Proposed Solution
{{proposed_solution}}

## Implementation Plan
{{implementation_plan}}

## Timeline
{{timeline}}

## Budget
{{budget}}

## Conclusion
{{conclusion}}
"""
        }
        
        return templates.get(template_name, "# {{title}}\n\n{{content}}")
