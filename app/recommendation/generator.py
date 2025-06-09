"""
Recommendation Generator module for Resume Helper.

This module creates tailoring suggestions for resumes based on comparison results.
It generates specific, actionable recommendations to improve the resume for a job.
"""

from langchain.llms import Ollama
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate


class RecommendationGenerator:
    """Generator for creating resume tailoring recommendations."""
    
    def __init__(self, model_name="llama3"):
        """
        Initialize the RecommendationGenerator.
        
        Args:
            model_name (str): Name of the Ollama model to use for generating recommendations.
        """
        self.llm = Ollama(model=model_name)
        
        # Create prompt template for generating recommendations
        self.recommendation_prompt = PromptTemplate(
            input_variables=["resume_text", "job_description", "comparison_results"],
            template="""
            Generate specific, actionable recommendations for tailoring this resume to better match the job description.
            
            Resume:
            {resume_text}
            
            Job Description:
            {job_description}
            
            Comparison Results:
            {comparison_results}
            
            For each gap or missing requirement, provide a specific recommendation on how to address it.
            Also suggest improvements to highlight existing matches more effectively.
            
            Return the recommendations in JSON format as follows:
            {{
                "summary": "Brief overall assessment of the resume match and key areas to improve",
                "recommendations": [
                    {{
                        "section": "Skills",
                        "type": "add",
                        "content": "Add Docker to your skills section",
                        "reason": "Docker is a required skill that is missing from your resume",
                        "priority": 9
                    }},
                    {{
                        "section": "Experience",
                        "type": "modify",
                        "content": "Highlight your experience with database design at ABC Corp",
                        "reason": "Database design is a key responsibility in the job description",
                        "priority": 7
                    }},
                    ...
                ],
                "keyword_suggestions": [
                    "cloud computing",
                    "agile development",
                    ...
                ]
            }}
            
            The priority should be a number from 1-10, with 10 being the highest priority.
            Focus on specific, actionable changes rather than generic advice.
            """
        )
        
        self.recommendation_chain = LLMChain(llm=self.llm, prompt=self.recommendation_prompt)
    
    def generate_recommendations(self, resume_text, job_description, comparison_results):
        """
        Generate tailoring recommendations based on comparison results.
        
        Args:
            resume_text (str): The full text of the resume.
            job_description (str): The text of the job description.
            comparison_results (dict): Results from the resume-job comparison.
            
        Returns:
            dict: A dictionary of tailoring recommendations.
        """
        try:
            # Format comparison results for the prompt
            comparison_results_str = self._format_comparison_results(comparison_results)
            
            # Run the recommendation generation
            result = self.recommendation_chain.run(
                resume_text=resume_text,
                job_description=job_description,
                comparison_results=comparison_results_str
            )
            
            # Parse the JSON result
            import json
            recommendations = json.loads(result)
            return recommendations
        except Exception as e:
            print(f"Error generating recommendations: {e}")
            # Return basic structure as fallback
            return self._basic_recommendations()
    
    def _format_comparison_results(self, comparison_results):
        """
        Format comparison results for the recommendation prompt.
        
        Args:
            comparison_results (dict): Results from the resume-job comparison.
            
        Returns:
            str: Formatted string representation of comparison results.
        """
        formatted = f"Overall Match Score: {comparison_results.get('match_score', 0)}%\n\n"
        
        # Add matches
        formatted += "=== Matches ===\n"
        for match in comparison_results.get("matches", []):
            formatted += f"- {match.get('item', '')} (Found in {match.get('where_found', '')})\n"
        formatted += "\n"
        
        # Add gaps
        formatted += "=== Gaps ===\n"
        for gap in comparison_results.get("gaps", []):
            formatted += f"- {gap.get('item', '')} (Suggestion: {gap.get('suggestion', '')})\n"
        formatted += "\n"
        
        # Add section scores
        formatted += "=== Section Scores ===\n"
        for section, score in comparison_results.get("section_scores", {}).items():
            formatted += f"- {section.replace('_', ' ').title()}: {score}%\n"
        
        return formatted
    
    def _basic_recommendations(self):
        """
        Create a basic recommendations structure as fallback.
        
        Returns:
            dict: A basic recommendations dictionary.
        """
        return {
            "summary": "Unable to generate detailed recommendations. Consider reviewing the job description manually and highlighting relevant skills and experience in your resume.",
            "recommendations": [],
            "keyword_suggestions": []
        }
    
    def prioritize_recommendations(self, recommendations):
        """
        Sort recommendations by priority.
        
        Args:
            recommendations (dict): The recommendations dictionary.
            
        Returns:
            dict: The recommendations with sorted recommendations list.
        """
        if "recommendations" in recommendations:
            recommendations["recommendations"] = sorted(
                recommendations["recommendations"],
                key=lambda x: x.get("priority", 0),
                reverse=True
            )
        return recommendations


# Example usage
if __name__ == "__main__":
    generator = RecommendationGenerator()
    
    # Example resume text
    resume_text = """
    John Doe
    john.doe@example.com
    (123) 456-7890
    
    Summary:
    Experienced software engineer with 5 years of Python development.
    
    Skills:
    Python, Django, Flask, SQL, JavaScript, React
    
    Experience:
    Software Engineer at ABC Corp (2018-Present)
    - Developed web applications using Django
    - Designed database schemas
    
    Education:
    Bachelor of Science in Computer Science, XYZ University (2014-2018)
    """
    
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
    
    # Example comparison results
    comparison_results = {
        "matches": [
            {"category": "required_skills", "item": "Python", "where_found": "Skills section"},
            {"category": "required_skills", "item": "Django", "where_found": "Skills section"},
            {"category": "required_skills", "item": "SQL", "where_found": "Skills section"},
            {"category": "required_education", "item": "Bachelor's degree", "where_found": "Education section"}
        ],
        "gaps": [
            {"category": "required_skills", "item": "Data structures and algorithms", "suggestion": "Add to Skills section"},
            {"category": "preferred_skills", "item": "Docker", "suggestion": "Add containerization experience"},
            {"category": "preferred_skills", "item": "AWS", "suggestion": "Add cloud platform experience"}
        ],
        "match_score": 75,
        "section_scores": {
            "required_skills": 80,
            "preferred_skills": 30,
            "required_experience": 90,
            "required_education": 100,
            "keywords": 70
        }
    }
    
    # Generate recommendations
    recommendations = generator.generate_recommendations(resume_text, job_description, comparison_results)
    
    # Print recommendations
    print(f"Summary: {recommendations['summary']}\n")
    
    print("=== Recommendations ===")
    for rec in recommendations.get("recommendations", []):
        print(f"[Priority: {rec['priority']}] {rec['section']} ({rec['type']}): {rec['content']}")
        print(f"  Reason: {rec['reason']}")
        print()
    
    print("=== Keyword Suggestions ===")
    for keyword in recommendations.get("keyword_suggestions", []):
        print(f"- {keyword}")
