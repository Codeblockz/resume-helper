"""
PDF Parser module for Resume Helper.

This module handles the extraction of text and structure from PDF resume files.
It uses PyPDF2 for basic text extraction and Ollama for section identification
with Pydantic models for structured outputs.
"""

import io
import os
import PyPDF2
from langchain_ollama import OllamaLLM
from langchain.prompts import PromptTemplate
from langchain.output_parsers import PydanticOutputParser

from ..models.responses import ResumeSection, ResumeData


class ResumeParser:
    """Parser for extracting and structuring content from PDF resumes using Pydantic models."""

    def __init__(self, model_name="qwen3:32b"):
        """
        Initialize the ResumeParser.

        Args:
            model_name (str): Name of the Ollama model to use for section identification.
        """
        self.llm = OllamaLLM(model=model_name)
        self.output_parser = PydanticOutputParser(pydantic_object=ResumeSection)

        # Create prompt template for section identification with format instructions
        self.section_id_prompt = PromptTemplate(
            template="""
            Identify and extract the sections from this resume.

            {format_instructions}

            Resume:
            {resume_text}

            Extract common sections like:
            - Contact Information (name, email, phone, address)
            - Summary/Objective statement
            - Education (degrees, institutions, dates)
            - Experience/Work History (job titles, companies, responsibilities)
            - Skills (technical and professional skills)
            - Projects (notable projects with descriptions)
            - Certifications (professional certifications)
            - Other relevant sections if present

            Ensure each field contains clear, specific content.
            """,
            input_variables=["resume_text"],
            partial_variables={
                "format_instructions": self.output_parser.get_format_instructions()
            }
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
        Identify and extract sections from resume text using LLM with structured output parsing.

        Args:
            resume_text (str): The text content of the resume.

        Returns:
            ResumeSection: A Pydantic model containing structured resume sections.
        """
        try:
            # Get raw LLM response first
            chain = self.section_id_prompt | self.llm
            raw_response = chain.invoke({"resume_text": resume_text})
            
            # Preprocess the response to remove thinking tags and clean JSON
            cleaned_response = self._preprocess_llm_response(raw_response)
            
            # Parse the cleaned response with Pydantic
            result = self.output_parser.parse(cleaned_response)
            return result

        except Exception as parse_err:
            print(f"Error parsing structured output: {parse_err}")
            # Fall back to manual parsing if Pydantic parsing fails
            return self._fallback_parse(resume_text)

    def _preprocess_llm_response(self, raw_response):
        """
        Preprocess LLM response to extract clean JSON, removing thinking tags and other artifacts.

        Args:
            raw_response (str): The raw response from the LLM.

        Returns:
            str: Cleaned JSON string ready for Pydantic parsing.
        """
        result = raw_response.strip()
        
        # Remove thinking tags if present
        if "<think>" in result and "</think>" in result:
            think_start = result.find("<think>")
            think_end = result.find("</think>", think_start) + len("</think>")
            result = result[:think_start] + result[think_end:].strip()
        
        # Clean up common LLM formatting artifacts
        if "```json" in result:
            result = result.split("```json")[1].split("```")[0]
        elif "```" in result:
            result = result.split("```")[1].split("```")[0]
        
        # Extract JSON content by finding the outermost braces
        json_start = result.find('{')
        json_end = result.rfind('}') + 1
        
        if json_start >= 0 and json_end > json_start:
            result = result[json_start:json_end]
        
        return result.strip()

    def _basic_section_identification(self, resume_text):
        """
        Basic section identification as fallback when LLM fails.

        Args:
            resume_text (str): The text content of the resume.

        Returns:
            dict: A dictionary with a single 'Full Text' section.
        """
        return {"contact_information": resume_text}

    def _fallback_parse(self, resume_text):
        """
        Fallback method using traditional parsing if Pydantic parsing fails.

        Args:
            resume_text (str): The resume text to parse.

        Returns:
            ResumeSection: Parsed sections using fallback method.
        """
        try:
            # Use simpler prompt for fallback
            simple_prompt = PromptTemplate(
                input_variables=["resume_text"],
                template="""
                Identify and extract the sections from this resume in JSON format:

                {resume_text}

                Return JSON with keys: contact_information, summary, education,
                experience, skills, projects, certifications, additional
                """
            )

            chain = simple_prompt | self.llm
            result = chain.invoke({"resume_text": resume_text})

            # Manual JSON parsing with enhanced cleaning
            import json
            result = result.strip()

            # Handle thinking process in the response
            if "<think>" in result and "</think>" in result:
                # Extract content after thinking tags
                think_start = result.find("<think>")
                think_end = result.find("</think>", think_start) + len("</think>")
                # Remove the thinking part
                result = result[:think_start] + result[think_end:].strip()

            # Clean up common LLM formatting
            if "```json" in result:
                result = result.split("```json")[1].split("```")[0]
            elif "```" in result:
                result = result.split("```")[1].split("```")[0]

            # Find JSON bounds
            json_start = result.find('{')
            json_end = result.rfind('}') + 1

            if json_start >= 0 and json_end > json_start:
                json_str = result[json_start:json_end]
                data = json.loads(json_str)

                # Create ResumeSection with proper field mapping
                return ResumeSection(**data)
            else:
                print("No valid JSON found in fallback parsing")
                basic_sections = self._basic_section_identification(resume_text)
                return ResumeSection(**basic_sections)

        except Exception as e:
            print(f"Fallback parsing failed: {e}")
            basic_sections = self._basic_section_identification(resume_text)
            return ResumeSection(**basic_sections)

    def parse_resume(self, pdf_file):
        """
        Parse a PDF resume file into structured Pydantic model.

        Args:
            pdf_file (bytes or file-like object): The PDF resume file.

        Returns:
            ResumeData: A structured Pydantic model containing raw text and sections.
        """
        # Extract text from PDF
        resume_text = self.extract_text_from_pdf(pdf_file)

        # Identify sections using structured parsing
        sections = self.identify_sections(resume_text)

        return ResumeData(raw_text=resume_text, sections=sections)


# Example usage
if __name__ == "__main__":
    parser = ResumeParser()

    # Example with file path
    resume_data = parser.parse_resume("path/to/resume.pdf")

    # Print sections using Pydantic model attributes
    print("=== Raw Text (first 500 chars) ===")
    print(resume_data.raw_text[:500] + "...")

    print("\n=== Structured Sections ===")
    for field_name, value in resume_data.sections.model_dump().items():
        if value:
            print(f"--- {field_name} ---")
            print(value)
            print()
