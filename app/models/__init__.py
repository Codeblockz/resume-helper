"""
Models package for Resume Helper.

This package contains Pydantic models for structured data validation
and type-safe LLM responses.
"""

from .responses import (
    JobRequirements,
    ResumeSection,
    MatchItem,
    GapItem,
    ComparisonResults,
    Recommendation,
    RecommendationResults,
    ResumeData
)

__all__ = [
    "JobRequirements",
    "ResumeSection", 
    "MatchItem",
    "GapItem",
    "ComparisonResults",
    "Recommendation",
    "RecommendationResults",
    "ResumeData"
]
