"""
Database models for Resume Tailor App using SQLAlchemy
"""

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship

Base = declarative_base()

class User(Base):
    """User model for authentication and account management"""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    hashed_password = Column(String(100), nullable=False)
    is_active = Column(Boolean, default=True)

    resumes = relationship("Resume", back_populates="owner")
    job_postings = relationship("JobPosting", back_populates="creator")

class Resume(Base):
    """Resume model for storing parsed resume data"""
    __tablename__ = "resumes"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    original_filename = Column(String(100), nullable=False)
    file_path = Column(String(255), nullable=False)  # Path to stored file
    content_text = Column(Text, nullable=True)  # Full text content of resume

    owner = relationship("User", back_populates="resumes")
    analyses = relationship("ResumeAnalysis", back_populates="resume")

class JobPosting(Base):
    """Job posting model for storing job description data"""
    __tablename__ = "job_postings"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    title = Column(String(100), nullable=False)
    company = Column(String(100), nullable=True)
    description_text = Column(Text, nullable=False)  # Full job description
    url = Column(String(255), nullable=True)

    creator = relationship("User", back_populates="job_postings")
    analyses = relationship("ResumeAnalysis", back_populates="job")

class ResumeAnalysis(Base):
    """Model for storing resume-job analysis results"""
    __tablename__ = "resume_analyses"

    id = Column(Integer, primary_key=True, index=True)
    resume_id = Column(Integer, ForeignKey("resumes.id"), nullable=False)
    job_posting_id = Column(Integer, ForeignKey("job_postings.id"), nullable=False)
    match_score = Column(Integer, nullable=False)  # Percentage (0-100)

    # Analysis results stored as JSON
    matches = Column(Text, nullable=True)  # Matches between resume and job
    gaps = Column(Text, nullable=True)  # Gaps that need to be addressed
    recommendations = Column(Text, nullable=True)  # AI-generated recommendations

    resume = relationship("Resume", back_populates="analyses")
    job = relationship("JobPosting", back_populates="analyses")

class Recommendation(Base):
    """Model for storing individual recommendation items"""
    __tablename__ = "recommendations"

    id = Column(Integer, primary_key=True, index=True)
    analysis_id = Column(Integer, ForeignKey("resume_analyses.id"), nullable=False)
    section = Column(String(50), nullable=False)  # e.g., "Skills", "Experience"
    recommendation_type = Column(String(20), nullable=False)  # e.g., "add", "modify"
    content = Column(Text, nullable=False)  # The actual recommendation text
    priority = Column(Integer, nullable=False)  # Priority level (1-10)
