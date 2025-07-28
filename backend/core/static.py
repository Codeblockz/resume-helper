"""
Static file serving for Resume Tailor App
"""

from fastapi.staticfiles import StaticFiles

def setup_static_routes(app):
    """Set up static file routes for frontend assets"""
    # Serve production build at root, API on /api subpath
    app.mount("/static", StaticFiles(directory="/app/static"), name="static")
    app.mount("/", StaticFiles(directory="/app/static/public", html=True), name="frontend")

# Add this to main.py after app creation
if __name__ == "__main__":
    from backend.main import app
    setup_static_routes(app)
