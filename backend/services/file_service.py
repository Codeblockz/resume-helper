"""
File processing services for Resume Tailor App
"""

import os
from PyPDF2 import PdfReader
from docx import Document

class FileService:
    """Service class for handling file operations and text extraction"""

    def extract_text_from_file(self, file_path: str) -> str:
        """
        Extract text content from various file formats.
        Supports PDF, DOCX, and TXT files.
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")

        _, ext = os.path.splitext(file_path)
        ext = ext.lower()

        if ext == '.pdf':
            return self._extract_text_from_pdf(file_path)
        elif ext == '.docx':
            return self._extract_text_from_docx(file_path)
        elif ext in ['.txt']:
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        else:
            raise ValueError(f"Unsupported file format: {ext}")

    def _extract_text_from_pdf(self, pdf_path: str) -> str:
        """Extract text from PDF using PyPDF2"""
        try:
            with open(pdf_path, 'rb') as f:
                reader = PdfReader(f)
                text = ""
                for page in range(len(reader.pages)):
                    text += reader.pages[page].extract_text() or ""
                return text.strip()
        except Exception as e:
            raise RuntimeError(f"Failed to extract text from PDF: {str(e)}")

    def _extract_text_from_docx(self, docx_path: str) -> str:
        """Extract text from DOCX using python-docx"""
        try:
            document = Document(docx_path)
            text = []
            for para in document.paragraphs:
                text.append(para.text)
            return "\n".join(text).strip()
        except Exception as e:
            raise RuntimeError(f"Failed to extract text from DOCX: {str(e)}")

    def save_text_to_file(self, content: str, output_path: str) -> None:
        """Save text content to a file"""
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(content)
        except Exception as e:
            raise RuntimeError(f"Failed to save text to file: {str(e)}")

    def get_file_size(self, file_path: str) -> int:
        """Get size of a file in bytes"""
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")
        return os.path.getsize(file_path)
