"""
Resume Editor module for Resume Helper.

This module provides functionality for editing and customizing resumes
based on analysis results. It includes Pydantic models for editable resume data
and core logic for managing resume edits.
"""

from pydantic import BaseModel, Field
from typing import Optional, Dict, List
from datetime import datetime

from ..models.responses import ResumeData


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

        # Add each section to the editable resume
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
                editable_resume.add_section(display_name, content)

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
                print(f"✅ {result}")
            except Exception as e:
                print(f"❌ Error applying recommendation: {str(e)}")

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
                        print(f"Warning: Could not parse edit history entry: {str(e)}")

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
    """Editable resume section with versioning and change tracking."""
    
    content: str = Field(
        description="The editable text content of this section"
    )
    original_content: Optional[str] = Field(
        None,
        description="Original content from parsed resume (for comparison)"
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

    def add_section(self, name: str, content: str) -> None:
        """Add a new editable section to the resume."""
        if name not in self.sections:
            self.sections[name] = EditableResumeSection(
                content=content,
                original_content=content
            )

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

# Example usage
if __name__ == "__main__":
    # Create an example editable resume
    from ..models.responses import ResumeData, ResumeSection

    # Sample data for testing
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
    editable_resume = EditableResume(
        raw_text=resume_data.raw_text,
        original_data=resume_data
    )
    
    # Add sections from the parsed data
    for section_name, content in sample_resume["sections"].items():
        display_name = section_name.replace("_", " ").title()
        editable_resume.add_section(display_name, content)
    
    # Test basic functionality
    print("=== Original Resume ===")
    for name, section in editable_resume.sections.items():
        print(f"{name}: {section.content}")
    
    # Apply a recommendation
    recommendation = {
        "section": "Skills",
        "type": "add",
        "content": "Flask",
        "reason": "Web development framework"
    }
    result = editable_resume.apply_recommendation(recommendation)
    print(f"\nApplied: {result}")
    
    # Test edit history
    skills_section = editable_resume.sections["Skills"]
    print(f"Edit history for Skills: {skills_section.edit_history}")
    
    # Generate final text
    final_text = editable_resume.get_final_resume_text()
    print("\n=== Final Resume Text ===")
    print(final_text)
