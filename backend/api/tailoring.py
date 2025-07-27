"""
API endpoints for resume tailoring functionality in Resume Tailor App
"""

from fastapi import APIRouter, HTTPException, BackgroundTasks
from pydantic import BaseModel
from backend.services.ollama_service import OllamaService

router = APIRouter(
    prefix="/tailoring",
    tags=["Tailoring"],
    responses={404: {"description": "Not found"}},
)

class TailoringRequest(BaseModel):
    """Request model for resume tailoring"""
    resume_text: str
    job_description: str
    model_name: str = None

@router.post("/")
async def tailor_resume(
    request: TailoringRequest,
    background_tasks: BackgroundTasks
):
    """
    Tailor a resume to match a specific job description using AI.
    Returns the optimized resume with suggested changes.
    """
    try:
        ollama_service = OllamaService()

        # Check if custom model is available, otherwise use default
        if request.model_name:
            models = ollama_service.get_model_list()
            if request.model_name not in models:
                raise HTTPException(
                    status_code=400,
                    detail=f"Model {request.model_name} not found. Available models: {models}"
                )

        tailored_resume = ollama_service.tailor_resume(
            request.resume_text,
            request.job_description,
            model=request.model_name
        )

        return {
            "original_resume_length": len(request.resume_text),
            "tailored_resume_length": len(tailored_resume),
            "tailored_resume": tailored_resume,
            "keywords_added": ["Python", "Django", "AWS"],  # Placeholder
            "sections_reordered": True,  # Placeholder
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to tailor resume: {str(e)}")

@router.post("/diff")
async def get_tailoring_diff(
    request: TailoringRequest,
    background_tasks: BackgroundTasks
):
    """
    Get a diff showing changes made during tailoring.
    Returns original vs. tailored comparison.
    """
    try:
        ollama_service = OllamaService()

        # Generate both versions for comparison
        original = request.resume_text
        tailored = ollama_service.tailor_resume(
            original,
            request.job_description,
            model=request.model_name
        )

        # Simple diff algorithm (placeholder)
        diff_lines = []
        original_lines = original.split('\n')
        tailored_lines = tailored.split('\n')

        for i, (orig_line, tail_line) in enumerate(zip(original_lines, tailored_lines)):
            if orig_line != tail_line:
                diff_lines.append({
                    "line_number": i + 1,
                    "original": orig_line,
                    "tailored": tail_line,
                    "type": "modified"
                })

        return {
            "diff": diff_lines,
            "total_changes": len(diff_lines),
            "estimated_impact_score": max(0, min(100, len(diff_lines) * 5)),
            "tailored_resume": tailored
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate diff: {str(e)}")
