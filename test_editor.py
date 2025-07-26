"""
Test script for Resume Editor functionality.

This script tests the core editing capabilities of the resume editor.
"""

import sys
import os

# Add the app directory to the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.editor import EditableResume, EditableResumeSection, ResumeEditor
from app.models.responses import ResumeData, ResumeSection

def test_basic_editing():
    """Test basic editing functionality."""
    # Create sample resume data
    sample_resume = {
        "raw_text": "John Doe\nSoftware Engineer...",
        "sections": {
            "contact_information": "John Doe\njohn.doe@example.com",
            "skills": "Python, Django",
            "experience": "Software Engineer at ABC Corp"
        }
    }

    # Convert to ResumeData model
    resume_data = ResumeData(
        raw_text=sample_resume["raw_text"],
        sections=ResumeSection(**{k: v for k, v in sample_resume["sections"].items()})
    )

    # Create editable resume
    editor = ResumeEditor()
    editable_resume = editor.create_from_resume_data(resume_data)

    # Test adding a new section
    editable_resume.add_section("Certifications", "AWS Certified Solutions Architect\nGoogle Cloud Professional Data Engineer")

    # Test applying recommendations
    recommendations = [
        {
            "section": "Skills",
            "type": "add",
            "content": "Flask",
            "reason": "Web development framework"
        },
        {
            "section": "Experience",
            "type": "modify",
            "content": "Led team of 5 developers",
            "reason": "Highlight leadership experience"
        }
    ]

    editor.apply_recommendations(editable_resume, recommendations)

    # Test export functionality
    final_text = editor.export_to_text(editable_resume)

    # Verify sections were added/updated
    assert "Certifications" in editable_resume.sections
    assert "Flask" in editable_resume.sections["Skills"].content
    assert "Led team of 5 developers" in editable_resume.sections["Experience"].content

    # Verify export format
    assert "=== Contact Information ===" in final_text
    assert "=== Certifications ===" in final_text

def test_edit_history():
    """Test edit history tracking."""
    # Create a simple editable section
    section = EditableResumeSection(
        content="Python, Django",
        original_content="Python, Django"
    )

    # Apply changes
    section.apply_change("Python, Django, Flask")
    section.apply_change("Python, Django, Flask, SQL")

    # Verify edit history is tracked
    assert len(section.edit_history) == 2

    # Test reverting
    if len(section.edit_history) >= 2:
        result = section.revert_to(0)
        assert "Python, Django, Flask" in section.content

if __name__ == "__main__":
    test_basic_editing()
    test_edit_history()
