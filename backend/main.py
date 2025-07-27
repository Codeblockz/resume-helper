"""
Main entry point for Resume Tailor Backend API
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import os

# Import API routers
from backend.api.upload import router as upload_router
from backend.api.recommendations import router as recommendations_router
from backend.api.jobs import router as jobs_router
from backend.api.tailoring import router as tailoring_router

# Initialize FastAPI app
app = FastAPI(
    title="Resume Tailor API",
    description="API for Resume Tailor application with AI-powered resume optimization",
    version="0.1.0",
)

# Configure CORS to allow frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, restrict this to your frontend domains
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routers
app.include_router(upload_router)
app.include_router(recommendations_router)
app.include_router(jobs_router)
app.include_router(tailoring_router)

@app.get("/")
def read_root():
    """Root endpoint returning basic API info"""
    return {
        "message": "Welcome to Resume Tailor API",
        "version": "0.1.0",
        "available_endpoints": {
            "upload_resume": "/upload/resume",
            "upload_job_description": "/upload/job-description",
            "manual_text_submit": "/upload/manual-text",
            # Add other endpoints here
        }
    }

if __name__ == "__main__":
    # Read configuration from environment variables
    host = os.getenv("API_HOST", "0.0.0.0")
    port = int(os.getenv("API_PORT", 8000))

    print(f"Starting Resume Tailor API on http://{host}:{port}")
    uvicorn.run(app, host=host, port=port)
