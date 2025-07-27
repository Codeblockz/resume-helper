"""
Configuration settings for Resume Tailor App
"""

from pydantic import BaseSettings

class Settings(BaseSettings):
    """Application configuration settings"""

    # API Configuration
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000
    API_DEBUG: bool = True

    # Database Configuration
    DATABASE_URL: str = "sqlite:///./data/resume_tailor.db"

    # Ollama AI Integration
    OLLAMA_HOST: str = "http://localhost"
    OLLAMA_PORT: int = 11434
    DEFAULT_MODEL: str = "llama3.1"

    # File Storage
    UPLOAD_DIRECTORY: str = "/tmp/resume_tailor_uploads"
    MAX_FILE_SIZE_MB: int = 5

    class Config:
        """Settings configuration"""
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()
