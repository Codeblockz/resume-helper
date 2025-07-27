"""
Ollama AI Integration Service for Resume Tailor App
"""

import requests
from backend.core.config import settings

class OllamaService:
    """Service class for interacting with Ollama AI models"""

    def __init__(self, base_url=None):
        """Initialize the Ollama service"""
        self.base_url = base_url or f"{settings.OLLAMA_HOST}:{settings.OLLAMA_PORT}"

    def get_model_list(self):
        """Get available Ollama models"""
        try:
            response = requests.get(f"{self.base_url}/api/models")
            response.raise_for_status()
            return response.json().get("models", [])
        except requests.RequestException as e:
            raise ConnectionError(f"Failed to connect to Ollama: {e}")

    def generate_text(self, model_name, prompt):
        """Generate text using an Ollama model"""
        payload = {
            "model": model_name,
            "prompt": prompt,
            "stream": False
        }

        try:
            response = requests.post(f"{self.base_url}/api/generate", json=payload)
            response.raise_for_status()
            return response.json().get("response", "")
        except requests.RequestException as e:
            raise RuntimeError(f"Ollama generation failed: {e}")

    def tailor_resume(self, resume_text, job_description, model=None):
        """
        Tailor a resume for a specific job using Ollama AI
        Following the pattern from projectPrompt.md
        """
        model = model or settings.DEFAULT_MODEL

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

        return self.generate_text(model, prompt)

# Example usage
if __name__ == "__main__":
    service = OllamaService()
    try:
        print("Available models:", service.get_model_list())

        # Test with sample data
        sample_resume = "John Doe\nSoftware Engineer"
        sample_job = "Python Developer position"

        tailored = service.tailor_resume(sample_resume, sample_job)
        print("\nTailored Resume:")
        print(tailored)

    except Exception as e:
        print(f"Error: {e}")
