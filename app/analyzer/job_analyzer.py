"""
Job Description Analyzer module for Resume Helper.

This module processes job posting text to identify key requirements and keywords.
It uses Ollama for natural language processing with Pydantic for structured outputs.
"""

from langchain_ollama import OllamaLLM
from langchain.prompts import PromptTemplate
from langchain.output_parsers import PydanticOutputParser

from ..models.responses import JobRequirements


class JobAnalyzer:
    """Analyzer for processing job descriptions and extracting requirements with structured outputs."""
    
    def __init__(self, model_name="qwen3:32b"):
        """
        Initialize the JobAnalyzer with Pydantic output parsing.
        
        Args:
            model_name (str): Name of the Ollama model to use for analysis.
        """
        self.llm = OllamaLLM(model=model_name)
        self.output_parser = PydanticOutputParser(pydantic_object=JobRequirements)
        
        # Create prompt template for job description analysis with format instructions
        self.job_analysis_prompt = PromptTemplate(
            template="""
            Analyze the following job description and extract structured requirements.
            
            {format_instructions}
            
            Job Description:
            {job_description}
            
            Please extract:
            1. Required skills - Essential technical and professional skills
            2. Preferred skills - Nice-to-have skills that would be beneficial
            3. Required experience - Work experience and background requirements
            4. Required education - Educational qualifications and degrees
            5. Key responsibilities - Main duties and responsibilities of the role
            6. Important keywords - Keywords valuable for ATS optimization
            
            Ensure all lists contain clear, specific string items.
            """,
            input_variables=["job_description"],
            partial_variables={
                "format_instructions": self.output_parser.get_format_instructions()
            }
        )
    
    def analyze_job_description(self, job_description_text: str) -> JobRequirements:
        """
        Analyze a job description to extract structured requirements using Pydantic.
        
        Args:
            job_description_text (str): The text content of the job description.
            
        Returns:
            JobRequirements: A Pydantic model containing structured job requirements.
        """
        if not job_description_text or not job_description_text.strip():
            print("Warning: Empty job description provided")
            return JobRequirements()
            
        try:
            # Create chain with structured output parsing
            chain = self.job_analysis_prompt | self.llm | self.output_parser
            
            # Invoke chain with structured parsing
            result = chain.invoke({"job_description": job_description_text})
            
            # Return the validated Pydantic model
            return result
            
        except Exception as parse_err:
            print(f"Error parsing structured output: {parse_err}")
            # Fall back to manual parsing
            return self._fallback_parse(job_description_text)
        except Exception as e:
            print(f"Error analyzing job description: {e}")
            # Return empty structure as fallback
            return JobRequirements()
    
    def _fallback_parse(self, job_description_text: str) -> JobRequirements:
        """
        Fallback method using traditional parsing if Pydantic parsing fails.
        
        Args:
            job_description_text (str): The job description text.
            
        Returns:
            JobRequirements: Parsed requirements using fallback method.
        """
        try:
            # Use simpler prompt for fallback
            simple_prompt = PromptTemplate(
                input_variables=["job_description"],
                template="""
                Analyze this job description and extract requirements in JSON format:
                {job_description}
                
                Return JSON with keys: required_skills, preferred_skills, required_experience, 
                required_education, responsibilities, keywords
                """
            )
            
            chain = simple_prompt | self.llm
            result = chain.invoke({"job_description": job_description_text})
            
            # Manual JSON parsing with validation
            import json
            result = result.strip()
            
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
                
                # Validate and create JobRequirements
                return JobRequirements(**data)
            else:
                print("No valid JSON found in fallback parsing")
                return JobRequirements()
                
        except Exception as e:
            print(f"Fallback parsing failed: {e}")
            return JobRequirements()
    
    def analyze_job_description_legacy(self, job_description_text: str) -> dict:
        """
        Legacy method that returns a dictionary for backward compatibility.
        
        Args:
            job_description_text (str): The job description text.
            
        Returns:
            dict: Dictionary representation of job requirements.
        """
        requirements = self.analyze_job_description(job_description_text)
        return requirements.model_dump()
    
    def extract_keywords(self, job_description_text: str) -> list:
        """
        Extract just the keywords from a job description.
        
        Args:
            job_description_text (str): The text content of the job description.
            
        Returns:
            list: A list of important keywords from the job description.
        """
        requirements = self.analyze_job_description(job_description_text)
        return requirements.keywords


# Example usage
if __name__ == "__main__":
    analyzer = JobAnalyzer()
    
    # Example job description
    job_description = """
    Software Engineer
    
    Requirements:
    - Bachelor's degree in Computer Science or related field
    - 3+ years of experience in Python development
    - Experience with web frameworks such as Django or Flask
    - Strong understanding of data structures and algorithms
    - Experience with SQL and database design
    
    Preferred Qualifications:
    - Master's degree in Computer Science
    - Experience with cloud platforms (AWS, Azure, GCP)
    - Knowledge of machine learning frameworks
    - Experience with containerization (Docker, Kubernetes)
    
    Responsibilities:
    - Design and implement new features for our platform
    - Collaborate with cross-functional teams
    - Write clean, maintainable, and efficient code
    - Participate in code reviews and provide feedback
    - Troubleshoot and debug issues in production
    """
    
    # Analyze job description
    requirements = analyzer.analyze_job_description(job_description)
    
    # Print requirements using Pydantic model
    print("=== Required Skills ===")
    for skill in requirements.required_skills:
        print(f"- {skill}")
    print()
    
    print("=== Preferred Skills ===")
    for skill in requirements.preferred_skills:
        print(f"- {skill}")
    print()
    
    print("=== Required Experience ===")
    for exp in requirements.required_experience:
        print(f"- {exp}")
    print()
    
    print("=== Required Education ===")
    for edu in requirements.required_education:
        print(f"- {edu}")
    print()
    
    print("=== Responsibilities ===")
    for resp in requirements.responsibilities:
        print(f"- {resp}")
    print()
    
    print("=== Keywords ===")
    for keyword in requirements.keywords:
        print(f"- {keyword}")
    print()
