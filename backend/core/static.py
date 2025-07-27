"""
Static file serving for Resume Tailor App
"""

from fastapi.staticfiles import StaticFiles

def setup_static_routes(app):
    """Set up static file routes for frontend assets"""
    app.mount("/static", StaticFiles(directory="backend/static"), name="static")
    app.mount("/", StaticFiles(directory="backend/static", html=True), name="frontend")

# Add this to main.py after app creation
if __name__ == "__main__":
    from backend.main import app
    setup_static_routes(app)
