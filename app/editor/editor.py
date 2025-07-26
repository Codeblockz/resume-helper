"""
Resume Editor module for Resume Helper.

This module provides functionality for editing and customizing resumes
based on analysis results. It includes Pydantic models for editable resume data,
core logic for managing resume edits, and CSS styling support.
"""

from pydantic import BaseModel, Field
from typing import Optional, Dict, List
from datetime import datetime

from ..models.responses import ResumeData
from .styles import RESUME_CSS_STYLES, CSS_TO_PDF_STYLE_MAP, DEFAULT_PDF_STYLE
from .markdown_utils import MarkdownConverter


class ResumeEditor:
    """Core class for managing resume editing operations."""

    def __init__(self):
        """Initialize the ResumeEditor."""
        pass

    @staticmethod
    def create_from_resume_data(resume_data: ResumeData) -> 'EditableResume':
        """
        Create an EditableResume from parsed resume data.

        Args:
            resume_data (ResumeData): The structured resume data to edit.

        Returns:
            EditableResume: An editable version of the resume.
        """
        # Import here to avoid circular import
        from .editor import EditableResume

        editable_resume = EditableResume(
            raw_text=resume_data.raw_text,
            original_data=resume_data
        )

        # Convert sections from ResumeSection to individual editable sections
        if hasattr(resume_data.sections, 'model_dump'):
            sections_dict = resume_data.sections.model_dump()
        else:
            sections_dict = {
                field: getattr(resume_data.sections, field)
                for field in resume_data.sections.__fields__
                if getattr(resume_data.sections, field) is not None
            }

        # Try to extract style information from the original data
        section_styles = {}
        if hasattr(resume_data, 'sections') and hasattr(resume_data.sections, 'styles'):
            styles_obj = resume_data.sections.styles
            if isinstance(styles_obj, dict):
                for section_title, class_name in styles_obj.items():
                    # Map section titles to field names (e.g., "Contact Information" -> contact_information)
                    field_name = None
                    lower_title = section_title.lower()

                    if 'contact' in lower_title or 'name' in lower_title:
                        field_name = 'contact_information'
                    elif 'summary' in lower_title or 'objective' in lower_title:
                        field_name = 'summary'
                    elif 'education' in lower_title or 'degrees' in lower_title:
                        field_name = 'education'
                    elif 'experience' in lower_title or 'work history' in lower_title:
                        field_name = 'experience'
                    elif 'skills' in lower_title or 'abilities' in lower_title:
                        field_name = 'skills'
                    elif 'projects' in lower_title:
                        field_name = 'projects'
                    elif 'certifications' in lower_title or 'licenses' in lower_title:
                        field_name = 'certifications'

                    if field_name:
                        section_styles[field_name] = class_name

        # Add each section to the editable resume with appropriate CSS classes
        for section_name, content in sections_dict.items():
            display_name = section_name.replace("_", " ").title()
            if display_name == "Contact Information":
                display_name = "Contact Information"
            elif display_name == "Summary":
                display_name = "Summary"
            elif display_name == "Skills":
                display_name = "Skills"
            elif display_name == "Experience":
                display_name = "Experience"
            elif display_name == "Education":
                display_name = "Education"

            if content:
                # Get CSS class for this section (from original parsing)
                css_class = section_styles.get(section_name)

                # If no CSS class from styles, try to infer it from the section name
                if not css_class:
                    lower_section = display_name.lower()
                    if 'contact' in lower_section or 'name' in lower_section:
                        css_class = "resume-contact"
                    elif 'summary' in lower_section or 'objective' in lower_section:
                        css_class = "resume-summary"
                    elif 'experience' in lower_section or 'work history' in lower_section:
                        css_class = "resume-experience"
                    elif 'education' in lower_section or 'degrees' in lower_section:
                        css_class = "resume-education"
                    elif 'skills' in lower_section or 'abilities' in lower_section:
                        css_class = "resume-skills"

                # Add section with CSS class
                editable_resume.add_section(display_name, content)
                if css_class and display_name in editable_resume.sections:
                    editable_resume.sections[display_name].css_class = css_class

        return editable_resume

    def apply_recommendations(self, editable_resume: 'EditableResume', recommendations: List[Dict]) -> None:
        """
        Apply a list of recommendations to the editable resume.

        Args:
            editable_resume (EditableResume): The resume being edited.
            recommendations (List[Dict]): List of recommendation dictionaries.
        """
        for rec in recommendations:
            try:
                result = editable_resume.apply_recommendation(rec)
            except Exception as e:
                raise ValueError(f"Error applying recommendation: {str(e)}")

    def get_edit_summary(self, editable_resume: 'EditableResume') -> Dict[str, List[Dict]]:
        """
        Get a summary of all edits made to the resume.

        Args:
            editable_resume (EditableResume): The resume being edited.

        Returns:
            Dict[str, List[Dict]]: Summary of changes by section.
        """
        edit_summary = {}

        for section_name, section in editable_resume.sections.items():
            if section.edit_history:
                edit_summary[section_name] = []
                for change in section.edit_history:
                    try:
                        change_data = eval(change)
                        edit_summary[section_name].append({
                            "timestamp": change_data["timestamp"],
                            "change": f"{change_data['previous']} → {change_data['current']}"
                        })
                    except Exception as e:
                        raise ValueError(f"Could not parse edit history entry: {str(e)}")

        return edit_summary

    def export_to_text(self, editable_resume: 'EditableResume') -> str:
        """
        Export the edited resume as plain text.

        Args:
            editable_resume (EditableResume): The resume being edited.

        Returns:
            str: The complete formatted resume text.
        """
        return editable_resume.get_final_resume_text()


