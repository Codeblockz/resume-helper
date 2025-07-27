"""
API endpoints for resume recommendation generation in Resume Tailor App
"""

from fastapi import APIRouter, HTTPException, BackgroundTasks
from pydantic import BaseModel
from backend.services.ollama_service import OllamaService
from typing import Dict, Any

router = APIRouter(
    prefix="/recommendations",
    tags=["Recommendations"],
    responses={404: {"description": "Not found"}},
)

class RecommendationRequest(BaseModel):
    """Request model for generating recommendations"""
    resume_text: str
    job_description: str
    model_name: str = None

class RecommendationResponse(BaseModel):
    """Response model for recommendation results"""
    tailored_resume: str
    match_score: int
    suggestions: Dict[str, Any]
    processing_time_ms: float = 0.0

@router.post("/", summary="Generate resume recommendations")
async def generate_recommendations(
    request: RecommendationRequest,
    background_tasks: BackgroundTasks
):
    """
    Generate AI-powered recommendations for tailoring a resume to a job description.
    Returns the tailored resume and specific suggestions.
    """
    try:
        # Initialize Ollama service
        ollama_service = OllamaService()

        # Check if custom model is available, otherwise use default
        if request.model_name:
            models = ollama_service.get_model_list()
            if request.model_name not in models:
                raise HTTPException(
                    status_code=400,
                    detail=f"Model {request.model_name} not found. Available models: {models}"
                )

        # Start processing (this could be moved to background)
        tailored_resume = ollama_service.tailor_resume(
            request.resume_text,
            request.job_description,
            model=request.model_name
        )

        # Generate additional analysis (mock for now)
        match_score = 85  # Placeholder - would come from actual analysis

        suggestions = {
            "keywords": ["Python", "Django", "AWS"],
            "sections_to_add": ["Cloud Certifications"],
            "achievements_to_highlight": [
                {"description": "Successfully migrated database to PostgreSQL",
                 "metrics": ["Increased performance by 35%"]}
            ]
        }

        return RecommendationResponse(
            tailored_resume=tailed_resume,
            match_score=match_score,
            suggestions=suggestions
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate recommendations: {str(e)}")

@router.post("/analyze", summary="Analyze resume-job fit")
async def analyze_resume_fit(
    request: RecommendationRequest,
    background_tasks: BackgroundTasks
):
    """
    Analyze how well a resume matches a job description.
    Returns a detailed breakdown of matches, gaps, and recommendations.
    """
    try:
        # For now, we'll use the same service but with different output formatting
        ollama_service = OllamaService()

        tailored_resume = ollama_service.tailor_resume(
            request.resume_text,
            request.job_description,
            model=request.model_name
        )

        analysis_result = {
            "match_score": 85,  # Placeholder
            "matches": [
                {"skill": "Python Development", "confidence": 0.95},
                {"skill": "Web Application Design", "confidence": 0.87}
            ],
            "gaps": [
                {"required_skill": "Kubernetes Experience", "explanation": "Job requires Kubernetes experience, but resume shows limited containerization experience"},
                {"missing_keyword": "Microservices Architecture", "explanation": "This is a key term in the job description that appears less prominently in your resume"}
            ],
            "recommendations": [
                {
                    "section": "Skills",
                    "suggestion": "Add 'Kubernetes' to your skills section and mention any containerization experience you have, even if limited"
                },
                {
                    "section": "Experience",
                    "suggestion": "Highlight your work with web applications by mentioning they followed microservices principles where applicable"
                }
            ]
        }

        return analysis_result

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to analyze resume: {str(e)}")
