"""
Pydantic response models for Resume Helper.

This module defines structured data models for all LLM responses,
providing type safety and validation for the application data flow.
"""

from pydantic import BaseModel, Field
from typing import List, Optional, Dict


class JobRequirements(BaseModel):
    """Structured job requirements extracted from job descriptions."""
    
    required_skills: List[str] = Field(
        description="Essential skills required for the job",
        default_factory=list
    )
    preferred_skills: List[str] = Field(
        description="Nice-to-have skills that would be beneficial",
        default_factory=list
    )
    required_experience: List[str] = Field(
        description="Required work experience and background",
        default_factory=list
    )
    required_education: List[str] = Field(
        description="Educational requirements and qualifications",
        default_factory=list
    )
    responsibilities: List[str] = Field(
        description="Key job responsibilities and duties",
        default_factory=list
    )
    keywords: List[str] = Field(
        description="Important keywords for ATS optimization",
        default_factory=list
    )
    
    class Config:
        """Pydantic configuration for JobRequirements."""
        json_schema_extra = {
            "example": {
                "required_skills": ["Python", "Django", "SQL", "Git"],
                "preferred_skills": ["React", "Docker", "AWS"],
                "required_experience": ["3+ years software development", "Web application development"],
                "required_education": ["Bachelor's degree in Computer Science"],
                "responsibilities": ["Develop web applications", "Database design", "Code reviews"],
                "keywords": ["Python", "Django", "SQL", "web development", "database"]
            }
        }


class ResumeSection(BaseModel):
    """Structured resume sections extracted from PDF resumes."""
    
    contact_information: Optional[str] = Field(
        None,
        description="Contact details including name, email, phone, address"
    )
    summary: Optional[str] = Field(
        None,
        description="Professional summary or objective statement"
    )
    education: Optional[str] = Field(
        None,
        description="Educational background and qualifications"
    )
    experience: Optional[str] = Field(
        None,
        description="Work experience and employment history"
    )
    skills: Optional[str] = Field(
        None,
        description="Technical and professional skills"
    )
    projects: Optional[str] = Field(
        None,
        description="Notable projects and accomplishments"
    )
    certifications: Optional[str] = Field(
        None,
        description="Professional certifications and licenses"
    )
    additional: Optional[str] = Field(
        None,
        description="Other relevant sections (awards, publications, etc.)"
    )
    
    def to_dict(self) -> Dict[str, str]:
        """Convert to dictionary format for backward compatibility."""
        result = {}
        for field_name, value in self.model_dump().items():
            if value is not None:
                # Convert snake_case to title case for display
                display_name = field_name.replace("_", " ").title()
                if display_name == "Contact Information":
                    display_name = "Contact Information"
                result[display_name] = value
        return result
    
    class Config:
        """Pydantic configuration for ResumeSection."""
        json_schema_extra = {
            "example": {
                "contact_information": "John Doe\njohn.doe@example.com\n(123) 456-7890",
                "summary": "Experienced software engineer with 5 years of Python development.",
                "skills": "Python, Django, Flask, SQL, JavaScript, React",
                "experience": "Software Engineer at ABC Corp (2018-Present)\n- Developed web applications using Django",
                "education": "Bachelor of Science in Computer Science, XYZ University (2014-2018)"
            }
        }


class ResumeData(BaseModel):
    """Complete resume data structure including raw text and parsed sections."""
    
    raw_text: str = Field(
        description="The complete raw text extracted from the PDF resume"
    )
    sections: ResumeSection = Field(
        description="Structured sections of the resume"
    )
    
    class Config:
        """Pydantic configuration for ResumeData."""
        json_schema_extra = {
            "example": {
                "raw_text": "John Doe\nSoftware Engineer\n...",
                "sections": {
                    "contact_information": "John Doe\njohn.doe@example.com",
                    "experience": "Software Engineer at ABC Corp...",
                    "skills": "Python, Django, SQL..."
                }
            }
        }


