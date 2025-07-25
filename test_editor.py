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
    print("=== Testing Basic Editing ===")

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

    print("Original sections:")
    for name, section in editable_resume.sections.items():
        print(f"  {name}: {section.content}")

    # Test adding a new section
    editable_resume.add_section("Certifications", "AWS Certified Solutions Architect\nGoogle Cloud Professional Data Engineer")
    print("\nAfter adding Certifications:")

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

    print("\nAfter applying recommendations:")
    for name, section in editable_resume.sections.items():
        print(f"  {name}:")
        print(f"    Content: {section.content}")
        if section.edit_history:
            print(f"    Edit history ({len(section.edit_history)} entries):")
            for i, change in enumerate(section.edit_history[:1]):  # Show just first change
                print(f"      {i+1}. {change}")

    # Test export functionality
    final_text = editor.export_to_text(editable_resume)
    print("\n=== Final Exported Resume ===")
    print(final_text)

    return True


def test_edit_history():
    """Test edit history tracking."""
    print("\n=== Testing Edit History ===")

    # Create a simple editable section
    section = EditableResumeSection(
        content="Python, Django",
        original_content="Python, Django"
    )

    # Apply changes
    section.apply_change("Python, Django, Flask")
    section.apply_change("Python, Django, Flask, SQL")

    print("Original content:", section.original_content)
    print("Current content:", section.content)
    print(f"Edit history ({len(section.edit_history)} entries):")
    for i, change in enumerate(section.edit_history):
        print(f"  {i+1}. {change}")

    # Test reverting
    if len(section.edit_history) >= 2:
        result = section.revert_to(0)
        print(f"\nReverted to version 0: {result}")
        print("Current content after revert:", section.content)

    return True


if __name__ == "__main__":
    try:
        test_basic_editing()
        test_edit_history()
        print("\n✅ All tests completed successfully!")
    except Exception as e:
        print(f"\n❌ Test failed: {str(e)}")
        import traceback
        traceback.print_exc()
