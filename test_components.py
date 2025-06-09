"""
Test script for Resume Helper components.

This script tests the core components of the Resume Helper application:
1. Resume Parser
2. Job Description Analyzer
3. Resume-Job Comparison
4. Recommendation Generator

It uses the sample resume and job description provided in the data directory.
"""

import os
import sys
import json

# Add the app directory to the path so we can import our modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import our modules
from app.parser.pdf_parser import ResumeParser
from app.analyzer.job_analyzer import JobAnalyzer
from app.comparison.matcher import ResumeMatcher
from app.recommendation.generator import RecommendationGenerator


def test_resume_parser():
    """Test the resume parser component."""
    print("\n=== Testing Resume Parser ===")
    
    # Initialize parser
    parser = ResumeParser()
    
    # Get sample resume path
    sample_resume_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "sample_resumes")
    sample_resumes = [f for f in os.listdir(sample_resume_dir) if f.endswith(".pdf")]
    
    if not sample_resumes:
        print("No sample resumes found in data/sample_resumes directory.")
        return None
    
    sample_resume_path = os.path.join(sample_resume_dir, sample_resumes[0])
    print(f"Using sample resume: {sample_resumes[0]}")
    
    # Parse resume
    try:
        resume_data = parser.parse_resume(sample_resume_path)
        print(f"Successfully parsed resume.")
        print(f"Extracted {len(resume_data['sections'])} sections:")
        
        for section_name in resume_data['sections'].keys():
            print(f"- {section_name}")
        
        return resume_data
    except Exception as e:
        print(f"Error parsing resume: {str(e)}")
        return None


def test_job_analyzer():
    """Test the job description analyzer component."""
    print("\n=== Testing Job Description Analyzer ===")
    
    # Initialize analyzer
    analyzer = JobAnalyzer()
    
    # Get sample job description path
    sample_job_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "sample_job_descriptions")
    sample_jobs = [f for f in os.listdir(sample_job_dir) if f.endswith(".txt")]
    
    if not sample_jobs:
        print("No sample job descriptions found in data/sample_job_descriptions directory.")
        return None
    
    sample_job_path = os.path.join(sample_job_dir, sample_jobs[0])
    print(f"Using sample job description: {sample_jobs[0]}")
    
    # Read job description
    try:
        with open(sample_job_path, 'r') as f:
            job_description_text = f.read()
        
        # Analyze job description
        job_requirements = analyzer.analyze_job_description(job_description_text)
        print(f"Successfully analyzed job description.")
        
        for category, items in job_requirements.items():
            print(f"\n{category.replace('_', ' ').title()}:")
            for item in items:
                print(f"- {item}")
        
        return job_description_text, job_requirements
    except Exception as e:
        print(f"Error analyzing job description: {str(e)}")
        return None


def test_resume_matcher(resume_data, job_requirements):
    """Test the resume-job comparison component."""
    print("\n=== Testing Resume-Job Comparison ===")
    
    if not resume_data or not job_requirements:
        print("Cannot test matcher without resume data and job requirements.")
        return None
    
    # Initialize matcher
    matcher = ResumeMatcher()
    
    try:
        # Compare resume to job
        comparison_results = matcher.compare_resume_to_job(resume_data, job_requirements)
        print(f"Successfully compared resume to job requirements.")
        print(f"Overall match score: {comparison_results.get('match_score', 0)}%")
        
        print("\nMatches:")
        for match in comparison_results.get("matches", []):
            print(f"- {match.get('item', '')} (Found in {match.get('where_found', '')})")
        
        print("\nGaps:")
        for gap in comparison_results.get("gaps", []):
            print(f"- {gap.get('item', '')} (Suggestion: {gap.get('suggestion', '')})")
        
        print("\nSection Scores:")
        for section, score in comparison_results.get("section_scores", {}).items():
            print(f"- {section.replace('_', ' ').title()}: {score}%")
        
        return comparison_results
    except Exception as e:
        print(f"Error comparing resume to job: {str(e)}")
        return None


def test_recommendation_generator(resume_data, job_description_text, comparison_results):
    """Test the recommendation generator component."""
    print("\n=== Testing Recommendation Generator ===")
    
    if not resume_data or not job_description_text or not comparison_results:
        print("Cannot test recommendation generator without resume data, job description, and comparison results.")
        return None
    
    # Initialize generator
    generator = RecommendationGenerator()
    
    try:
        # Generate recommendations
        recommendations = generator.generate_recommendations(
            resume_data["raw_text"],
            job_description_text,
            comparison_results
        )
        print(f"Successfully generated recommendations.")
        
        print(f"\nSummary: {recommendations.get('summary', 'No summary available.')}")
        
        print("\nRecommendations:")
        for rec in recommendations.get("recommendations", []):
            print(f"[Priority: {rec.get('priority', 0)}] {rec.get('section', '')} ({rec.get('type', '')}): {rec.get('content', '')}")
            print(f"  Reason: {rec.get('reason', '')}")
            print()
        
        if "keyword_suggestions" in recommendations and recommendations["keyword_suggestions"]:
            print("Keyword Suggestions:")
            for keyword in recommendations["keyword_suggestions"]:
                print(f"- {keyword}")
        
        return recommendations
    except Exception as e:
        print(f"Error generating recommendations: {str(e)}")
        return None


def main():
    """Run tests for all components."""
    print("=== Resume Helper Component Tests ===")
    
    # Test resume parser
    resume_data = test_resume_parser()
    
    # Test job analyzer
    job_analyzer_result = test_job_analyzer()
    if job_analyzer_result:
        job_description_text, job_requirements = job_analyzer_result
    else:
        job_description_text, job_requirements = None, None
    
    # Test resume matcher
    comparison_results = test_resume_matcher(resume_data, job_requirements)
    
    # Test recommendation generator
    recommendations = test_recommendation_generator(resume_data, job_description_text, comparison_results)
    
    print("\n=== Test Summary ===")
    print(f"Resume Parser: {'Success' if resume_data else 'Failed'}")
    print(f"Job Analyzer: {'Success' if job_requirements else 'Failed'}")
    print(f"Resume Matcher: {'Success' if comparison_results else 'Failed'}")
    print(f"Recommendation Generator: {'Success' if recommendations else 'Failed'}")


if __name__ == "__main__":
    main()
