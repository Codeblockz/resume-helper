"""
PDF Parser module for Resume Helper.

This module handles the extraction of text and structure from PDF resume files.
It uses PyPDF2 for basic text extraction and Ollama for section identification.
"""

import io
import os
import PyPDF2
from langchain_ollama import OllamaLLM
from langchain.prompts import PromptTemplate


class ResumeParser:
    """Parser for extracting and structuring content from PDF resumes."""
    
    def __init__(self, model_name="qwen3:32b"):
        """
        Initialize the ResumeParser.
        
        Args:
            model_name (str): Name of the Ollama model to use for section identification.
        """
        self.llm = OllamaLLM(model=model_name)
        
        # Create prompt template for section identification
        self.section_id_prompt = PromptTemplate(
            input_variables=["resume_text"],
            template="""
            Identify the sections in this resume and extract the content for each section.
            Common resume sections include:
            - Contact Information
            - Summary/Objective
            - Education
            - Experience/Work History
            - Skills
            - Projects
            - Certifications
            - Publications
            - References
            
            Resume:
            {resume_text}
            
            Return the sections in JSON format with section names as keys and content as values.
            Format the JSON as follows:
            {{
                "Contact Information": "...",
                "Summary": "...",
                "Education": "...",
                ...
            }}
            """
        )
    
    def extract_text_from_pdf(self, pdf_file):
        """
        Extract text content from a PDF file.
        
        Args:
            pdf_file (str, bytes, or file-like object): The PDF file to extract text from.
                Can be a file path string, bytes, or file-like object.
            
        Returns:
            str: The extracted text content.
        """
        try:
            # Create a local variable to hold any file objects we open
            # so they don't get garbage collected before we're done
            file_obj = None
            
            if isinstance(pdf_file, str):  # If it's a file path
                # Check if the file exists
                if not os.path.exists(pdf_file):
                    raise FileNotFoundError(f"PDF file not found: {pdf_file}")
                
                # Open the file and keep a reference to it
                file_obj = open(pdf_file, 'rb')
                reader = PyPDF2.PdfReader(file_obj)
            else:  # Assume it's already bytes or file-like
                if hasattr(pdf_file, 'read'):  # File-like object
                    reader = PyPDF2.PdfReader(pdf_file)
                else:  # Bytes
                    # Create a BytesIO object and keep a reference to it
                    file_obj = io.BytesIO(pdf_file)
                    reader = PyPDF2.PdfReader(file_obj)
            
            # Extract text from all pages
            text = ""
            for page in reader.pages:
                text += page.extract_text() + "\n"
                
            # Close the file if we opened it
            if file_obj:
                file_obj.close()
                
            return text
        except Exception as e:
            print(f"Error extracting text from PDF: {e}")
            raise ValueError(f"Failed to extract text from PDF: {e}")
    
    def identify_sections(self, resume_text):
        """
        Identify and extract sections from resume text using LLM.
        
        Args:
            resume_text (str): The text content of the resume.
            
        Returns:
            dict: A dictionary of identified sections with their content.
        """
        try:
            # Use the prompt and LLM directly instead of LLMChain
            chain = self.section_id_prompt | self.llm
            result = chain.invoke({"resume_text": resume_text})
            
            # Parse the JSON result
            import json
            try:
                sections = json.loads(result)
                return sections
            except json.JSONDecodeError as json_err:
                print(f"Error parsing JSON from LLM response: {json_err}")
                print(f"Raw LLM response: {result[:500]}...")  # Print first 500 chars of response
                return self._basic_section_identification(resume_text)
        except Exception as e:
            print(f"Error identifying sections: {e}")
            # Fallback to basic section identification
            return self._basic_section_identification(resume_text)
    
    def _basic_section_identification(self, resume_text):
        """
        Basic section identification as fallback when LLM fails.
        
        Args:
            resume_text (str): The text content of the resume.
            
        Returns:
            dict: A dictionary with a single 'Full Text' section.
        """
        return {"Full Text": resume_text}
    
    def parse_resume(self, pdf_file):
        """
        Parse a PDF resume file into structured sections.
        
        Args:
            pdf_file (bytes or file-like object): The PDF resume file.
            
        Returns:
            dict: A dictionary of resume sections with their content.
        """
        # Extract text from PDF
        resume_text = self.extract_text_from_pdf(pdf_file)
        
        # Identify sections
        sections = self.identify_sections(resume_text)
        
        return {
            "raw_text": resume_text,
            "sections": sections
        }


# Example usage
if __name__ == "__main__":
    parser = ResumeParser()
    
    # Example with file path
    resume_data = parser.parse_resume("path/to/resume.pdf")
    
    # Print sections
    for section_name, content in resume_data["sections"].items():
        print(f"=== {section_name} ===")
        print(content)
        print()
