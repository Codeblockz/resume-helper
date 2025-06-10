"""
Resume-Job Comparison module for Resume Helper.

This module compares resume content against job requirements to identify
matches and gaps, and calculates a match score.
"""

from langchain_community.llms import Ollama
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate


class ResumeMatcher:
    """Matcher for comparing resume content against job requirements."""
    
    def __init__(self, model_name="qwen3:32b"):
        """
        Initialize the ResumeMatcher.
        
        Args:
            model_name (str): Name of the Ollama model to use for comparison.
        """
        self.llm = Ollama(model=model_name)
        
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
            """
        )
        
        self.comparison_chain = LLMChain(llm=self.llm, prompt=self.comparison_prompt)
    
    def compare_resume_to_job(self, resume_data, job_requirements):
        """
        Compare resume content to job requirements.
        
        Args:
            resume_data (dict): Structured resume data with sections.
            job_requirements (dict): Structured job requirements.
            
        Returns:
            dict: Comparison results with matches, gaps, and scores.
        """
        try:
            # Format resume sections for the prompt
            resume_sections_str = self._format_resume_sections(resume_data)
            
            # Format job requirements for the prompt
            job_requirements_str = self._format_job_requirements(job_requirements)
            
            # Run the comparison
            result = self.comparison_chain.run(
                resume_sections=resume_sections_str,
                job_requirements=job_requirements_str
            )
            
            # Parse the JSON result
            import json
            comparison_results = json.loads(result)
            return comparison_results
        except Exception as e:
            print(f"Error comparing resume to job: {e}")
            # Return basic structure as fallback
            return self._basic_comparison_result()
    
    def _format_resume_sections(self, resume_data):
        """
        Format resume sections for the comparison prompt.
        
        Args:
            resume_data (dict): Structured resume data.
            
        Returns:
            str: Formatted string representation of resume sections.
        """
        sections = resume_data.get("sections", {})
        formatted = ""
        
        for section_name, content in sections.items():
            formatted += f"=== {section_name} ===\n{content}\n\n"
        
        return formatted
    
    def _format_job_requirements(self, job_requirements):
        """
        Format job requirements for the comparison prompt.
        
        Args:
            job_requirements (dict): Structured job requirements.
            
        Returns:
            str: Formatted string representation of job requirements.
        """
        formatted = ""
        
        for category, items in job_requirements.items():
            if items:  # Only include non-empty categories
                formatted += f"=== {category.replace('_', ' ').title()} ===\n"
                for item in items:
                    formatted += f"- {item}\n"
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
