"""
Reviewer agent for quality assurance and content review.
"""

from typing import Any, Dict, List

from .base_agent import BaseAgent
from ..tools.utility_tools.text_processors import TextProcessors


class ReviewerAgent(BaseAgent):
    """Agent specialized in quality assurance and content review."""
    
    def __init__(self, **kwargs):
        super().__init__(
            name="Reviewer Agent",
            role="Quality Assurance Specialist",
            goal="Ensure high quality, accuracy, and consistency in generated documents and content",
            backstory=(
                "You are an expert reviewer with keen attention to detail and extensive experience in "
                "quality assurance. You excel at identifying errors, inconsistencies, and areas for improvement "
                "in written content. You are thorough, methodical, and committed to maintaining high standards "
                "of quality in all deliverables."
            ),
            **kwargs
        )
        
        self.text_processor = TextProcessors()
        self.add_tool(self.text_processor)
    
    async def execute_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        task_type = task.get("type", "content_review")
        
        if task_type == "content_review":
            return await self._review_content(task)
        elif task_type == "fact_check":
            return await self._fact_check(task)
        elif task_type == "consistency_check":
            return await self._check_consistency(task)
        elif task_type == "comprehensive_review":
            return await self._comprehensive_review(task)
        else:
            raise ValueError(f"Unknown task type: {task_type}")
    
    async def _review_content(self, task: Dict[str, Any]) -> Dict[str, Any]:
        content = task.get("content", "")
        review_criteria = task.get("criteria", ["grammar", "style", "clarity"])
        
        if not content:
            raise ValueError("Content is required for review")
        
        issues = []
        for criterion in review_criteria:
            criterion_issues = await self._check_criterion(content, criterion)
            issues.extend(criterion_issues)
        
        return {
            "type": "content_review",
            "criteria": review_criteria,
            "issues": issues,
            "total_issues": len(issues),
            "quality_score": self._calculate_quality_score(content, issues)
        }
    
    async def _fact_check(self, task: Dict[str, Any]) -> Dict[str, Any]:
        claims = task.get("claims", [])
        sources = task.get("sources", [])
        
        fact_check_results = []
        for claim in claims:
            verification = await self._verify_claim(claim, sources)
            fact_check_results.append(verification)
        
        return {
            "type": "fact_check",
            "claims_checked": len(claims),
            "results": fact_check_results,
            "accuracy_score": self._calculate_accuracy_score(fact_check_results)
        }
    
    async def _check_consistency(self, task: Dict[str, Any]) -> Dict[str, Any]:
        content = task.get("content", "")
        consistency_type = task.get("consistency_type", "all")
        
        inconsistencies = []
        if consistency_type in ["all", "terminology"]:
            inconsistencies.extend(await self._check_terminology_consistency(content))
        if consistency_type in ["all", "formatting"]:
            inconsistencies.extend(await self._check_formatting_consistency(content))
        
        return {
            "type": "consistency_check",
            "consistency_type": consistency_type,
            "inconsistencies": inconsistencies,
            "total_inconsistencies": len(inconsistencies)
        }
    
    async def _comprehensive_review(self, task: Dict[str, Any]) -> Dict[str, Any]:
        content = task.get("content", "")
        
        # Run all review types
        content_review = await self._review_content({"content": content})
        consistency_check = await self._check_consistency({"content": content})
        
        # Generate overall assessment
        assessment = await self._generate_overall_assessment(content_review, consistency_check)
        
        return {
            "type": "comprehensive_review",
            "content_review": content_review,
            "consistency_check": consistency_check,
            "overall_assessment": assessment,
            "recommendations": self._generate_recommendations(content_review, consistency_check)
        }
    
    async def _check_criterion(self, content: str, criterion: str) -> List[Dict]:
        # Simplified implementation
        return [{"type": criterion, "issue": f"Sample {criterion} issue", "severity": "medium"}]
    
    async def _verify_claim(self, claim: str, sources: List) -> Dict:
        return {"claim": claim, "verified": True, "confidence": 0.8}
    
    async def _check_terminology_consistency(self, content: str) -> List[Dict]:
        return [{"type": "terminology", "issue": "Sample terminology inconsistency"}]
    
    async def _check_formatting_consistency(self, content: str) -> List[Dict]:
        return [{"type": "formatting", "issue": "Sample formatting inconsistency"}]
    
    def _calculate_quality_score(self, content: str, issues: List) -> float:
        base_score = 100.0
        penalty = len(issues) * 2.0
        return max(0, base_score - penalty)
    
    def _calculate_accuracy_score(self, results: List[Dict]) -> float:
        if not results:
            return 0.0
        verified_count = sum(1 for r in results if r.get("verified", False))
        return (verified_count / len(results)) * 100
    
    async def _generate_overall_assessment(self, content_review: Dict, consistency_check: Dict) -> str:
        return "Overall content quality is good with minor issues identified."
    
    def _generate_recommendations(self, content_review: Dict, consistency_check: Dict) -> List[str]:
        recommendations = []
        if content_review.get("total_issues", 0) > 0:
            recommendations.append("Address identified content issues")
        if consistency_check.get("total_inconsistencies", 0) > 0:
            recommendations.append("Fix consistency problems")
        recommendations.extend(["Proofread final document", "Validate all sources"])
        return recommendations
