"""
Text processing utilities for content enhancement and formatting.
"""

import re
import logging
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)


class TextProcessors:
    """Tool for text processing and enhancement."""
    
    async def enhance_content(self, content: str) -> str:
        """Enhance content with better formatting and structure."""
        # Clean up extra whitespace
        content = re.sub(r'\n\s*\n\s*\n', '\n\n', content)
        
        # Ensure proper heading spacing
        content = re.sub(r'\n(#{1,6})', r'\n\1', content)
        
        # Fix common formatting issues
        content = self._fix_common_issues(content)
        
        return content.strip()
    
    async def format_content(
        self,
        content: str,
        format_type: str,
        style_guide: Dict[str, Any]
    ) -> str:
        """Format content according to specified style."""
        if format_type == "business_report":
            return self._format_business_report(content, style_guide)
        elif format_type == "academic_paper":
            return self._format_academic_paper(content, style_guide)
        elif format_type == "technical_doc":
            return self._format_technical_doc(content, style_guide)
        else:
            return content
    
    async def fix_grammar(self, content: str) -> str:
        """Fix basic grammar issues."""
        # Fix common grammar mistakes
        fixes = {
            r'\bi\b': 'I',  # Capitalize standalone 'i'
            r'\. +': '. ',  # Fix spacing after periods
            r', +': ', ',   # Fix spacing after commas
            r' +,' : ',',   # Fix spacing before commas
        }
        
        for pattern, replacement in fixes.items():
            content = re.sub(pattern, replacement, content)
        
        return content
    
    async def improve_style(self, content: str) -> str:
        """Improve writing style."""
        # Remove redundant words
        redundant_words = ['very', 'really', 'quite', 'rather', 'somewhat']
        for word in redundant_words:
            content = re.sub(rf'\b{word}\s+', '', content, flags=re.IGNORECASE)
        
        # Improve sentence structure
        content = self._improve_sentence_structure(content)
        
        return content
    
    async def improve_clarity(self, content: str) -> str:
        """Improve content clarity."""
        # Simplify complex sentences
        content = self._simplify_sentences(content)
        
        # Add transition words where needed
        content = self._add_transitions(content)
        
        return content
    
    async def comprehensive_edit(
        self,
        content: str,
        focus_areas: List[str]
    ) -> str:
        """Perform comprehensive editing."""
        edited_content = content
        
        for area in focus_areas:
            if area == "grammar":
                edited_content = await self.fix_grammar(edited_content)
            elif area == "style":
                edited_content = await self.improve_style(edited_content)
            elif area == "clarity":
                edited_content = await self.improve_clarity(edited_content)
            elif area == "formatting":
                edited_content = await self.enhance_content(edited_content)
        
        return edited_content
    
    async def extract_key_points(self, content: str) -> List[str]:
        """Extract key points from content."""
        sentences = re.split(r'[.!?]+', content)
        key_points = []
        
        # Simple heuristic: longer sentences with important keywords
        important_keywords = ['important', 'significant', 'key', 'critical', 'essential', 'major']
        
        for sentence in sentences:
            sentence = sentence.strip()
            if len(sentence) > 50 and any(keyword in sentence.lower() for keyword in important_keywords):
                key_points.append(sentence)
        
        return key_points[:10]  # Return top 10 key points
    
    async def extract_headings(self, content: str) -> List[Dict[str, Any]]:
        """Extract headings from content."""
        headings = []
        lines = content.split('\n')
        
        for i, line in enumerate(lines):
            if line.strip().startswith('#'):
                level = len(line) - len(line.lstrip('#'))
                text = line.strip('#').strip()
                headings.append({
                    "text": text,
                    "level": level,
                    "line": i + 1
                })
        
        return headings
    
    def _fix_common_issues(self, content: str) -> str:
        """Fix common formatting issues."""
        # Fix multiple spaces
        content = re.sub(r' +', ' ', content)
        
        # Fix line breaks
        content = re.sub(r'\r\n', '\n', content)
        
        # Fix quotes
        content = re.sub(r'"([^"]*)"', r'"\1"', content)
        
        return content
    
    def _format_business_report(self, content: str, style_guide: Dict[str, Any]) -> str:
        """Format content as business report."""
        # Add professional formatting
        if not content.startswith('#'):
            content = f"# Business Report\n\n{content}"
        
        # Add sections if missing
        if '## Executive Summary' not in content:
            content = content.replace('\n# ', '\n## Executive Summary\n\n# ')
        
        return content
    
    def _format_academic_paper(self, content: str, style_guide: Dict[str, Any]) -> str:
        """Format content as academic paper."""
        # Add academic structure
        if '## Abstract' not in content and 'Abstract' not in content:
            content = f"## Abstract\n\n{content}"
        
        return content
    
    def _format_technical_doc(self, content: str, style_guide: Dict[str, Any]) -> str:
        """Format content as technical documentation."""
        # Add code blocks for technical content
        content = re.sub(r'`([^`]+)`', r'`\1`', content)
        
        return content
    
    def _improve_sentence_structure(self, content: str) -> str:
        """Improve sentence structure."""
        # Break up very long sentences
        sentences = re.split(r'(?<=[.!?])\s+', content)
        improved_sentences = []
        
        for sentence in sentences:
            if len(sentence) > 200:  # Very long sentence
                # Try to split at conjunctions
                parts = re.split(r'\b(and|but|or|however|therefore)\b', sentence, flags=re.IGNORECASE)
                if len(parts) > 1:
                    # Reconstruct with proper breaks
                    new_sentence = parts[0]
                    for i in range(1, len(parts), 2):
                        if i + 1 < len(parts):
                            new_sentence += parts[i] + parts[i+1] + '. '
                    improved_sentences.append(new_sentence.strip())
                else:
                    improved_sentences.append(sentence)
            else:
                improved_sentences.append(sentence)
        
        return ' '.join(improved_sentences)
    
    def _simplify_sentences(self, content: str) -> str:
        """Simplify complex sentences."""
        # Replace complex words with simpler alternatives
        replacements = {
            'utilize': 'use',
            'facilitate': 'help',
            'implement': 'carry out',
            'subsequently': 'then',
            'consequently': 'therefore',
            'nevertheless': 'however'
        }
        
        for complex_word, simple_word in replacements.items():
            content = re.sub(rf'\b{complex_word}\b', simple_word, content, flags=re.IGNORECASE)
        
        return content
    
    def _add_transitions(self, content: str) -> str:
        """Add transition words to improve flow."""
        # Simple heuristic: add transitions between paragraphs
        paragraphs = content.split('\n\n')
        transitions = ['Furthermore,', 'Additionally,', 'Moreover,', 'In addition,']
        
        improved_paragraphs = []
        for i, paragraph in enumerate(paragraphs):
            improved_paragraphs.append(paragraph)
            if i < len(paragraphs) - 1 and i % 2 == 0:
                transition = transitions[i % len(transitions)]
                improved_paragraphs.append(f"{transition} ")
        
        return '\n\n'.join(improved_paragraphs)
