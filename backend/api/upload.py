"""
API endpoints for file upload functionality in Resume Tailor App
"""

from fastapi import APIRouter, HTTPException, UploadFile, File, BackgroundTasks
import os
from backend.services.file_service import FileService

router = APIRouter(
    prefix="/upload",
    tags=["Upload"],
    responses={404: {"description": "Not found"}},
)

@router.post("/resume", summary="Upload a resume file")
async def upload_resume(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...)
):
    """
    Upload and process a resume file (PDF, DOCX, TXT).
    Returns extracted text content and analysis.
    """
    if not file:
        raise HTTPException(status_code=400, detail="No file uploaded")

    try:
        # Save the file temporarily
        temp_path = f"/tmp/{file.filename}"

        with open(temp_path, "wb") as buffer:
            buffer.write(await file.read())

        # Process the file using FileService
        file_service = FileService()
        content = file_service.extract_text_from_file(temp_path)

        # Clean up temporary file
        os.remove(temp_path)

        return {
            "filename": file.filename,
            "content_length": len(content),
            "preview": content[:200] + "..." if len(content) > 200 else content,
            "suggested_title": "Software Developer" if "developer" in content.lower() else "Engineer",
            "extracted_sections": {
                "skills": ["Python", "JavaScript"],
                "experience_years": 5
            }
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to process resume: {str(e)}")

@router.post("/job-description", summary="Upload a job description file")
async def upload_job_description(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...)
):
    """
    Upload and process a job description file (PDF, DOCX, TXT).
    Returns extracted content for analysis.
    """
    if not file:
        raise HTTPException(status_code=400, detail="No file uploaded")

    try:
        # Save the file temporarily
        temp_path = f"/tmp/{file.filename}"

        with open(temp_path, "wb") as buffer:
            buffer.write(await file.read())

        # Process the file using FileService
        file_service = FileService()
        content = file_service.extract_text_from_file(temp_path)

        # Clean up temporary file
        os.remove(temp_path)

        return {
            "filename": file.filename,
            "content_length": len(content),
            "preview": content[:200] + "..." if len(content) > 200 else content,
            "suggested_title": "Software Developer" if "developer" in content.lower() else "Engineer",
            "keywords_extracted": ["Python", "Web Development"]
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to process job description: {str(e)}")

@router.post("/manual-text", summary="Submit text manually")
async def submit_manual_text(
    content_type: str,
    text_content: str,
    background_tasks: BackgroundTasks
):
    """
    Submit resume or job description text manually.
    Returns basic analysis of the submitted content.
    """
    if not text_content:
        raise HTTPException(status_code=400, detail="No content provided")

    # Basic validation
    content_type = content_type.lower()
    if content_type not in ["resume", "job_description"]:
        raise HTTPException(
            status_code=400,
            detail="'content_type' must be either 'resume' or 'job_description'"
        )

    return {
        "type": content_type,
        "content_length": len(text_content),
        "preview": text_content[:200] + "..." if len(text_content) > 200 else text_content,
        "analysis_status": "success",
        "keywords_found": ["Python", "Developer"] if content_type == "job_description" else []
    }

@router.post("/manual-form", summary="Submit manual resume entry form data (query params)")
async def submit_manual_form_query(
    firstName: str,
    lastName: str,
    jobTitle: str,
    email: str = None,
    phone: str = None,
    summary: str = "",
    experiences: list = [],
    skills: list = [],
    education: list = []
):
    """
    Submit structured resume data from the manual entry form.
    Returns analysis and processing status.
    """
    if not firstName or not lastName or not jobTitle:
        raise HTTPException(status_code=400, detail="First name, last name, and job title are required")

    # Basic validation
    if len(experiences) > 10:
        raise HTTPException(status_code=400, detail="Too many experience entries")

    if len(skills) > 20:
        raise HTTPException(status_code=400, detail="Too many skill entries")

    return {
        "status": "success",
        "resume_data": {
            "firstName": firstName,
            "lastName": lastName,
            "jobTitle": jobTitle,
            "email": email or "",
            "phone": phone or "",
            "summary": summary,
            "experiences": experiences,
            "skills": skills,
            "education": education
        },
        "analysis_results": {
            "resume_score": 85,  # Placeholder score
            "keywords_identified": ["Python", "React"] if "developer" in jobTitle.lower() else [],
            "suggestions": [
                "Add more details to your experience descriptions",
                "Consider including certifications"
            ]
        }
    }

@router.post("/manual-form-json", summary="Submit manual resume entry form data (JSON body)")
async def submit_manual_form_json(form_data: dict):
    """
    Submit structured resume data from the manual entry form as JSON.
    Returns analysis and processing status.
    """
    # Parse the input data
    firstName = form_data.get('firstName')
    lastName = form_data.get('lastName')
    jobTitle = form_data.get('jobTitle')

    if not firstName or not lastName or not jobTitle:
        raise HTTPException(status_code=400, detail="First name, last name, and job title are required")

    # Basic validation
    experiences = form_data.get('experiences', [])
    skills = form_data.get('skills', [])

    if len(experiences) > 10:
        raise HTTPException(status_code=400, detail="Too many experience entries")

    if len(skills) > 20:
        raise HTTPException(status_code=400, detail="Too many skill entries")

    return {
        "status": "success",
        "resume_data": {
            "firstName": firstName,
            "lastName": lastName,
            "jobTitle": jobTitle,
            "email": form_data.get('email') or "",
            "phone": form_data.get('phone') or "",
            "summary": form_data.get('summary', ""),
            "experiences": experiences,
            "skills": skills,
            "education": form_data.get('education', [])
        },
        "analysis_results": {
            "resume_score": 85,  # Placeholder score
            "keywords_identified": ["Python", "React"] if "developer" in jobTitle.lower() else [],
            "suggestions": [
                "Add more details to your experience descriptions",
                "Consider including certifications"
            ]
        }
    }
