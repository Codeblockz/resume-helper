"""
PDF Parser module for Resume Helper.

This module handles the extraction of text and structure from PDF resume files.
It uses PyPDF2 for basic text extraction and Ollama for section identification.
"""

import io
import PyPDF2
from langchain.llms import Ollama
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate


class ResumeParser:
    """Parser for extracting and structuring content from PDF resumes."""
    
    def __init__(self, model_name="llama3"):
        """
        Initialize the ResumeParser.
        
        Args:
            model_name (str): Name of the Ollama model to use for section identification.
        """
        self.llm = Ollama(model=model_name)
        
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
        
        self.section_id_chain = LLMChain(llm=self.llm, prompt=self.section_id_prompt)
    
    def extract_text_from_pdf(self, pdf_file):
        """
        Extract text content from a PDF file.
        
        Args:
            pdf_file (bytes or file-like object): The PDF file to extract text from.
            
        Returns:
            str: The extracted text content.
        """
        if isinstance(pdf_file, str):  # If it's a file path
            with open(pdf_file, 'rb') as file:
                pdf_bytes = file.read()
        else:  # Assume it's already bytes or file-like
            pdf_bytes = pdf_file
            
        reader = PyPDF2.PdfReader(io.BytesIO(pdf_bytes))
        text = ""
        for page in reader.pages:
            text += page.extract_text() + "\n"
        return text
    
    def identify_sections(self, resume_text):
        """
        Identify and extract sections from resume text using LLM.
        
        Args:
            resume_text (str): The text content of the resume.
            
        Returns:
            dict: A dictionary of identified sections with their content.
        """
        try:
            result = self.section_id_chain.run(resume_text=resume_text)
            # Parse the JSON result
            import json
            sections = json.loads(result)
            return sections
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
