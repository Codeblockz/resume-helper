"""
API endpoints for file upload functionality in Resume Tailor App
"""

from fastapi import APIRouter, UploadFile, File, HTTPException, status
from typing import List
import shutil
from backend.services.file_service import save_uploaded_file, extract_text_from_file

router = APIRouter(
    prefix="/upload",
    tags=["Upload"],
    responses={404: {"description": "Not found"}},
)

@router.post("/resume", summary="Upload a resume file")
async def upload_resume(file: UploadFile = File(...)):
    """
    Upload a resume file (PDF, DOCX, TXT).
    Returns the file path and extracted text content.
    """
    if not file:
        raise HTTPException(status_code=400, detail="No file uploaded")

    # Validate file size
    max_size_mb = 5 * 1024 * 1024  # 5MB
    if len(await file.read()) > max_size_mb:
        raise HTTPException(
            status_code=413,
            detail=f"File too large. Maximum size is {max_size_mb / (1024*1024)}MB"
        )

    # Reset file pointer after reading for size validation
    await file.seek(0)

    # Save the file
    try:
        saved_path = save_uploaded_file(await file.read(), file.filename)
        text_content = extract_text_from_file(saved_path)

        return {
            "filename": file.filename,
            "saved_path": saved_path,
            "content_length": len(text_content) if text_content else 0,
            "content_preview": (text_content[:200] + "...") if text_content and len(text_content) > 200 else text_content
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to process file: {str(e)}")

@router.post("/job-description", summary="Upload a job description")
async def upload_job_description(file: UploadFile = File(...)):
    """
    Upload a job description file (PDF, DOCX, TXT) or text.
    Returns the extracted content for analysis.
    """
    if not file:
        raise HTTPException(status_code=400, detail="No file uploaded")

    try:
        saved_path = save_uploaded_file(await file.read(), file.filename)
        text_content = extract_text_from_file(saved_path)

        return {
            "filename": file.filename,
            "content_length": len(text_content) if text_content else 0,
            "content_preview": (text_content[:200] + "...") if text_content and len(text_content) > 200 else text_content
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to process file: {str(e)}")

@router.post("/raw-text", summary="Submit raw text for job description")
async def submit_raw_text(text: str):
    """
    Submit raw text content for a job description.
    Useful for copy-pasting from job listings.
    """
    if not text or len(text.strip()) < 50:
        raise HTTPException(status_code=400, detail="Text is too short or empty")

    return {
        "content_length": len(text),
        "content_preview": (text[:200] + "...") if len(text) > 200 else text
    }
