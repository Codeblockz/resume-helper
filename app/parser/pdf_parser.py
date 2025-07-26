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

    def extract_style_information(self, resume_text):
        """
        Extract style information from resume text by analyzing formatting patterns.

        Args:
            resume_text (str): The raw text content of the resume.

        Returns:
            Dict[str, str]: CSS style mappings for different sections and inline styles.
        """
        styles = {}
        section_styles = {}  # Section-level styles
        line_styles = []     # Line-level formatting information

        # Analyze section headers to determine typical formatting
        lines = [line.strip() for line in resume_text.split('\n') if line.strip()]

        # Look for common section patterns (all-caps, bold markers)
        current_section = None
        previous_indentation = 0
        section_start_indices = {}  # Track where each section starts

        for i, line in enumerate(lines):
            # Check for section header patterns - more comprehensive detection
            is_section_header = False
            indentation = self._calculate_indentation(line)

            # Pattern 1: All caps or large text (simulated by checking if line has no lowercase letters)
            if line.isupper() and len(line) > 2:
                is_section_header = True

            # Pattern 2: Underlined text (simulated by checking for repeated characters)
            elif len(line) > 3 and any(char == '=' or char == '-' or char == '_' for char in line):
                is_section_header = True

            # Pattern 3: Line followed by content indentation (section header if much less indented than next lines)
            elif i + 1 < len(lines):
                next_line_indentation = self._calculate_indentation(lines[i+1])
                prev_line_indentation = previous_indentation if i > 0 else 0

                # Consider as section header if:
                # - Not all caps (already handled above) AND
                # - Has more than 2 words AND
                # - Is much less indented than the next line (section start)
                if (not line.isupper() and len(line.split()) > 2 and
                    indentation < next_line_indentation - 1):
                    is_section_header = True

            # Pattern 4: Bold text markers (*text* or __text__)
            elif (line.startswith('*') and line.endswith('*')) or (line.startswith('_') and line.endswith('_')):
                is_section_header = True
                line_styles.append({'line': i, 'style': 'font-weight: bold'})

            # Pattern 5: Text with trailing colons or in angle brackets
            elif line.endswith(':') or ('<' in line and '>' in line):
                is_section_header = True

            # If we detected a section header, assign styles and record position
            if is_section_header:
                # Determine the CSS class based on content with better keyword matching
                lower_content = line.lower()

                # More comprehensive keyword matching for different section types
                if any(keyword in lower_content for keyword in ['name', 'address', 'phone', 'email', 'contact']):
                    css_class = "resume-contact"
                elif any(keyword in lower_content for keyword in ['summary', 'objective', 'professional summary', 'career objective']):
                    css_class = "resume-summary"
                elif any(keyword in lower_content for keyword in
                         ['experience', 'work history', 'employment history', 'professional experience',
                          'career experience', 'work background']):
                    css_class = "resume-experience"
                elif any(keyword in lower_content for keyword in
                         ['education', 'degrees', 'schooling', 'academic background',
                          'educational qualifications', 'institutions attended']):
                    css_class = "resume-education"
                elif any(keyword in lower_content for keyword in
                         ['skills', 'abilities', 'competencies', 'technical skills',
                          'professional skills', 'core competencies']):
                    css_class = "resume-skills"
                elif any(keyword in lower_content for keyword in
                         ['projects', 'project experience', 'portfolios', 'notable projects']):
                    css_class = "resume-projects"
                elif any(keyword in lower_content for keyword in
                         ['certifications', 'licenses', 'professional certifications',
                          'industry certifications', 'accreditations']):
                    css_class = "resume-certifications"
                else:
                    css_class = "resume-section"

                current_section = line
                section_styles[current_section] = css_class
                section_start_indices[current_section] = i

            # Detect bullet points or numbered lists with better patterns
            elif (line.startswith('- ') or line.startswith('• ')
                  or line.startswith('•') or ':' in line or '-' in line[:2]):
                if i > 0 and current_section:
                    if section_styles.get(current_section) != "resume-list":
                        section_styles[current_section] = "resume-list"
            else:
                # Update previous indentation for the next iteration
                previous_indentation = indentation

        # Additional heading detection - first line or lines after blank lines
        for i, line in enumerate(lines):
            if (i == 0 or lines[i-1] == '') and len(line) > 5:
                if not any(char.isdigit() for char in line[:3]) and ':' not in line:  # Not a bullet point
                    if current_section is None or i < section_start_indices.get(current_section, float('inf')):
                        if line.lower() not in [k.lower() for k in section_styles.keys()]:
                            css_class = "resume-heading"
                            section_styles[line] = css_class

        styles['sections'] = section_styles
        return styles

    def _calculate_indentation(self, line):
        """
        Calculate indentation level of a line (number of leading spaces/tabs).

        Args:
            line (str): The text line to analyze.

        Returns:
            int: Number of indent characters at the start of the line.
        """
        indent = 0
        for char in line:
            if char == ' ' or char == '\t':
                indent += 1
            else:
                break
        return indent

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

        # Extract style information before section identification
        styles = self.extract_style_information(resume_text)

        # Identify sections using structured parsing
        sections = self.identify_sections(resume_text)

        # Apply style information to the sections model
        if hasattr(sections, 'styles'):
            for section_name, css_class in styles.items():
                # Map section names (e.g., "Contact Information" -> contact_information)
                field_name = None
                lower_section = section_name.lower()
                
                if 'contact' in lower_section or 'name' in lower_section:
                    field_name = 'contact_information'
                elif 'summary' in lower_section or 'objective' in lower_section:
                    field_name = 'summary'
                elif 'education' in lower_section or 'degrees' in lower_section:
                    field_name = 'education'
                elif 'experience' in lower_section or 'work history' in lower_section:
                    field_name = 'experience'
                elif 'skills' in lower_section or 'abilities' in lower_section:
                    field_name = 'skills'
                elif 'projects' in lower_section:
                    field_name = 'projects'
                elif 'certifications' in lower_section or 'licenses' in lower_section:
                    field_name = 'certifications'
                
                if field_name and hasattr(sections, field_name):
                    # Get the current styles dict and update it
                    existing_styles = getattr(sections.styles, field_name, {})
                    existing_styles[section_name] = css_class

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