class MatchItem(BaseModel):
    """Individual match between resume content and job requirements."""
    
    category: str = Field(
        description="Category of the match (required_skills, experience, etc.)"
    )
    item: str = Field(
        description="The specific item that matches"
    )
    where_found: str = Field(
        description="Where in the resume this match was found"
    )
    
    class Config:
        """Pydantic configuration for MatchItem."""
        json_schema_extra = {
            "example": {
                "category": "required_skills",
                "item": "Python",
                "where_found": "Skills section"
            }
        }


class GapItem(BaseModel):
    """Individual gap or missing requirement from the resume."""
    
    category: str = Field(
        description="Category of the gap (required_skills, experience, etc.)"
    )
    item: str = Field(
        description="The specific item that is missing"
    )
    suggestion: str = Field(
        description="Specific suggestion for how to address this gap"
    )
    
    class Config:
        """Pydantic configuration for GapItem."""
        json_schema_extra = {
            "example": {
                "category": "required_skills",
                "item": "Docker",
                "suggestion": "Add Docker experience to Skills section"
            }
        }


class ComparisonResults(BaseModel):
    """Complete comparison results between resume and job requirements."""
    
    matches: List[MatchItem] = Field(
        description="Items that match between resume and job requirements",
        default_factory=list
    )
    gaps: List[GapItem] = Field(
        description="Missing items or gaps in the resume",
        default_factory=list
    )
    match_score: int = Field(
        ge=0,
        le=100,
        description="Overall match percentage (0-100)"
    )
    section_scores: Dict[str, int] = Field(
        description="Scores by category/section",
        default_factory=dict
    )
    
    class Config:
        """Pydantic configuration for ComparisonResults."""
        json_schema_extra = {
            "example": {
                "matches": [
                    {
                        "category": "required_skills",
                        "item": "Python",
                        "where_found": "Skills section"
                    }
                ],
                "gaps": [
                    {
                        "category": "required_skills", 
                        "item": "Docker",
                        "suggestion": "Add Docker experience to Skills section"
                    }
                ],
                "match_score": 75,
                "section_scores": {
                    "required_skills": 80,
                    "preferred_skills": 60,
                    "required_experience": 90,
                    "required_education": 100,
                    "keywords": 75
                }
            }
        }


class Recommendation(BaseModel):
    """Individual recommendation for improving resume match."""
    
    section: str = Field(
        description="Resume section to modify (Skills, Experience, etc.)"
    )
    type: str = Field(
        description="Type of change needed (add, modify, emphasize, remove)"
    )
    content: str = Field(
        description="Specific recommendation or change to make"
    )
    reason: str = Field(
        description="Explanation of why this change is needed"
    )
    priority: int = Field(
        ge=1,
        le=10,
        description="Priority level from 1 (low) to 10 (critical)"
    )
    
    class Config:
        """Pydantic configuration for Recommendation."""
        json_schema_extra = {
            "example": {
                "section": "Skills",
                "type": "add",
                "content": "Add Docker containerization experience",
                "reason": "Docker is a required skill that is missing from your resume",
                "priority": 9
            }
        }


class RecommendationResults(BaseModel):
    """Complete recommendation results with summary and specific suggestions."""
    
    summary: str = Field(
        description="Overall assessment and brief summary of recommendations"
    )
    recommendations: List[Recommendation] = Field(
        description="Specific, prioritized recommendations for improvement",
        default_factory=list
    )
    keyword_suggestions: List[str] = Field(
        description="Important keywords to incorporate into the resume",
        default_factory=list
    )
    
    class Config:
        """Pydantic configuration for RecommendationResults."""
        json_schema_extra = {
            "example": {
                "summary": "Your resume matches 75% of the job requirements. Consider adding Docker and AWS experience to strengthen your profile.",
                "recommendations": [
                    {
                        "section": "Skills",
                        "type": "add", 
                        "content": "Add Docker containerization experience",
                        "reason": "Docker is a required skill missing from your resume",
                        "priority": 9
                    }
                ],
                "keyword_suggestions": [
                    "cloud computing",
                    "agile development",
                    "microservices"
                ]
            }
        }
