"""
Resume-Job Comparison module for Resume Helper.

This module compares resume content against job requirements to identify
matches and gaps, and calculates a match score.
"""

from langchain_ollama import OllamaLLM
from langchain.prompts import PromptTemplate


class ResumeMatcher:
    """Matcher for comparing resume content against job requirements."""
    
    def __init__(self, model_name="qwen3:32b"):
        """
        Initialize the ResumeMatcher.
        
        Args:
            model_name (str): Name of the Ollama model to use for comparison.
        """
        self.llm = OllamaLLM(model=model_name)
        
        # Create prompt template for resume-job comparison
        self.comparison_prompt = PromptTemplate(
            input_variables=["resume_sections", "job_requirements"],
            template="""
            Compare the following resume sections against the job requirements and identify matches and gaps.
            
            Resume Sections:
            {resume_sections}
            
            Job Requirements:
            {job_requirements}
            
            For each category in the job requirements, identify:
            1. Which requirements are matched in the resume
            2. Which requirements are missing or not clearly demonstrated
            3. Suggestions for how to address the gaps
            
            Return the analysis in JSON format as follows:
            {{
                "matches": [
                    {{"category": "required_skills", "item": "Python", "where_found": "Skills section"}},
                    ...
                ],
                "gaps": [
                    {{"category": "required_skills", "item": "Docker", "suggestion": "Add Docker experience to Skills section"}},
                    ...
                ],
                "match_score": 85,
                "section_scores": {{
                    "required_skills": 80,
                    "preferred_skills": 60,
                    "required_experience": 90,
                    "required_education": 100,
                    "keywords": 75
                }}
            }}
            
            The match_score should be a percentage (0-100) representing how well the resume matches the job requirements overall.
            The section_scores should be percentages for each category.
            IMPORTANT: Return ONLY the JSON object, with no additional text, explanations, or thinking process.
            """
        )
    
    def compare_resume_to_job(self, resume_data, job_requirements):
        """
        Compare resume content to job requirements.
        
        Args:
            resume_data (dict or ResumeData): Structured resume data with sections.
            job_requirements (dict or JobRequirements): Structured job requirements.
            
        Returns:
            dict: Comparison results with matches, gaps, and scores.
        """
        # Validate inputs - accept both dict and Pydantic models
        if not resume_data:
            print("Warning: No resume data provided")
            return self._basic_comparison_result()
            
        # Check if it's a Pydantic model or dict
        if not (isinstance(resume_data, dict) or hasattr(resume_data, 'sections')):
            print("Warning: Invalid resume data format")
            return self._basic_comparison_result()
            
        if not job_requirements:
            print("Warning: No job requirements provided")
            return self._basic_comparison_result()
            
        # Check if it's a Pydantic model or dict
        if not (isinstance(job_requirements, dict) or hasattr(job_requirements, 'model_dump')):
            print("Warning: Invalid job requirements format")
            return self._basic_comparison_result()
            
        try:
            # Format resume sections for the prompt
            resume_sections_str = self._format_resume_sections(resume_data)
            
            # Format job requirements for the prompt
            job_requirements_str = self._format_job_requirements(job_requirements)
            
            # Use the prompt and LLM directly instead of LLMChain
            chain = self.comparison_prompt | self.llm
            result = chain.invoke({
                "resume_sections": resume_sections_str,
                "job_requirements": job_requirements_str
            })
            
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
                    comparison_results = json.loads(json_str)
                else:
                    # If no JSON found, create a fallback structure
                    print("No valid JSON structure found in response")
                    return self._basic_comparison_result()
                
                # Validate the structure of the comparison results
                if "matches" not in comparison_results:
                    print("Warning: Missing 'matches' in comparison results")
                    comparison_results["matches"] = []
                
                if "gaps" not in comparison_results:
                    print("Warning: Missing 'gaps' in comparison results")
                    comparison_results["gaps"] = []
                
                if "match_score" not in comparison_results:
                    print("Warning: Missing 'match_score' in comparison results")
                    comparison_results["match_score"] = 0
                
                if "section_scores" not in comparison_results:
                    print("Warning: Missing 'section_scores' in comparison results")
                    comparison_results["section_scores"] = {
                        "required_skills": 0,
                        "preferred_skills": 0,
                        "required_experience": 0,
                        "required_education": 0,
                        "keywords": 0
                    }
                
                return comparison_results
            except json.JSONDecodeError as json_err:
                print(f"Error parsing JSON from LLM response: {json_err}")
                print(f"Raw LLM response: {result[:500]}...")  # Print first 500 chars of response
                return self._basic_comparison_result()
        except Exception as e:
            print(f"Error comparing resume to job: {e}")
            # Return basic structure as fallback
            return self._basic_comparison_result()
    
    def _format_resume_sections(self, resume_data):
        """
        Format resume sections for the comparison prompt.
        
        Args:
            resume_data (dict or ResumeData): Structured resume data.
            
        Returns:
            str: Formatted string representation of resume sections.
        """
        # Handle both dictionary and Pydantic model formats
        if hasattr(resume_data, 'sections'):
            # It's a Pydantic ResumeData model
            if hasattr(resume_data.sections, 'model_dump'):
                sections = resume_data.sections.model_dump()
            else:
                # Fallback - convert to dict manually
                sections = {
                    field: getattr(resume_data.sections, field) 
                    for field in resume_data.sections.__fields__
                    if getattr(resume_data.sections, field) is not None
                }
        else:
            # It's a dictionary
            sections = resume_data.get("sections", {})
        
        formatted = ""
        for section_name, content in sections.items():
            if content:  # Only include non-empty sections
                formatted += f"=== {section_name} ===\n{content}\n\n"
        
        return formatted
    
    def _format_job_requirements(self, job_requirements):
        """
        Format job requirements for the comparison prompt.
        
        Args:
            job_requirements (dict or JobRequirements): Structured job requirements.
            
        Returns:
            str: Formatted string representation of job requirements.
        """
        # Handle both dictionary and Pydantic model formats
        if hasattr(job_requirements, 'model_dump'):
            # It's a Pydantic JobRequirements model
            requirements_dict = job_requirements.model_dump()
        else:
            # It's a dictionary
            requirements_dict = job_requirements
        
        formatted = ""
        for category, items in requirements_dict.items():
            if items:  # Only include non-empty categories
                formatted += f"=== {category.replace('_', ' ').title()} ===\n"
                if isinstance(items, list):
                    for item in items:
                        formatted += f"- {item}\n"
                else:
                    formatted += f"- {items}\n"
                formatted += "\n"
        
        return formatted
    
    def _basic_comparison_result(self):
        """
        Create a basic comparison result structure as fallback.
        
        Returns:
            dict: A basic comparison result dictionary.
        """
        return {
            "matches": [],
            "gaps": [],
            "match_score": 0,
            "section_scores": {
                "required_skills": 0,
                "preferred_skills": 0,
                "required_experience": 0,
                "required_education": 0,
                "keywords": 0
            }
        }
    
    def calculate_keyword_match(self, resume_text, keywords):
        """
        Calculate a simple keyword match score.
        
        Args:
            resume_text (str): The full text of the resume.
            keywords (list): List of keywords from the job description.
            
        Returns:
            dict: A dictionary with matched keywords and score.
        """
        resume_text = resume_text.lower()
        matched_keywords = []
        
        for keyword in keywords:
            if keyword.lower() in resume_text:
                matched_keywords.append(keyword)
        
        match_percentage = (len(matched_keywords) / len(keywords) * 100) if keywords else 0
        
        return {
            "matched_keywords": matched_keywords,
            "missing_keywords": [k for k in keywords if k.lower() not in resume_text],
            "keyword_match_score": round(match_percentage, 1)
        }


