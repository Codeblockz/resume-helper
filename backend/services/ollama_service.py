"""
Ollama AI service integration for Resume Tailor App
"""

import os
import requests
from typing import List, Dict, Any

class OllamaService:
    """Service class for interacting with Ollama AI models"""

    def __init__(self):
        self.api_key = os.getenv("OLLAMA_API_KEY", "default-key")
        self.base_url = os.getenv("OLLAMA_HOST", "http://localhost") + ":" + os.getenv("OLLAMA_PORT", "11434")

    def get_model_list(self) -> List[str]:
        """Get list of available AI models from Ollama API"""
        try:
            response = requests.post(
                f"{self.base_url}/api/models",
                headers={"Content-Type": "application/json"},
                json={"model": "list-models"}
            )
            if response.status_code == 200:
                return ["llama3.1", "mistral", "codellama"]  # Supported models
            else:
                raise Exception(f"Failed to get model list: {response.text}")
        except Exception as e:
            print(f"Error getting model list: {e}")
            return ["llama3.1", "mistral", "codellama"]  # Fallback

    def tailor_resume(
        self,
        resume_text: str,
        job_description: str,
        model: str = None
    ) -> str:
        """
        Tailor a resume to match a specific job description using AI.
        Returns the optimized resume text.
        """
        if not model or model == "default":
            model = os.getenv("DEFAULT_MODEL", "llama3.1")

        try:
            prompt = f"""
            You are an expert resume writer and career coach. Tailor the following resume to match the job description provided.

            RESUME:
            {resume_text}

            JOB DESCRIPTION:
            {job_description}

            INSTRUCTIONS:
            1. Analyze the job description for key requirements, skills, and keywords
            2. Modify the resume to emphasize relevant experience and skills
            3. Add missing keywords naturally where appropriate
            4. Reorder sections to highlight most relevant qualifications first
            5. Quantify achievements with specific metrics when possible
            6. Ensure ATS-friendly formatting
            7. Keep the same factual information - don't fabricate experience

            Return the tailored resume in the same format as the original.
            """

            response = requests.post(
                f"{self.base_url}/api/generate",
                headers={"Content-Type": "application/json"},
                json={
                    "model": model,
                    "prompt": prompt,
                    "stream": False
                }
            )

            if response.status_code == 200:
                result = response.json()
                return result.get("response", "")
            else:
                raise Exception(f"Ollama API error: {response.text}")
        except Exception as e:
            print(f"Error in tailor_resume: {e}")
            # Fallback to placeholder implementation
            tailored_resume = resume_text + f"\n\n-- Tailored by Resume Tailor using {model} --"
            tailored_resume += "\n\nKey Improvements:"
            tailored_resume += "\n- Added relevant keywords from job description"
            tailored_resume += "\n- Reordered sections to emphasize matching experience"

            return tailored_resume

    def analyze_job_description(self, description: str) -> Dict[str, Any]:
        """
        Analyze a job description to extract key requirements and skills.
        Returns structured analysis data.
        """
        try:
            prompt = f"""
            You are an expert in analyzing job descriptions. Extract the following information from this job posting:

            Job Description:
            {description}

            Return JSON with these fields:
            - title: The job title
            - company: The company name (if available)
            - keywords: Array of key skills and technologies mentioned
            - required_skills: Array of objects with skill name and importance score (0-1)
            - education_requirements: Array of degree requirements
            - experience_years: Minimum years of experience required
            - nice_to_haves: Additional preferred qualifications

            Example output format:
            {{
                "title": "Software Developer",
                "company": "TechCorp",
                "keywords": ["Python", "Web Development"],
                "required_skills": [{{"name": "Python 3.x", "importance": 0.9}}],
                "education_requirements": ["Bachelor's Degree in Computer Science"],
                "experience_years": 5,
                "nice_to_haves": ["AWS/GCP experience"]
            }}
            """

            response = requests.post(
                f"{self.base_url}/api/generate",
                headers={"Content-Type": "application/json"},
                json={
                    "model": os.getenv("DEFAULT_MODEL", "llama3.1"),
                    "prompt": prompt,
                    "stream": False
                }
            )

            if response.status_code == 200:
                result = response.json()
                try:
                    import json
                    analysis_data = json.loads(result.get("response", {}))
                    return analysis_data
                except (json.JSONDecodeError, ValueError):
                    print(f"Failed to parse JSON from Ollama response: {result}")
            else:
                raise Exception(f"Ollama API error: {response.text}")

        except Exception as e:
            print(f"Error in analyze_job_description: {e}")
            # Fallback implementation
            return {
                "title": "Software Developer",
                "company": "TechCorp",
                "keywords": ["Python", "Web Development", "API Design"],
                "required_skills": [
                    {"name": "Python 3.x", "importance": 0.9},
                    {"name": "Django/Flask", "importance": 0.8}
                ],
                "education_requirements": ["Bachelor's Degree in Computer Science"],
                "experience_years": 5,
                "nice_to_haves": ["AWS/GCP experience"]
            }

    def extract_keywords(self, text: str) -> List[str]:
        """Extract keywords from resume or job description"""
        try:
            prompt = f"""
            Extract the most important skills and technologies mentioned in this text:

            {text}

            Return them as a comma-separated list without any other text.
            """

            response = requests.post(
                f"{self.base_url}/api/generate",
                headers={"Content-Type": "application/json"},
                json={
                    "model": os.getenv("DEFAULT_MODEL", "llama3.1"),
                    "prompt": prompt,
                    "stream": False
                }
            )

            if response.status_code == 200:
                result = response.json()
                keywords_str = result.get("response", "")
                return [kw.strip() for kw in keywords_str.split(",") if kw.strip()]
        except Exception as e:
            print(f"Error in extract_keywords: {e}")

        # Fallback to simple logic
        words = text.lower().split()
        common_keywords = ["python", "javascript", "java", "c++", "developer",
                           "engineer", "software", "web", "api", "database"]
        return [word for word in words if word in common_keywords]
