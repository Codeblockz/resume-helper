"""
Markdown Utilities for Resume Helper

This module provides functions for converting between plain text, HTML,
and markdown formats to support markdown-based resume editing.
"""

import re
from typing import Dict, Any, Optional
from markdown2 import Markdown
import bleach

class MarkdownConverter:
    """
    Utility class for converting between markdown, HTML, and plain text formats
    with proper handling of resume-specific formatting patterns.
    """

    def __init__(self):
        """Initialize the markdown converter."""
        self.markdown_converter = Markdown()

    def text_to_markdown(self, content: str) -> str:
        """
        Convert plain text resume content to markdown format.

        Args:
            content (str): Plain text content of a resume section

        Returns:
            str: Markdown-formatted content
        """
        if not content or not isinstance(content, str):
            return ""

        # Clean input by removing any HTML tags that might exist
        cleaned_content = bleach.clean(content)

        lines = [line.strip() for line in cleaned_content.split('\n') if line.strip()]
        markdown_lines = []
        bullet_point_pattern = re.compile(r'^(-|\*|\•)\s+')

        current_indent_level = 0

        for i, line in enumerate(lines):
            # Check for headers (all caps or specific keywords)
            is_header = False
            header_text = line.upper()
            if line == header_text and len(line) > 2:
                is_header = True

            # Handle section breaks with horizontal lines
            elif line.startswith('===') or line.startswith('---'):
                markdown_lines.append('')
                continue

            # Preserve bullet points and numbering
            elif bullet_point_pattern.match(line):
                bullet_char = line[0]
                markdown_content = f"{bullet_char} {line[2:]}"
                markdown_lines.append(markdown_content)

            # Handle indentation for lists and paragraphs
            else:
                # Detect if this might be a continuation of a list item
                if i > 0 and bullet_point_pattern.match(lines[i-1]):
                    indent_size = len(re.match(r'^\s*', line).group(0))
                    markdown_lines.append(' ' * indent_size + line)
                else:
                    markdown_lines.append(line)

        # Convert to markdown with proper paragraph handling
        final_markdown = '\n\n'.join(markdown_lines)

        return final_markdown

    def markdown_to_html(self, markdown_content: str) -> str:
        """
        Convert markdown content to HTML format for rendering in the editor.

        Args:
            markdown_content (str): Markdown text to convert

        Returns:
            str: HTML representation of the markdown
        """
        if not markdown_content or not isinstance(markdown_content, str):
            return ""

        # Use basic markdown2 conversion
        html_output = self.markdown_converter.convert(markdown_content)

        # Apply additional formatting to match resume styles
        html_output = self._apply_resume_styles(html_output)

        return html_output

    def html_to_markdown(self, html_content: str) -> str:
        """
        Convert HTML content back to markdown format.

        Args:
            html_content (str): HTML content to convert

        Returns:
            str: Markdown representation of the HTML
        """
        if not html_content or not isinstance(html_content, str):
            return ""

        # Remove any script tags and clean HTML
        cleaned_html = bleach.clean(
            html_content,
            tags=['p', 'h1', 'h2', 'h3', 'h4', 'ul', 'ol', 'li',
                  'strong', 'em', 'a', 'div', 'span'],
            attributes={'a': ['href'], 'img': ['src', 'alt']}
        )

        # Basic conversion - markdown2 doesn't support HTML->markdown directly
        # so we'll just return the cleaned HTML as a fallback
        try:
            result = self.markdown_converter.convert(cleaned_html)
            return result
        except Exception as e:
            print(f"Error converting HTML to markdown: {e}")
            return cleaned_html

    def _apply_resume_styles(self, html_content: str) -> str:
        """
        Apply resume-specific CSS classes and styles to HTML content.

        Args:
            html_content (str): Base HTML content

        Returns:
            str: HTML with resume styling applied
        """
        if not html_content:
            return ""

        # Simple styling enhancement - in a real implementation,
        # this would be more sophisticated and tied to the section type
        styled_html = html_content.replace(
            '<p>', '<p class="resume-content">'
        ).replace(
            '</p>', '</p>'
        )

        # Add basic resume classes for better CSS targeting
        if '<ul>' in styled_html:
            styled_html = styled_html.replace(
                '<ul>', '<ul class="resume-list">'
            )
        if '<ol>' in styled_html:
            styled_html = styled_html.replace(
                '<ol>', '<ol class="resume-list">'
            )

        return styled_html

    def convert_resume_section(self, section_name: str, content: str) -> Dict[str, Any]:
        """
        Convert a resume section to markdown format with metadata.

        Args:
            section_name (str): Name of the resume section
            content (str): Content of the resume section

        Returns:
            Dict[str, Any]: Dictionary containing markdown and metadata
        """
        if not content or not isinstance(content, str):
            return {"section": section_name, "markdown": "", "metadata": {}}

        # Convert to markdown
        markdown_content = self.text_to_markdown(content)

        # Create metadata for the section
        metadata = {
            "original_format": "text",
            "css_class": None,
            "section_type": "generic"
        }

        # Infer CSS class based on section name
        lower_name = section_name.lower()
        if 'contact' in lower_name:
            metadata["css_class"] = "resume-contact"
            metadata["section_type"] = "contact"
        elif 'summary' in lower_name or 'objective' in lower_name:
            metadata["css_class"] = "resume-summary"
            metadata["section_type"] = "summary"
        elif 'experience' in lower_name or 'work history' in lower_name:
            metadata["css_class"] = "resume-experience"
            metadata["section_type"] = "experience"
        elif 'education' in lower_name or 'degrees' in lower_name:
            metadata["css_class"] = "resume-education"
            metadata["section_type"] = "education"
        elif 'skills' in lower_name or 'abilities' in lower_name:
            metadata["css_class"] = "resume-skills"
            metadata["section_type"] = "skills"

        return {
            "section": section_name,
            "markdown": markdown_content,
            "metadata": metadata
        }

    def convert_markdown_to_resume_section(self, section_name: str, markdown_content: str) -> Dict[str, Any]:
        """
        Convert markdown content back to resume section format.

        Args:
            section_name (str): Name of the resume section
            markdown_content (str): Markdown content

        Returns:
            Dict[str, Any]: Dictionary containing converted content and metadata
        """
        if not markdown_content or not isinstance(markdown_content, str):
            return {"section": section_name, "content": "", "metadata": {}}

        # Convert markdown to HTML for rendering
        html_content = self.markdown_to_html(markdown_content)

        # For now, we'll store the original markdown and provide HTML for display
        metadata = {
            "original_format": "markdown",
            "css_class": None,
            "section_type": "generic"
        }

        # Infer CSS class based on section name (same as above)
        lower_name = section_name.lower()
        if 'contact' in lower_name:
            metadata["css_class"] = "resume-contact"
            metadata["section_type"] = "contact"
        elif 'summary' in lower_name or 'objective' in lower_name:
            metadata["css_class"] = "resume-summary"
            metadata["section_type"] = "summary"
        elif 'experience' in lower_name or 'work history' in lower_name:
            metadata["css_class"] = "resume-experience"
            metadata["section_type"] = "experience"
        elif 'education' in lower_name or 'degrees' in lower_name:
            metadata["css_class"] = "resume-education"
            metadata["section_type"] = "education"
        elif 'skills' in lower_name or 'abilities' in lower_name:
            metadata["css_class"] = "resume-skills"
            metadata["section_type"] = "skills"

        return {
            "section": section_name,
            "content": html_content,  # HTML for rendering
            "markdown": markdown_content,  # Original markdown preserved
            "metadata": metadata
        }

# Example usage
if __name__ == "__main__":
    converter = MarkdownConverter()

    # Test data - example resume section content
    test_section_name = "Skills"
    test_content = """Python
Django
Flask
SQL
JavaScript"""

    print("=== Converting Text to Markdown ===")
    result = converter.convert_resume_section(test_section_name, test_content)
    print(f"Section: {result['section']}")
    print(f"Markdown:\n{result['markdown']}")
    print(f"Metadata: {result['metadata']}")

    print("\n=== Converting Markdown to HTML ===")
    html_result = converter.markdown_to_html(result['markdown'])
    print(f"HTML:\n{html_result}")

    print("\n=== Converting Back to Resume Section ===")
    back_conversion = converter.convert_markdown_to_resume_section(
        test_section_name, result['markdown']
    )
    print(f"Content (HTML):\n{back_conversion['content']}")
    print(f"Preserved Markdown:\n{back_conversion['markdown']}")
