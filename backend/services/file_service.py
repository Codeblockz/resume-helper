"""
File handling services for Resume Tailor App
"""

import os
import uuid
from pathlib import Path
from typing import Tuple, Optional
from backend.core.config import settings

def ensure_upload_directory_exists():
    """Ensure the upload directory exists"""
    upload_dir = Path(settings.UPLOAD_DIRECTORY)
    upload_dir.mkdir(parents=True, exist_ok=True)

def get_unique_file_path(original_filename: str) -> str:
    """Generate a unique file path for uploaded resume"""
    # Extract file extension
    if '.' in original_filename:
        ext = original_filename.split('.')[-1]
        filename = f"{uuid.uuid4()}.{ext}"
    else:
        filename = f"{uuid.uuid4()}"

    return str(Path(settings.UPLOAD_DIRECTORY) / filename)

def save_uploaded_file(file_bytes: bytes, original_filename: str) -> str:
    """Save an uploaded file and return the saved path"""
    ensure_upload_directory_exists()
    unique_path = get_unique_file_path(original_filename)
    Path(unique_path).write_bytes(file_bytes)
    return unique_path

def delete_file(file_path: str) -> bool:
    """Delete a file from the upload directory"""
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
            return True
        return False
    except OSError as e:
        print(f"Error deleting file {file_path}: {e}")
        return False

def extract_text_from_pdf(pdf_path: str) -> Optional[str]:
    """Extract text content from a PDF file"""
    try:
        import pdfplumber
        with pdfplumber.open(pdf_path) as pdf:
            text = ""
            for page in pdf.pages:
                text += page.extract_text()
            return text.strip() if text else None
    except Exception as e:
        print(f"Error extracting text from PDF: {e}")
        return None

def extract_text_from_docx(docx_path: str) -> Optional[str]:
    """Extract text content from a DOCX file"""
    try:
        from docx import Document
        document = Document(docx_path)
        return " ".join([para.text for para in document.paragraphs]).strip()
    except Exception as e:
        print(f"Error extracting text from DOCX: {e}")
        return None

def extract_text_from_file(file_path: str) -> Optional[str]:
    """Extract text content based on file extension"""
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

    ext = file_path.lower().split('.')[-1]

    if ext == "pdf":
        return extract_text_from_pdf(file_path)
    elif ext == "docx":
        return extract_text_from_docx(file_path)
    elif ext in ["txt", "md"]:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read().strip()
        except Exception as e:
            print(f"Error reading text file: {e}")
            return None
    else:
        raise ValueError(f"Unsupported file type: {ext}")
