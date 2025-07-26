"""
PDF Export module for Resume Helper.

This module provides functionality to export edited resumes as PDF files
using ReportLab with support for rich formatting and CSS styling.
"""

from reportlab.lib.pagesizes import letter
from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor

from ..editor.styles import CSS_TO_PDF_STYLE_MAP, DEFAULT_PDF_STYLE


class ResumePDFExporter:
    """Class for exporting resume data to PDF format with enhanced formatting support."""

    def __init__(self):
        """Initialize the PDF exporter."""
        self.styles = getSampleStyleSheet()

        # Enhanced custom styles with CSS mapping support
        self.custom_styles = {
            'section_title': ParagraphStyle(
                name='SectionTitle',
                parent=self.styles['Heading2'],
                fontSize=14,
                leading=16,
                textColor='#003366',
                spaceBefore=10,
                spaceAfter=5
            ),
            'skill_item': ParagraphStyle(
                name='SkillItem',
                parent=self.styles['BodyText'],
                bulletChar='• ',
                fontSize=12,
                leading=14,
                spaceBefore=0,
                spaceAfter=3
            ),
            'experience_item': ParagraphStyle(
                name='ExperienceItem',
                parent=self.styles['BodyText'],
                bulletChar='• ',
                fontSize=12,
                leading=14,
                spaceBefore=0,
                spaceAfter=5
            ),
            # Enhanced styles for different section types
            'resume_contact': ParagraphStyle(
                name='ResumeContact',
                parent=self.styles['BodyText'],
                fontSize=12,
                leading=16,
                textColor='#333333'
            ),
            'resume_summary': ParagraphStyle(
                name='ResumeSummary',
                parent=self.styles['BodyText'],
                fontSize=12,
                leading=18,
                spaceBefore=5
            ),
            'resume_experience': ParagraphStyle(
                name='ResumeExperience',
                parent=self.styles['BodyText'],
                bulletChar='• ',
                fontSize=12,
                leading=16
            ),
            'resume_education': ParagraphStyle(
                name='ResumeEducation',
                parent=self.styles['BodyText'],
                bulletChar='• ',
                fontSize=12,
                leading=16
            ),
            'resume_skills': ParagraphStyle(
                name='ResumeSkills',
                parent=self.styles['BodyText'],
                bulletChar='• ',
                fontSize=12,
                leading=14,
                spaceBefore=0,
                spaceAfter=3
            )
        }

    def export_to_pdf(self, resume_data, output_path):
        """
        Export an editable resume to PDF format with enhanced styling.

        Args:
            resume_data (EditableResume): The resume data to export.
            output_path (str): Path where the PDF should be saved.

        Returns:
            str: Path to the generated PDF file.
        """
        # Create a PDF document
        doc = SimpleDocTemplate(
            output_path,
            pagesize=letter,
            title="Edited Resume",
            author="Resume Helper"
        )

        # Prepare content
        story = []

        # Add resume title/heading with better styling
        story.append(Paragraph("Resume", self.styles['Heading1']))
        story.append(Spacer(1, 0.3 * inch))

        # Process each section with enhanced formatting support
        for section_name, section_data in resume_data.sections.items():
            if section_data.content.strip():

                # Get CSS class for this section (from original parsing)
                css_class = self._get_section_css_class(resume_data, section_name)

                # Select appropriate style based on content and detected CSS
                pdf_style = self._get_pdf_style_for_section(section_name, css_class)

                # Add section title with appropriate style and color
                section_title = Paragraph(
                    f"{section_name}",
                    self.custom_styles['section_title']
                )

                # Apply custom styling if available
                if css_class in CSS_TO_PDF_STYLE_MAP:
                    style_map = CSS_TO_PDF_STYLE_MAP[css_class]
                    if 'title_color' in style_map:
                        section_title.textColor = HexColor(style_map['title_color'])

                story.append(section_title)

                # Format the content based on section type and detected styles
                formatted_content = self._format_section_content_enhanced(
                    section_name,
                    section_data.content,
                    css_class
                )

                # Add the formatted content
                if formatted_content:
                    for paragraph in formatted_content:
                        story.append(paragraph)
                        story.append(Spacer(1, 0.2 * inch))

                # Add space between sections based on type
                section_spacing = pdf_style.get('spacing_after', 0.4 * 72) / 72
                story.append(Spacer(1, section_spacing * inch))

        try:
            doc.build(story)
            return output_path

        except Exception as e:
            raise ValueError(f"Failed to generate PDF: {e}")

    def _get_section_css_class(self, resume_data, section_name):
        """
        Get the CSS class for a section from the editable resume or original parsed data.

        Args:
            resume_data (EditableResume): The resume data containing style information.
            section_name (str): Name of the section to get CSS class for.

        Returns:
            str: CSS class name or empty string if not found.
        """
        # First try to get CSS class from editable sections
        css_class = ""
        if hasattr(resume_data, 'sections') and section_name in resume_data.sections:
            section_obj = resume_data.sections[section_name]
            if hasattr(section_obj, 'css_class'):
                css_class = section_obj.css_class

        # If no CSS class from editable sections, fall back to original data
        if not css_class:
            try:
                # Check different possible ways to access styles in original data
                if hasattr(resume_data.original_data, 'sections'):
                    sections_obj = resume_data.original_data.sections

                    # Handle both Pydantic and dict formats
                    if hasattr(sections_obj, 'styles'):
                        if isinstance(sections_obj.styles, dict):
                            for section_title, class_name in sections_obj.styles.items():
                                if (section_title.lower().replace(' ', '_') == section_name.lower().replace(' ', '_') or
                                    section_title.replace(" ", "") == section_name.replace(" ", "")):
                                    css_class = class_name
                                    break

                # Map common field names to display names
                if not css_class:
                    # Try mapping from field name to CSS class
                    field_mapping = {
                        "Contact Information": "resume-contact",
                        "Summary": "resume-summary",
                        "Experience": "resume-experience",
                        "Education": "resume-education",
                        "Skills": "resume-skills"
                    }
                    # Try both exact match and partial match
                    for display_name, css_class_value in field_mapping.items():
                        if (display_name.lower() == section_name.lower() or
                            display_name.replace(" ", "_").lower() == section_name.lower().replace(" ", "_")):
                            css_class = css_class_value
                            break

            except Exception as e:
                # If any error occurs, log it and continue with fallback logic
                print(f"Error getting CSS class from original data: {e}")

        return css_class

    def _get_pdf_style_for_section(self, section_name, css_class):
        """
        Get the PDF styling parameters for a section based on its CSS class.

        Args:
            section_name (str): Name of the section.
            css_class (str): CSS class for the section.

        Returns:
            dict: Style parameters for PDF formatting.
        """
        # Return appropriate style based on CSS class
        if css_class and css_class in CSS_TO_PDF_STYLE_MAP:
            return CSS_TO_PDF_STYLE_MAP[css_class]
        elif section_name.lower() == 'contact information':
            return CSS_TO_PDF_STYLE_MAP['resume-contact']
        elif section_name.lower() == 'summary':
            return CSS_TO_PDF_STYLE_MAP['resume-summary']
        elif section_name.lower() == 'experience' or 'experience' in section_name.lower():
            return CSS_TO_PDF_STYLE_MAP['resume-experience']
        elif section_name.lower() == 'education':
            return CSS_TO_PDF_STYLE_MAP['resume-education']
        elif section_name.lower() == 'skills':
            return CSS_TO_PDF_STYLE_MAP['resume-skills']
        
        # Default style for other sections
        return DEFAULT_PDF_STYLE

    def _format_section_content_enhanced(self, section_name, content, css_class=""):
        """
        Enhanced section content formatting with better bullet handling and styling.

        Args:
            section_name (str): Name of the section.
            content (str): The raw text content of the section.
            css_class (str): Detected CSS class for this section.

        Returns:
            list: List of formatted Paragraph objects.
        """
        paragraphs = []
        
        # Get appropriate PDF styling parameters
        pdf_style = self._get_pdf_style_for_section(section_name, css_class)
        
        # Handle different section types with appropriate formatting
        if section_name.lower() == 'contact information':
            # Format contact info as styled paragraphs
            lines = [line.strip() for line in content.split('\n') if line.strip()]
            if len(lines) > 1:
                # Split into name and details
                name = lines[0]
                details = "\n".join(lines[1:])
                
                name_paragraph = Paragraph(f"<strong>{name}</strong>", self.custom_styles['resume_contact'])
                details_paragraph = Paragraph(details, self.styles['BodyText'])
                paragraphs.extend([name_paragraph, Spacer(1, 0.1 * inch), details_paragraph])
            else:
                paragraphs.append(Paragraph(content, self.custom_styles['resume_contact']))

        elif section_name.lower() == 'summary' or section_name.lower() == 'objective':
            # Format summary with proper styling
            paragraphs.append(Paragraph(content, self.custom_styles['resume_summary']))

        elif section_name.lower() == 'skills':
            # Format skills as bullet points with column layout if many items
            lines = [line.strip() for line in content.split('\n') if line.strip()]
            
            # Use appropriate bullet character based on CSS class
            bullet_char = pdf_style.get('bullet_char', '•')
            
            skill_paragraphs = []
            for skill in lines:
                skill_text = f"{bullet_char} {skill}"
                skill_paragraphs.append(Paragraph(skill_text, self.custom_styles['resume_skills']))
                
                # Add some space between skills but not too much
                if len(lines) > 1 and skill != lines[-1]:
                    skill_paragraphs.append(Spacer(1, 0.05 * inch))
            
            paragraphs.extend(skill_paragraphs)

        elif section_name.lower() == 'experience' or 'experience' in section_name.lower():
            # Format experience with bullet points and proper indentation
            lines = [line.strip() for line in content.split('\n') if line.strip()]
            
            # Group by job title/description blocks
            job_blocks = []
            current_block = []

            for line in lines:
                if line.startswith('- ') or line.startswith('• '):
                    # Add the previous block if it exists, then start a new one
                    if current_block:
                        job_blocks.append(current_block)
                        current_block = []
                    # Remove bullet before adding to block
                    line_content = line[2:] if line.startswith('-') else line[2:]
                    current_block.append(line_content)
                elif current_block:
                    current_block.append(line)
                else:
                    current_block.append(line)
            
            if current_block:
                job_blocks.append(current_block)
            
            # Format each job block with proper hierarchy
            for job in job_blocks:
                job_title = job[0]
                job_details = []
                
                # Add job title with stronger styling
                job_title_para = Paragraph(f"<b>{job_title}</b>", self.custom_styles['resume_experience'])
                paragraphs.append(job_title_para)
                
                # Format remaining details as bullet points
                for detail in job[1:]:
                    if not detail.startswith('-') and not detail.startswith('•'):
                        detail = f"{bullet_char} {detail}"
                    job_details.append(Paragraph(detail, self.custom_styles['experience_item']))
                    
                if job_details:
                    paragraphs.extend(job_details)
                    paragraphs.append(Spacer(1, 0.1 * inch))

        elif section_name.lower() == 'education':
            # Format education with proper hierarchy and bullet points
            lines = [line.strip() for line in content.split('\n') if line.strip()]
            
            # Group by degree/education blocks
            edu_blocks = []
            current_block = []

            for line in lines:
                if line.startswith('- ') or line.startswith('• '):
                    # Add the previous block if it exists, then start a new one
                    if current_block:
                        edu_blocks.append(current_block)
                        current_block = []
                    # Remove bullet before adding to block
                    line_content = line[2:] if line.startswith('-') else line[2:]
                    current_block.append(line_content)
                elif current_block:
                    current_block.append(line)
                else:
                    current_block.append(line)
            
            if current_block:
                edu_blocks.append(current_block)
            
            # Format each education block with proper hierarchy
            for degree in edu_blocks:
                degree_title = degree[0]
                degree_details = []
                
                # Add degree title with stronger styling
                degree_title_para = Paragraph(f"<b>{degree_title}</b>", self.custom_styles['resume_education'])
                paragraphs.append(degree_title_para)
                
                # Format remaining details as bullet points
                for detail in degree[1:]:
                    if not detail.startswith('-') and not detail.startswith('•'):
                        detail = f"{bullet_char} {detail}"
                    degree_details.append(Paragraph(detail, self.custom_styles['resume_education']))
                    
                if degree_details:
                    paragraphs.extend(degree_details)
                    paragraphs.append(Spacer(1, 0.1 * inch))

        else:
            # Default formatting for other sections with proper styling
            lines = [line.strip() for line in content.split('\n') if line.strip()]
            
            for line in lines:
                paragraph_style = self.styles['BodyText']
                
                # Apply section-specific styling
                if 'summary' in section_name.lower():
                    paragraph_style = self.custom_styles['resume_summary']
                elif css_class == 'resume-heading':
                    paragraph_style.fontSize = 14
                    paragraph_style.textColor = HexColor('#2a2a2a')
                    paragraph_style.fontWeight = 'bold'
            
                paragraphs.append(Paragraph(line, paragraph_style))
                
                # Add space between paragraphs but not too much
                if len(lines) > 1 and line != lines[-1]:
                    paragraphs.append(Spacer(1, 0.1 * inch))

        return paragraphs

    @staticmethod
    def generate_resume_pdf(resume_data, output_path):
        """
        Static method to export an EditableResume as PDF.

        Args:
            resume_data (EditableResume): The editable resume to export.
            output_path (str): Path where the PDF should be saved.

        Returns:
            str: Path to the generated PDF file.
        """
        exporter = ResumePDFExporter()
        return exporter.export_to_pdf(resume_data, output_path)

# Example usage
if __name__ == "__main__":
    from app.editor import EditableResume

    # Create a sample resume for testing
    test_resume = EditableResume(
        raw_text="Sample resume text...",
        original_data=None,
        sections={
            "Contact Information": {
                "content": "John Doe\njohn.doe@example.com\n555-123-4567"
            },
            "Summary": {
                "content": "Highly motivated software engineer with 5+ years of experience in full-stack development."
            },
            "Skills": {
                "content": "Python\nDjango\nJavaScript\nReact\nSQL"
            }
        }
    )

    # Export to PDF
    output_file = "/tmp/test_resume.pdf"
    ResumePDFExporter.generate_resume_pdf(test_resume, output_file)
    print(f"PDF exported successfully: {output_file}")
