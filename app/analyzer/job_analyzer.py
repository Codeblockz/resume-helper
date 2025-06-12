"""
Job Description Analyzer module for Resume Helper.

This module processes job posting text to identify key requirements and keywords.
It uses Ollama for natural language processing and extraction.
"""

from langchain_ollama import OllamaLLM
from langchain.prompts import PromptTemplate


class JobAnalyzer:
    """Analyzer for processing job descriptions and extracting requirements."""
    
    def __init__(self, model_name="qwen3:32b"):
        """
        Initialize the JobAnalyzer.
        
        Args:
            model_name (str): Name of the Ollama model to use for analysis.
        """
        self.llm = OllamaLLM(model=model_name)
        
        # Create prompt template for job description analysis
        self.job_analysis_prompt = PromptTemplate(
            input_variables=["job_description"],
            template="""
            Analyze the following job description and extract:
            1. Required skills
            2. Preferred skills
            3. Required experience
            4. Required education
            5. Key responsibilities
            6. Important keywords that would be valuable to include in a resume

            Job Description:
            {job_description}
            
            Return the analysis in JSON format as follows:
            {{
                "required_skills": ["skill1", "skill2", ...],
                "preferred_skills": ["skill1", "skill2", ...],
                "required_experience": ["experience1", "experience2", ...],
                "required_education": ["education1", "education2", ...],
                "responsibilities": ["responsibility1", "responsibility2", ...],
                "keywords": ["keyword1", "keyword2", ...]
            }}
            
            Ensure all lists contain string items, not nested objects.
            IMPORTANT: Return ONLY the JSON object, with no additional text, explanations, or thinking process.
            """
        )
    
    def analyze_job_description(self, job_description_text):
        """
        Analyze a job description to extract requirements and keywords.
        
        Args:
            job_description_text (str): The text content of the job description.
            
        Returns:
            dict: A dictionary containing structured job requirements.
        """
        if not job_description_text or not job_description_text.strip():
            print("Warning: Empty job description provided")
            return self._empty_requirements()
            
        try:
            # Use the prompt and LLM directly instead of LLMChain
            chain = self.job_analysis_prompt | self.llm
            result = chain.invoke({"job_description": job_description_text})
            
            # Parse the JSON result
            import json
            try:
                # Clean the result to ensure it's valid JSON
                # Sometimes LLMs add extra text before or after the JSON
                result = result.strip()
                
                # Handle thinking process in the response
                if "<think>" in result and "</think>" in result:
                    # Extract content between thinking tags
                    think_start = result.find("<think>")
                    think_end = result.find("</think>", think_start) + len("</think>")
                    # Remove the thinking part
                    result = result[:think_start] + result[think_end:].strip()
                
                # If the result starts with a backtick (markdown code block), remove it
                if result.startswith("```json"):
                    result = result[7:].strip()
                if result.startswith("```"):
                    result = result[3:].strip()
                if result.endswith("```"):
                    result = result[:-3].strip()
                
                # Try to find JSON in the text - look for opening and closing braces
                json_start = result.find('{')
                json_end = result.rfind('}') + 1
                
                if json_start >= 0 and json_end > json_start:
                    # Extract just the JSON part
                    json_str = result[json_start:json_end]
                    requirements = json.loads(json_str)
                else:
                    # If no JSON found, create a fallback structure
                    print("No valid JSON structure found in response")
                    return self._empty_requirements()
                
                # Validate the structure of the requirements
                expected_keys = ["required_skills", "preferred_skills", "required_experience", 
                                "required_education", "responsibilities", "keywords"]
                for key in expected_keys:
                    if key not in requirements:
                        print(f"Warning: Missing '{key}' in job requirements")
                        requirements[key] = []
                    elif not isinstance(requirements[key], list):
                        print(f"Warning: '{key}' is not a list in job requirements")
                        requirements[key] = [str(requirements[key])] if requirements[key] else []
                
                return requirements
            except json.JSONDecodeError as json_err:
                print(f"Error parsing JSON from LLM response: {json_err}")
                print(f"Raw LLM response: {result[:500]}...")  # Print first 500 chars of response
                return self._empty_requirements()
        except Exception as e:
            print(f"Error analyzing job description: {e}")
            # Return empty structure as fallback
            return self._empty_requirements()
    
    def _empty_requirements(self):
        """
        Create an empty requirements structure as fallback.
        
        Returns:
            dict: An empty requirements dictionary.
        """
        return {
            "required_skills": [],
            "preferred_skills": [],
            "required_experience": [],
            "required_education": [],
            "responsibilities": [],
            "keywords": []
        }
    
    def extract_keywords(self, job_description_text):
        """
        Extract just the keywords from a job description.
        
        Args:
            job_description_text (str): The text content of the job description.
            
        Returns:
            list: A list of important keywords from the job description.
        """
        requirements = self.analyze_job_description(job_description_text)
        return requirements.get("keywords", [])


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
    
    # Print requirements
    for category, items in requirements.items():
        print(f"=== {category.replace('_', ' ').title()} ===")
        for item in items:
            print(f"- {item}")
        print()