class EditableResumeSection(BaseModel):
    """Editable resume section with versioning, change tracking, and CSS styling."""

    content: str = Field(
        description="The editable text content of this section"
    )
    original_content: Optional[str] = Field(
        None,
        description="Original content from parsed resume (for comparison)"
    )
    css_class: Optional[str] = Field(
        default=None,
        description="CSS class for styling this section (e.g., 'resume-experience')"
    )
    last_edited: Optional[datetime] = Field(
        default_factory=datetime.now,
        description="Timestamp of the last edit"
    )
    edit_history: List[str] = Field(
        default_factory=list,
        description="History of changes made to this section"
    )

    def apply_change(self, new_content: str) -> None:
        """Apply a change to this section and track it."""
        if self.content != new_content:
            # Track the change
            change_record = {
                "timestamp": datetime.now().isoformat(),
                "previous": self.content,
                "current": new_content
            }
            self.edit_history.append(str(change_record))

            # Update content
            self.content = new_content
            self.last_edited = datetime.now()

    def revert_to(self, version: int) -> str:
        """Revert to a specific version in the edit history."""
        if 0 <= version < len(self.edit_history):
            change_record = eval(self.edit_history[version])
            self.content = change_record["current"]
            self.last_edited = datetime.fromisoformat(change_record["timestamp"])
            return f"Reverted to version {version}: {self.content}"
        else:
            raise ValueError(f"Version {version} out of range (0-{len(self.edit_history)-1})")

    def format_for_display(self, bullet_points: bool = True) -> str:
        """Format the content for display in the UI."""
        if not self.content.strip():
            return ""

        lines = self.content.split('\n')
        formatted_lines = []

        for line in lines:
            line = line.strip()
            if not line:
                continue

            # Format bullets
            if bullet_points and (line.startswith('- ') or line.startswith('• ')):
                if not line.startswith('- '):
                    line = '• ' + line
            elif not line.startswith('-') and not line.startswith('•'):
                line = '- ' + line

            formatted_lines.append(line)

        return '\n'.join(formatted_lines)

    def to_markdown(self) -> str:
        """Convert section content to markdown format."""
        if not self.content.strip():
            return ""

        converter = MarkdownConverter()
        return converter.text_to_markdown(self.content)
    
    def from_markdown(self, markdown_content: str) -> None:
        """Update section content from markdown format."""
        if not markdown_content or not isinstance(markdown_content, str):
            return

        converter = MarkdownConverter()
        self.apply_change(converter.markdown_to_html(markdown_content))


