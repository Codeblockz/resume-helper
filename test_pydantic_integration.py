"""
Test script for Pydantic integration with Resume Helper components.

This script tests the new structured data models and enhanced components
to ensure proper functionality before full migration.
"""

import sys
from pathlib import Path

# Add project root to path
sys.path.append(str(Path(__file__).parent))

from app.analyzer.job_analyzer import JobAnalyzer
from app.models.responses import JobRequirements

def test_job_analyzer():
    """Test the enhanced JobAnalyzer with Pydantic models."""
    print("🧪 Testing JobAnalyzer with Pydantic integration...")
    
    # Initialize analyzer
    analyzer = JobAnalyzer()
    
    # Sample job description
    job_description = """
    Software Engineer - Full Stack
    
    Requirements:
    - Bachelor's degree in Computer Science or related field
    - 3+ years of experience in Python development
    - Experience with React and JavaScript
    - Knowledge of SQL databases
    - Familiarity with Git version control
    
    Preferred Qualifications:
    - Experience with Django or Flask frameworks
    - Knowledge of cloud platforms (AWS, Azure)
    - Experience with Docker containerization
    - Understanding of CI/CD pipelines
    
    Responsibilities:
    - Develop and maintain web applications
    - Collaborate with cross-functional teams
    - Write clean, maintainable code
    - Participate in code reviews
    - Debug and troubleshoot issues
    """
    
    try:
        # Test structured analysis
        print("\n📋 Analyzing job description...")
        requirements = analyzer.analyze_job_description(job_description)
        
        # Verify it's a Pydantic model
        assert isinstance(requirements, JobRequirements), "Result should be JobRequirements model"
        print("✅ Returned JobRequirements Pydantic model")
        
        # Test model properties
        print(f"\n🔍 Analysis Results:")
        print(f"   Required Skills: {len(requirements.required_skills)} items")
        print(f"   Preferred Skills: {len(requirements.preferred_skills)} items")
        print(f"   Experience: {len(requirements.required_experience)} items")
        print(f"   Education: {len(requirements.required_education)} items")
        print(f"   Responsibilities: {len(requirements.responsibilities)} items")
        print(f"   Keywords: {len(requirements.keywords)} items")
        
        # Display some results
        if requirements.required_skills:
            print(f"\n📌 Sample Required Skills:")
            for skill in requirements.required_skills[:3]:  # Show first 3
                print(f"   • {skill}")
        
        if requirements.keywords:
            print(f"\n🏷️  Sample Keywords:")
            for keyword in requirements.keywords[:5]:  # Show first 5
                print(f"   • {keyword}")
        
        # Test serialization
        print(f"\n💾 Testing model serialization...")
        data_dict = requirements.model_dump()
        assert isinstance(data_dict, dict), "Should serialize to dictionary"
        print("✅ Model serializes correctly")
        
        # Test legacy compatibility
        print(f"\n🔄 Testing legacy compatibility...")
        legacy_data = analyzer.analyze_job_description_legacy(job_description)
        assert isinstance(legacy_data, dict), "Legacy method should return dict"
        print("✅ Legacy compatibility maintained")
        
        print(f"\n🎉 All JobAnalyzer tests passed!")
        return True
        
    except Exception as e:
        print(f"❌ JobAnalyzer test failed: {e}")
        return False

def test_pydantic_models():
    """Test Pydantic model validation and functionality."""
    print("\n🧪 Testing Pydantic model validation...")
    
    try:
        # Test JobRequirements model creation
        requirements = JobRequirements(
            required_skills=["Python", "React"],
            preferred_skills=["Docker", "AWS"],
            required_experience=["3+ years software development"],
            required_education=["Bachelor's degree in Computer Science"],
            responsibilities=["Develop applications", "Code reviews"],
            keywords=["Python", "React", "software", "development"]
        )
        
        print("✅ JobRequirements model created successfully")
        
        # Test model properties
        assert len(requirements.required_skills) == 2
        assert "Python" in requirements.required_skills
        print("✅ Model properties accessible")
        
        # Test empty model (defaults)
        empty_requirements = JobRequirements()
        assert empty_requirements.required_skills == []
        assert empty_requirements.keywords == []
        print("✅ Empty model with defaults works")
        
        # Test serialization
        data = requirements.model_dump()
        assert "required_skills" in data
        assert data["required_skills"] == ["Python", "React"]
        print("✅ Model serialization works")
        
        print(f"\n🎉 All Pydantic model tests passed!")
        return True
        
    except Exception as e:
        print(f"❌ Pydantic model test failed: {e}")
        return False

def main():
    """Run all integration tests."""
    print("=" * 60)
    print("🚀 Resume Helper - Pydantic Integration Tests")
    print("=" * 60)
    
    # Run tests
    pydantic_success = test_pydantic_models()
    analyzer_success = test_job_analyzer()
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 Test Summary:")
    print(f"   Pydantic Models: {'✅ PASS' if pydantic_success else '❌ FAIL'}")
    print(f"   JobAnalyzer: {'✅ PASS' if analyzer_success else '❌ FAIL'}")
    
    if pydantic_success and analyzer_success:
        print("\n🎉 All tests passed! Pydantic integration is working correctly.")
        print("\n💡 Next steps:")
        print("   1. Test the Streamlit app: streamlit run streamlit_app.py")
        print("   2. Update remaining components (parser, matcher, generator)")
        print("   3. Add resume processing functionality")
    else:
        print("\n⚠️  Some tests failed. Check the output above for details.")
    
    print("=" * 60)

if __name__ == "__main__":
    main()
