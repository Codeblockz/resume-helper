#!/usr/bin/env python3
"""
Test script for markdown conversion functionality in Resume Helper.

This script tests the core markdown conversion capabilities that enable
editable resume support.
"""

import sys
import os

# Add the app directory to the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.editor.markdown_utils import MarkdownConverter
from app.editor.editor import EditableResume, EditableResumeSection

def test_markdown_conversion():
    """Test markdown conversion functionality."""
    print("=== Testing Markdown Conversion ===")

    # Test data - example resume section content
    test_sections = {
        "Skills": """Python
Django
Flask
SQL
JavaScript""",
        "Experience": """Senior Software Engineer
Acme Corporation • January 2022 - Present

- Developed and maintained microservices architecture
- Implemented CI/CD pipelines resulting in 30% reduction in deployment time
- Led team of 5 developers in agile environment""",
        "Education": """Bachelor of Science in Computer Science
University of Technology, San Francisco
Graduated: May 2018

Relevant Coursework:
- Data Structures and Algorithms
- Distributed Systems
- Machine Learning Fundamentals"""
    }

    converter = MarkdownConverter()

    # Test each section
    for section_name, content in test_sections.items():
        print(f"\n--- Testing {section_name} ---")

        # Convert to markdown
        markdown_content = converter.convert_resume_section(section_name, content)
        print(f"Markdown Output:\n{markdown_content['markdown']}")

        # Test round-trip conversion (markdown -> HTML -> back to markdown)
        html_output = converter.markdown_to_html(markdown_content['markdown'])
        print(f"\nHTML Conversion:\n{html_output}")

        # Convert back
        resume_section = converter.convert_markdown_to_resume_section(
            section_name, markdown_content['markdown']
        )
        print(f"\nRound-trip Content:\n{resume_section['content']}")

def test_editable_resume_markdown():
    """Test markdown export functionality in EditableResume."""
    print("\n=== Testing Editable Resume Markdown Export ===")

    # For testing purposes, let's just create the sections directly
    # without relying on the full EditableResume constructor

    from app.editor.editor import EditableResumeSection

    skills_section = EditableResumeSection(
        content="Python\nDjango\nFlask",
        original_content="Python\nDjango\nFlask"
    )

    experience_section = EditableResumeSection(
        content="""
Senior Developer at Acme Corp - Jan 2022-present
- Led development team""",
        original_content="""
Senior Developer at Acme Corp - Jan 2022-present
- Led development team"""
    )

    # Create a simple dictionary to test section export functionality
    print("Testing individual section markdown export...")

    # Test skills section markdown export
    skills_markdown = skills_section.to_markdown()
    if skills_markdown:
        print(f"Skills Section Markdown:\n{skills_markdown}")
    else:
        print("Error: Skills markdown export failed")

    # Test experience section markdown export
    exp_markdown = experience_section.to_markdown()
    if exp_markdown:
        print(f"\nExperience Section Markdown:\n{exp_markdown}")
    else:
        print("\nError: Experience markdown export failed")

def test_markdown_import():
    """Test markdown import functionality."""
    print("\n=== Testing Markdown Import ===")

    # Create markdown content for testing
    markdown_content = """# Experience

**Senior Software Engineer**
Acme Corporation • January 2022 - Present

- Developed and maintained microservices architecture
- Implemented CI/CD pipelines resulting in 30% reduction in deployment time
"""

    converter = MarkdownConverter()
    section_data = EditableResumeSection(
        content="",
        original_content=""
    )

    # Import markdown content
    print("Importing markdown content...")
    try:
        section_data.from_markdown(markdown_content)
        print(f"Updated Content:\n{section_data.content}")
        print("✅ Markdown import successful!")
    except Exception as e:
        print(f"❌ Error during import: {str(e)}")

if __name__ == "__main__":
    try:
        test_markdown_conversion()
        test_editable_resume_markdown()
        test_markdown_import()
        print("\n🎉 All tests completed!")
    except Exception as e:
        print(f"\n❌ Test failed with error: {str(e)}")
        sys.exit(1)