class EditableResume(BaseModel):
    """Complete editable resume structure with structured sections."""
    
    raw_text: str = Field(
        description="The complete raw text extracted from the PDF resume"
    )
    original_data: ResumeData = Field(
        description="Original parsed resume data for reference and comparison"
    )
    sections: Dict[str, EditableResumeSection] = Field(
        default_factory=dict,
        description="Dictionary of editable resume sections with change tracking"
    )
    
    class Config:
        """Pydantic configuration for EditableResume."""
        json_schema_extra = {
            "example": {
                "raw_text": "John Doe\nSoftware Engineer...",
                "original_data": {
                    # ResumeData example structure
                },
                "sections": {
                    "Contact Information": {
                        "content": "John Doe\njohn.doe@example.com",
                        "original_content": "John Doe\njohn.doe@example.com",
                        "last_edited": "2025-07-25T12:49:00",
                        "edit_history": []
                    },
                    "Skills": {
                        "content": "Python, Django, Flask",
                        "original_content": "Python, Django, Flask",
                        "last_edited": "2025-07-25T12:49:00",
                        "edit_history": [
                            '{"timestamp": "2025-07-25T12:30:00", "previous": "Python, Django", "current": "Python, Django, Flask"}'
                        ]
                    }
                }
            }
        }

    def add_section(self, name: str, content: str, css_class: Optional[str] = None) -> None:
        """Add a new editable section to the resume."""
        if name not in self.sections:
            self.sections[name] = EditableResumeSection(
                content=content,
                original_content=content
            )
            # Apply CSS class if provided
            if css_class:
                self.sections[name].css_class = css_class

    def remove_section(self, name: str) -> Optional[str]:
        """Remove an existing section from the resume."""
        if name in self.sections:
            removed = self.sections.pop(name)
            return removed.content
        return None

    def get_final_resume_text(self) -> str:
        """Generate the final resume text after all edits."""
        edited_sections = []

        for section_name, section_data in self.sections.items():
            if section_data.content.strip():
                formatted_content = section_data.format_for_display()
                if formatted_content.strip():
                    edited_sections.append(f"=== {section_name} ===\n{formatted_content}")

        return "\n\n".join(edited_sections)

    def export_to_markdown(self) -> str:
        """Export the entire resume as markdown format."""
        markdown_sections = []

        for section_name, section_data in self.sections.items():
            if section_data.content.strip():
                # Convert each section to markdown
                markdown_content = section_data.to_markdown()
                if markdown_content.strip():
                    # Format section header with appropriate markdown syntax
                    header = f"# {section_name}"
                    markdown_sections.append(f"{header}\n\n{markdown_content}")
                    # Add extra space between sections
                    markdown_sections.append("")  # Empty line for spacing

        return "\n".join(markdown_sections)

    def export_section_to_markdown(self, section_name: str) -> Optional[str]:
        """Export a specific section as markdown format."""
        if section_name not in self.sections:
            return None

        section = self.sections[section_name]
        if not section.content.strip():
            return None

        # Convert to markdown
        markdown_content = section.to_markdown()
        if not markdown_content.strip():
            return None

        # Format with header and spacing
        header = f"# {section_name}"
        return f"{header}\n\n{markdown_content}"

    def apply_recommendation(self, recommendation: Dict) -> str:
        """Apply a specific recommendation to the appropriate section."""
        section_name = self._map_section_name(recommendation.get("section", ""))
        
        if section_name not in self.sections:
            # Create new section if it doesn't exist
            content = f"- {recommendation['content']}"
            self.add_section(section_name, content)
            return f"Added new {section_name} with recommendation"
        
        # Apply to existing section
        current_content = self.sections[section_name].content
        new_content = self._apply_to_section(current_content, recommendation)
        
        self.sections[section_name].apply_change(new_content)
        return f"Applied recommendation to {section_name}"

    def _map_section_name(self, recommendation_section: str) -> str:
        """Map recommendation section names to internal section names."""
        mapping = {
            "Skills": "Skills",
            "Experience": "Experience",
            "Education": "Education",
            "Summary": "Summary",
            "Contact Information": "Contact Information",
            "Certifications": "Certifications"
        }
        
        # Convert from recommendation format to internal format
        section_name = mapping.get(recommendation_section, recommendation_section)
        
        # Standardize format (title case with spaces)
        return section_name.replace("_", " ").title()

    def _apply_to_section(self, current_content: str, recommendation: Dict) -> str:
        """Apply a specific recommendation to section content."""
        rec_type = recommendation.get("type", "")
        content = recommendation.get("content", "")
        
        if rec_type == "add":
            # Add new bullet point (if not already present)
            if f"- {content}" not in current_content:
                return f"{current_content}\n- {content}"
            else:
                return current_content
        
        elif rec_type == "modify" or rec_type == "emphasize":
            # Modify existing content - for simplicity, prepend the recommendation
            lines = current_content.split('\n')
            if lines[0].startswith('-'):
                lines[0] = f"- {content} ({lines[0][2:]})"
            else:
                lines.insert(0, f"- {content}")
            return '\n'.join(lines)
        
        elif rec_type == "remove":
            # Remove content (simplified - just remove exact match)
            if f"- {content}" in current_content:
                return current_content.replace(f"\n- {content}", "")
            else:
                return current_content
        
        return current_content

    def to_dict(self) -> Dict:
        """Convert to dictionary format for serialization."""
        result = {
            "raw_text": self.raw_text,
            "original_data": self.original_data.model_dump(),
            "sections": {}
        }
        
        for section_name, section in self.sections.items():
            result["sections"][section_name] = {
                "content": section.content,
                "original_content": section.original_content,
                "last_edited": section.last_edited.isoformat(),
                "edit_history": section.edit_history
            }
        
        return result

    @classmethod
    def from_dict(cls, data: Dict) -> 'EditableResume':
        """Create EditableResume from dictionary."""
        if isinstance(data.get("original_data"), dict):
            original_data = ResumeData(**data["original_data"])
        else:
            original_data = data["original_data"]
        
        editable_sections = {}
        for section_name, section_data in data.get("sections", {}).items():
            section = EditableResumeSection(
                content=section_data["content"],
                original_content=section_data.get("original_content"),
                last_edited=datetime.fromisoformat(section_data["last_edited"]),
                edit_history=section_data.get("edit_history", [])
            )
            editable_sections[section_name] = section
        
        return cls(
            raw_text=data.get("raw_text", ""),
            original_data=original_data,
            sections=editable_sections
        )
