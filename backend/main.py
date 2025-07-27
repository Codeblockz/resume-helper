"""
Resume Tailor App - FastAPI Backend
"""

import uvicorn
from fastapi import FastAPI
from backend.core.config import settings

app = FastAPI(
    title="Resume Tailor API",
    description="AI-powered resume tailoring service for job applications",
    version="0.1.0",
    contact={
        "name": "Resume Tailor Team",
        "email": "support@resumetailor.app",
    },
)

# Import routers to register them
from backend.api.upload import router as upload_router
from backend.api.jobs import router as jobs_router
from backend.api.recommendations import router as recommendations_router
from backend.api.tailoring import router as tailoring_router

app.include_router(upload_router)
app.include_router(jobs_router)
app.include_router(recommendations_router)
app.include_router(tailoring_router)

@app.get("/")
def read_root():
    """Root endpoint for health check"""
    return {
        "message": "Welcome to Resume Tailor API",
        "status": "up",
        "version": app.version,
    }

# Set up static file serving
from backend.core.static import setup_static_routes
setup_static_routes(app)

if __name__ == "__main__":
    uvicorn.run(
        app,
        host=settings.API_HOST,
        port=settings.API_PORT,
        reload=True,
    )
