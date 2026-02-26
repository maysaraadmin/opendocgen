"""
Statistical analysis tools for OpenDocGen.
"""

import asyncio
from typing import Any, Dict, List, Optional, Union
import statistics

try:
    import numpy as np
    import pandas as pd
    import scipy.stats as stats
    STATISTICS_AVAILABLE = True
except ImportError:
    STATISTICS_AVAILABLE = False
    np = None
    pd = None
    stats = None


class StatisticalTools:
    """Handles statistical analysis for data insights."""
    
    def __init__(self):
        """Initialize statistical tools."""
        self.available = STATISTICS_AVAILABLE
        self.supported_tests = [
            "mean", "median", "mode", "std", "variance",
            "correlation", "t_test", "chi_square", "anova",
            "regression", "distribution_fit", "outlier_detection"
        ]
    
    async def basic_statistics(self, data: List[Union[int, float]]) -> Dict[str, Any]:
        """Calculate basic statistical measures."""
        try:
            if not data:
                return {"error": "No data provided"}
            
            result = {
                "count": len(data),
                "mean": statistics.mean(data),
                "median": statistics.median(data),
                "mode": statistics.mode(data) if len(set(data)) < len(data) else None,
                "min": min(data),
                "max": max(data),
                "range": max(data) - min(data),
                "sum": sum(data),
            }
            
            # Calculate variance and standard deviation
            if len(data) > 1:
                result["variance"] = statistics.variance(data)
                result["std_dev"] = statistics.stdev(data)
            
            return {"success": True, "statistics": result}
            
        except Exception as e:
            return {"error": f"Statistical calculation failed: {str(e)}"}
    
    async def correlation_analysis(self, x_data: List[Union[int, float]], y_data: List[Union[int, float]]) -> Dict[str, Any]:
        """Perform correlation analysis."""
        try:
            if len(x_data) != len(y_data):
                return {"error": "x and y data must have same length"}
            
            if not self.available:
                # Basic correlation calculation without scipy
                n = len(x_data)
                sum_x = sum(x_data)
                sum_y = sum(y_data)
                sum_xy = sum(x * y for x, y in zip(x_data, y_data))
                sum_x2 = sum(x ** 2 for x in x_data)
                sum_y2 = sum(y ** 2 for y in y_data)
                
                # Calculate correlation with proper formula
                denominator = ((n * sum_x2 - sum_x ** 2) * (n * sum_y2 - sum_y ** 2)) ** 0.5
                
                if denominator == 0:
                    return {"error": "Cannot calculate correlation: zero denominator"}
                
                correlation = (n * sum_xy - sum_x * sum_y) / denominator
                
                return {
                    "success": True,
                    "correlation_coefficient": correlation,
                    "method": "pearson",
                }
            else:
                # Use scipy for more advanced analysis
                correlation, p_value = stats.pearsonr(x_data, y_data)
                
                return {
                    "success": True,
                    "correlation_coefficient": correlation,
                    "p_value": p_value,
                    "method": "pearson_scipy",
                }
                
        except Exception as e:
            return {"error": f"Correlation analysis failed: {str(e)}"}
    
    async def distribution_analysis(self, data: List[Union[int, float]]) -> Dict[str, Any]:
        """Analyze data distribution."""
        try:
            if not data:
                return {"error": "No data provided"}
            
            result = {
                "histogram": self._create_histogram(data),
                "percentiles": self._calculate_percentiles(data),
                "normality_test": self._test_normality(data) if self.available else "Not available",
            }
            
            return {"success": True, "distribution": result}
            
        except Exception as e:
            return {"error": f"Distribution analysis failed: {str(e)}"}
    
    async def outlier_detection(self, data: List[Union[int, float]], method: str = "iqr") -> Dict[str, Any]:
        """Detect outliers in data."""
        try:
            if not data:
                return {"error": "No data provided"}
            
            if method == "iqr":
                q1 = statistics.quantiles(data, 0.25)
                q3 = statistics.quantiles(data, 0.75)
                iqr = q3 - q1
                lower_bound = q1 - 1.5 * iqr
                upper_bound = q3 + 1.5 * iqr
                
                outliers = [x for x in data if x < lower_bound or x > upper_bound]
                
                return {
                    "success": True,
                    "method": "interquartile_range",
                    "outliers": outliers,
                    "outlier_count": len(outliers),
                    "bounds": {"lower": lower_bound, "upper": upper_bound},
                }
            
            elif method == "zscore":
                mean = statistics.mean(data)
                std = statistics.stdev(data)
                threshold = 2  # Standard threshold for z-score method
                
                outliers = [x for x in data if abs((x - mean) / std) > threshold]
                
                return {
                    "success": True,
                    "method": "z_score",
                    "outliers": outliers,
                    "outlier_count": len(outliers),
                    "threshold": threshold,
                }
            
            else:
                return {"error": f"Unsupported outlier detection method: {method}"}
                
        except Exception as e:
            return {"error": f"Outlier detection failed: {str(e)}"}
    
    def _create_histogram(self, data: List[Union[int, float]]) -> Dict[str, Any]:
        """Create histogram data."""
        try:
            if self.available and pd:
                df = pd.DataFrame(data, columns=['values'])
                hist = df['values'].value_counts().sort_index()
                return {
                    "bins": len(hist),
                    "frequency": hist.to_dict(),
                    "distribution": "histogram",
                }
            else:
                # Manual histogram calculation
                sorted_data = sorted(data)
                hist = {}
                for value in sorted_data:
                    hist[value] = hist.get(value, 0) + 1
                
                return {
                    "bins": len(hist),
                    "frequency": hist,
                    "distribution": "histogram",
                }
        except Exception:
            return {"error": "Failed to create histogram"}
    
    def _calculate_percentiles(self, data: List[Union[int, float]]) -> Dict[str, float]:
        """Calculate percentiles."""
        sorted_data = sorted(data)
        n = len(sorted_data)
        
        return {
            "p25": sorted_data[int(n * 0.25)] if n > 0 else None,
            "p50": sorted_data[int(n * 0.5)] if n > 0 else None,
            "p75": sorted_data[int(n * 0.75)] if n > 0 else None,
            "p90": sorted_data[int(n * 0.9)] if n > 0 else None,
            "p95": sorted_data[int(n * 0.95)] if n > 0 else None,
            "p99": sorted_data[int(n * 0.99)] if n > 0 else None,
        }
    
    def _test_normality(self, data: List[Union[int, float]]) -> Dict[str, Any]:
        """Test for normality using Shapiro-Wilk test."""
        if not self.available or not stats:
            return {"test": "shapiro_wilk", "available": False}
        
        try:
            statistic, p_value = stats.shapiro(data)
            
            return {
                "test": "shapiro_wilk",
                "statistic": statistic,
                "p_value": p_value,
                "is_normal": p_value > 0.05,  # Common significance level
                "available": True,
            }
        except Exception:
            return {"test": "shapiro_wilk", "available": True, "error": "Test failed"}
    
    def get_supported_tests(self) -> List[str]:
        """Get list of supported statistical tests."""
        return self.supported_tests
    
    def is_available(self) -> bool:
        """Check if statistical libraries are available."""
        return self.available