# Example usage
if __name__ == "__main__":
    matcher = ResumeMatcher()
    
    # Example resume data
    resume_data = {
        "sections": {
            "Contact Information": "John Doe\njohn.doe@example.com\n(123) 456-7890",
            "Summary": "Experienced software engineer with 5 years of Python development.",
            "Skills": "Python, Django, Flask, SQL, JavaScript, React",
            "Experience": "Software Engineer at ABC Corp (2018-Present)\n- Developed web applications using Django\n- Designed database schemas",
            "Education": "Bachelor of Science in Computer Science, XYZ University (2014-2018)"
        }
    }
    
    # Example job requirements
    job_requirements = {
        "required_skills": ["Python", "Django", "SQL", "Git"],
        "preferred_skills": ["React", "Docker", "AWS"],
        "required_experience": ["3+ years software development", "Web application development"],
        "required_education": ["Bachelor's degree in Computer Science"],
        "responsibilities": ["Develop web applications", "Database design"],
        "keywords": ["Python", "Django", "SQL", "web development", "database"]
    }
    
    # Compare resume to job
    comparison_results = matcher.compare_resume_to_job(resume_data, job_requirements)
    
    # Print results
    print(f"Overall Match Score: {comparison_results['match_score']}%\n")
    
    print("=== Matches ===")
    for match in comparison_results.get("matches", []):
        print(f"- {match['item']} (Found in {match['where_found']})")
    print()
    
    print("=== Gaps ===")
    for gap in comparison_results.get("gaps", []):
        print(f"- {gap['item']} (Suggestion: {gap['suggestion']})")
    print()
    
    print("=== Section Scores ===")
    for section, score in comparison_results.get("section_scores", {}).items():
        print(f"- {section.replace('_', ' ').title()}: {score}%")
