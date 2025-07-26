"""
Resume Helper - Streamlit Web Application

A modern web interface for the Resume Helper tool that allows job seekers
to tailor their resumes to specific job postings using AI-powered analysis.
"""

import streamlit as st
import os
import sys
from typing import Optional, Dict, Any
import json

# Add the app directory to the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

    # Import our modules
import streamlit_quill  # Import the rich text editor module
from app.parser.pdf_parser import ResumeParser
from app.editor.styles import RESUME_CSS_STYLES, CSS_TO_PDF_STYLE_MAP
from app.analyzer.job_analyzer import JobAnalyzer
from app.comparison.matcher import ResumeMatcher
from app.recommendation.generator import RecommendationGenerator

# Markdown support
import markdown2  # For rendering markdown in the editor interface

# Page configuration
st.set_page_config(
    page_title="Resume Helper",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-title {
        font-size: 2.5rem;
        font-weight: 700;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 0.5rem;
    }
    .subtitle {
        font-size: 1.2rem;
        color: #666;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin: 1rem 0;
    }
    .success-box {
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        border-radius: 5px;
        padding: 1rem;
        margin: 1rem 0;
    }
    .warning-box {
        background-color: #fff3cd;
        border: 1px solid #ffeaa7;
        border-radius: 5px;
        padding: 1rem;
        margin: 1rem 0;
    }
    /* Editor styling */
    .editor-container {
        display: flex;
        gap: 2rem;
        margin-top: 2rem;
    }
    .editor-column {
        flex: 1;
        min-width: 400px;
    }
    .preview-section {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 5px;
        border: 1px solid #ddd;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
def initialize_session_state():
    """Initialize session state variables."""
    if 'job_requirements' not in st.session_state:
        st.session_state.job_requirements = None
    if 'resume_data' not in st.session_state:
        st.session_state.resume_data = None
    if 'comparison_results' not in st.session_state:
        st.session_state.comparison_results = None
    if 'recommendations' not in st.session_state:
        st.session_state.recommendations = None
    if 'analysis_complete' not in st.session_state:
        st.session_state.analysis_complete = False

# Initialize components
@st.cache_resource
def get_components():
    """Initialize and cache the application components."""
    return {
        'parser': ResumeParser(),
        'analyzer': JobAnalyzer(),
        'matcher': ResumeMatcher(),
        'generator': RecommendationGenerator()
    }

def main():
    """Main application function."""
    initialize_session_state()
    components = get_components()

    # Title and header
    st.markdown('<h1 class="main-title">📄 Resume Helper</h1>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">Tailor your resume to match job descriptions using AI-powered analysis</p>', unsafe_allow_html=True)

    # Sidebar navigation
    st.sidebar.title("Navigation")
    page = st.sidebar.radio(
        "Choose a section:",
        ["📊 Analysis", "📝 Job Requirements", "🎯 Resume Upload", "🛠️ Editor", "⚙️ Settings"]
    )

    # Main content based on selected page
    if page == "📊 Analysis":
        show_analysis_page()
    elif page == "📝 Job Requirements":
        show_job_requirements_page(components['analyzer'])
    elif page == "🎯 Resume Upload":
        show_resume_upload_page(components['parser'])
    elif page == "🛠️ Editor":
        show_editor_page()
    elif page == "⚙️ Settings":
        show_settings_page()

def show_editor_page():
    """Display the resume editor page."""
    st.header("🛠️ Resume Editor")

    # Check if we have resume data
    if not st.session_state.resume_data:
        st.warning("Please upload and process a resume first before using the editor.")
        return

    # Import editor components
    from app.editor import EditableResume, EditableResumeSection, ResumeEditor

    # Initialize editor if not already in session state
    if 'editable_resume' not in st.session_state:
        try:
            editor = ResumeEditor()
            editable_resume = editor.create_from_resume_data(st.session_state.resume_data)
            st.session_state.editable_resume = editable_resume
        except Exception as e:
            st.error(f"❌ Error initializing resume editor: {str(e)}")
            return

    # Display current status
    editable_resume = st.session_state.editable_resume

    st.subheader("📋 Current Resume Sections")

    # Show sections with edit forms
    section_names = list(editable_resume.sections.keys())
    if not section_names:
        st.info("No sections found in resume. Please process a valid resume first.")
        return

    # Sidebar for navigation between sections
    selected_section = st.sidebar.selectbox(
        "Select section to edit:",
        section_names,
        index=0
    )

    # Display the selected section with editing controls
    st.subheader(f"📝 Editing: {selected_section}")

    section_data = editable_resume.sections[selected_section]

    # Display current content
    st.markdown(f"**Current Content:**")
    st.code(section_data.content, language="text")

    # Get CSS class for this section (from editable section if available)
    css_class = ""
    if hasattr(st.session_state.resume_data, 'sections') and hasattr(st.session_state.resume_data.sections, 'styles'):
        styles_obj = st.session_state.resume_data.sections.styles
        if isinstance(styles_obj, dict):
            # Look for exact section name match or partial match in keys
            for style_name, class_name in styles_obj.items():
                if selected_section in style_name:
                    css_class = class_name
                    break

    # If no CSS class from original parsing but we have editable resume data, check that
    if not css_class and hasattr(st.session_state, 'editable_resume'):
        if selected_section in st.session_state.editable_resume.sections:
            editable_section = st.session_state.editable_resume.sections[selected_section]
            if hasattr(editable_section, 'css_class') and editable_section.css_class:
                css_class = editable_section.css_class

    # If still no CSS class found, use section name to infer it
    if not css_class and selected_section:
        section_lower = selected_section.lower()
        if 'contact' in section_lower or 'name' in section_lower:
            css_class = "resume-contact"
        elif 'summary' in section_lower or 'objective' in section_lower:
            css_class = "resume-summary"
        elif 'experience' in section_lower or 'work history' in section_lower:
            css_class = "resume-experience"
        elif 'education' in section_lower or 'degrees' in section_lower:
            css_class = "resume-education"
        elif 'skills' in section_lower or 'abilities' in section_lower:
            css_class = "resume-skills"

    # Add CSS styles for resume sections - these will style the live preview and editor content
    st.markdown(f'<style>{RESUME_CSS_STYLES}</style>', unsafe_allow_html=True)

    # Use editor container layout
    st.markdown('<div class="editor-container">', unsafe_allow_html=True)

    # Left column for editing
    st.markdown('<div class="editor-column">', unsafe_allow_html=True)

    # Form for editing the section content using rich text editor
    new_content = streamlit_quill.st_quill(
        value=section_data.content,
        placeholder="Edit your resume section here...",
        css_class=css_class,  # Apply section-specific CSS class
        html=True,
        toolbar='full',  # Use full toolbar for rich editing capabilities
        height=300,
        help=f"Modify the content of this resume section with formatting options. CSS class: {css_class}"
    )

    # Buttons for actions
    col1, col2 = st.columns([1, 1])

    with col1:
        if st.button("💾 Save Changes"):
            try:
                section_data.apply_change(new_content)
                st.success(f"✅ Section '{selected_section}' updated successfully!")
            except Exception as e:
                st.error(f"❌ Error saving changes: {str(e)}")

    with col2:
        if len(section_data.edit_history) > 0:
            version = st.number_input(
                "Select version to revert to",
                min_value=0,
                max_value=len(section_data.edit_history)-1,
                step=1,
                value=len(section_data.edit_history)-1
            )
            if st.button("⏮️ Revert"):
                try:
                    section_data.revert_to(version)
                    st.success(f"✅ Reverted {selected_section} to version {version}")
                except Exception as e:
                    st.error(f"❌ Error reverting: {str(e)}")

    # Display edit history if available
    if section_data.edit_history:
        st.subheader("🕒 Edit History")

        for i, change in enumerate(section_data.edit_history):
            try:
                change_data = eval(change)
                timestamp = change_data.get("timestamp", "Unknown")
                previous = change_data.get("previous", "")
                current = change_data.get("current", "")

                with st.expander(f"Version {len(section_data.edit_history) - i} ({timestamp})"):
                    st.write(f"**Before:** {previous}")
                    st.write(f"**After:**  {current}")

            except Exception as e:
                st.warning(f"Could not parse edit history entry: {str(e)}")

    # Right column for preview
    st.markdown('</div><div class="editor-column">', unsafe_allow_html=True)

    # Live preview section with enhanced formatting support and markdown view toggle
    st.subheader("🔍 Live Preview")

    # Toggle for markdown/HTML display
    if 'markdown_view_enabled' not in st.session_state:
        st.session_state.markdown_view_enabled = False

    col1, col2 = st.columns([1, 4])
    with col1:
        markdown_view_toggle = st.checkbox("📄 View as Markdown", value=st.session_state.markdown_view_enabled)

    # Update session state
    if st.session_state.markdown_view_enabled != markdown_view_toggle:
        st.session_state.markdown_view_enabled = markdown_view_toggle

    st.markdown('<div class="preview-section">', unsafe_allow_html=True)

    # Display either HTML preview or markdown depending on the toggle
    if st.session_state.markdown_view_enabled:
        # Convert current content to markdown and display it
        try:
            from app.editor.markdown_utils import MarkdownConverter
            converter = MarkdownConverter()
            markdown_content = converter.text_to_markdown(new_content)
            st.code(markdown_content, language="markdown")
            st.info("⚠️ Note: This is a preview. To save as markdown, use the Export options.")
        except Exception as e:
            st.error(f"Error displaying markdown: {str(e)}")
    else:
        # Format the content for display using HTML/CSS for better visual representation
        if new_content.strip():
            # Apply CSS classes based on section type
            if css_class:
                html_preview = f'<div class="{css_class}">{new_content}</div>'
            else:
                html_preview = f'<div>{new_content}</div>'

            st.markdown(html_preview, unsafe_allow_html=True)
        else:
            st.info("Your changes will appear here in real-time.")

    st.markdown('</div>', unsafe_allow_html=True)

    # Display recommendations that apply to this section
    if st.session_state.recommendations and 'recommendations' in st.session_state.recommendations:
        st.subheader("💡 Recommendations for This Section")

        recs = st.session_state.recommendations['recommendations']
        section_recs = []

        # Find recommendations for this section
        for rec in recs:
            if rec.get('section', '').lower() == selected_section.lower():
                section_recs.append(rec)

        if section_recs:
            for i, rec in enumerate(section_recs):
                priority = rec.get('priority', 0)
                rec_type = rec.get('type', '')
                content = rec.get('content', '')
                reason = rec.get('reason', '')

                with st.expander(f"Recommendation {i+1} - Priority: {priority}"):
                    col_a, col_b, col_c = st.columns([2, 3, 5])

                    with col_a:
                        if st.button("✅ Apply", key=f"apply_{i}_{selected_section}"):
                            try:
                                editable_resume.apply_recommendation(rec)
                                st.success(f"✅ Recommendation applied to {selected_section}")
                                # Update the current section content display
                                new_content = editable_resume.sections[selected_section].content
                                st.rerun()
                            except Exception as e:
                                st.error(f"❌ Error applying recommendation: {str(e)}")

                    with col_b:
                        st.write(f"**Type:** {rec_type.capitalize()}")

                    with col_c:
                        st.write(f"**Content:** {content}")
                        st.write(f"**Reason:** {reason}")
        else:
            st.info("No specific recommendations for this section.")
    else:
        st.info("No recommendations available. Please run analysis first.")

    # Close editor container
    st.markdown('</div>', unsafe_allow_html=True)

    # Display CSS class information for the user
    if css_class:
        section_type = "Custom"
        if css_class in ["resume-contact", "resume-summary", "resume-experience", "resume-education", "resume-skills"]:
            section_type = {
                "resume-contact": "Contact",
                "resume-summary": "Summary/Objective",
                "resume-experience": "Experience",
                "resume-education": "Education",
                "resume-skills": "Skills"
            }[css_class]

        st.markdown(f"**🎨 Current Section Style:** {section_type} ({css_class})")
        st.info("This styling helps maintain visual consistency with your original resume format.")

    # Export options
    st.subheader("💾 Export Options")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("📄 Export as Text"):
            try:
                final_text = editable_resume.get_final_resume_text()
                st.session_state.exported_resume_text = final_text
                st.success("✅ Resume exported successfully!")
                st.download_button(
                    "Download Exported Resume",
                    data=final_text,
                    file_name="edited_resume.txt",
                    mime="text/plain"
                )
            except Exception as e:
                st.error(f"❌ Error exporting: {str(e)}")

    with col2:
        if st.button("🔄 Export to PDF"):
            try:
                from app.exporter.pdf_exporter import ResumePDFExporter

                # Generate a temporary filename for the PDF
                pdf_path = f"temp_edited_resume_{selected_section}.pdf"

                # Export the resume to PDF
                ResumePDFExporter.generate_resume_pdf(
                    editable_resume,
                    pdf_path
                )

                st.success("✅ Resume exported successfully!")
                with open(pdf_path, "rb") as f:
                    pdf_bytes = f.read()

                st.download_button(
                    "Download PDF",
                    data=pdf_bytes,
                    file_name="edited_resume.pdf",
                    mime="application/pdf"
                )

                # Clean up the temporary file
                import os
                if os.path.exists(pdf_path):
                    os.remove(pdf_path)
            except Exception as e:
                st.error(f"❌ Error with PDF export: {str(e)}")

    # Add markdown export option
    st.subheader("📄 Markdown Export Options")

    col3, col4 = st.columns(2)

    with col3:
        if st.button("Export Entire Resume as Markdown"):
            try:
                markdown_content = editable_resume.export_to_markdown()
                st.session_state.exported_markdown = markdown_content
                st.success("✅ Resume exported to markdown successfully!")
                st.download_button(
                    "Download Full Resume (Markdown)",
                    data=markdown_content,
                    file_name="edited_resume.md",
                    mime="text/markdown"
                )
            except Exception as e:
                st.error(f"❌ Error exporting markdown: {str(e)}")

    with col4:
        if st.button("Export This Section as Markdown"):
            try:
                section_markdown = editable_resume.export_section_to_markdown(selected_section)
                if section_markdown:
                    st.success(f"✅ '{selected_section}' exported to markdown successfully!")
                    st.download_button(
                        f"Download {selected_section} (Markdown)",
                        data=section_markdown,
                        file_name=f"{selected_section.lower().replace(' ', '_')}.md",
                        mime="text/markdown"
                    )
                else:
                    st.warning(f"No content available to export for '{selected_section}'")
            except Exception as e:
                st.error(f"❌ Error exporting section markdown: {str(e)}")

    # Add markdown import option
    st.subheader("📥 Markdown Import Options")

    markdown_file = st.file_uploader(
        "Upload a markdown file",
        type=['md', 'markdown'],
        help="Upload a markdown resume or section to merge with your current content"
    )

    if markdown_file:
        try:
            # Read the uploaded markdown file
            markdown_content = markdown_file.read().decode("utf-8")

            # Show preview of the markdown content
            st.subheader("📄 Markdown Preview")
            st.code(markdown_content, language="markdown")

            col_a, col_b = st.columns([1, 3])
            with col_a:
                if st.button("Import as New Section"):
                    section_name = st.text_input(
                        "Enter new section name",
                        placeholder="e.g., 'New Experience'"
                    )
                    if section_name and markdown_content.strip():
                        try:
                            # Import the markdown content
                            editable_resume.sections[section_name].from_markdown(markdown_content)
                            st.success(f"✅ Imported as new section: {section_name}")
                            st.rerun()
                        except Exception as e:
                            st.error(f"❌ Error importing as new section: {str(e)}")

                if st.button("Merge with Current Section"):
                    try:
                        # Update current section with markdown content
                        editable_resume.sections[selected_section].from_markdown(markdown_content)
                        st.success(f"✅ Merged with '{selected_section}'")
                        st.rerun()
                    except Exception as e:
                        st.error(f"❌ Error merging with current section: {str(e)}")

        except Exception as e:
            st.error(f"❌ Error processing markdown file: {str(e)}")

def show_analysis_page():
    """Display the main analysis dashboard."""
    st.header("📊 Analysis Dashboard")

    if not st.session_state.analysis_complete:
        st.info("👈 Please complete the job requirements and resume upload sections first.")

        # Show current status
        col1, col2 = st.columns(2)
        with col1:
            job_status = "✅ Complete" if st.session_state.job_requirements else "❌ Pending"
            st.metric("Job Analysis", job_status)
        with col2:
            resume_status = "✅ Complete" if st.session_state.resume_data else "❌ Pending"
            st.metric("Resume Upload", resume_status)

        return

    # Display analysis results
    if st.session_state.comparison_results and st.session_state.recommendations:
        # Match score display
        match_score = st.session_state.comparison_results.get("match_score", 0)

        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Match Score", f"{match_score}%")
        with col2:
            matches_count = len(st.session_state.comparison_results.get("matches", []))
            st.metric("Matches Found", matches_count)
        with col3:
            gaps_count = len(st.session_state.comparison_results.get("gaps", []))
            st.metric("Areas to Improve", gaps_count)

        # Results tabs
        tab1, tab2, tab3 = st.tabs(["📋 Summary", "✅ Matches", "⚠️ Gaps"])

        with tab1:
            st.subheader("Summary")
            summary = st.session_state.recommendations.get("summary", "No summary available.")
            st.markdown(summary)

            st.subheader("Recommendations")
            recommendations = st.session_state.recommendations.get("recommendations", [])

            for i, rec in enumerate(recommendations, 1):
                priority = rec.get("priority", 0)
                section = rec.get("section", "")
                rec_type = rec.get("type", "")
                content = rec.get("content", "")
                reason = rec.get("reason", "")

                with st.expander(f"{i}. {section} ({rec_type}) - Priority: {priority}"):
                    st.write(f"**Recommendation:** {content}")
                    st.write(f"**Reason:** {reason}")

            # Keyword suggestions
            if "keyword_suggestions" in st.session_state.recommendations:
                st.subheader("Suggested Keywords")
                keywords = st.session_state.recommendations["keyword_suggestions"]
                if keywords:
                    st.write("Consider adding these keywords to your resume:")
                    for keyword in keywords:
                        st.write(f"• {keyword}")

        with tab2:
            st.subheader("Matching Elements")
            matches = st.session_state.comparison_results.get("matches", [])

            if matches:
                for match in matches:
                    category = match.get("category", "").replace("_", " ").title()
                    item = match.get("item", "")
                    where_found = match.get("where_found", "")

                    st.success(f"**{category}:** {item}")
                    st.caption(f"Found in: {where_found}")
            else:
                st.info("No specific matches found.")

        with tab3:
            st.subheader("Areas for Improvement")
            gaps = st.session_state.comparison_results.get("gaps", [])

            if gaps:
                for gap in gaps:
                    category = gap.get("category", "").replace("_", " ").title()
                    item = gap.get("item", "")
                    suggestion = gap.get("suggestion", "")

                    st.warning(f"**{category}:** {item}")
                    st.caption(f"Suggestion: {suggestion}")
            else:
                st.success("Great! No significant gaps identified.")

def show_job_requirements_page(analyzer):
    """Display the job requirements analysis page."""
    st.header("📝 Job Requirements Analysis")

    st.write("Paste the job description below and click 'Analyze' to extract key requirements.")

    # Job description input
    job_description = st.text_area(
        "Job Description",
        height=300,
        placeholder="Paste the full job description here..."
    )

    col1, col2 = st.columns([1, 4])
    with col1:
        analyze_button = st.button("🔍 Analyze Job", type="primary")
    with col2:
        if st.session_state.job_requirements:
            st.success("✅ Job analysis complete!")

    if analyze_button and job_description.strip():
        with st.spinner("Analyzing job description..."):
            try:
                # Analyze job description
                job_requirements = analyzer.analyze_job_description(job_description)
                st.session_state.job_requirements = job_requirements

                # Check if we have both job and resume data for full analysis
                if st.session_state.resume_data:
                    perform_full_analysis()

                st.success("✅ Job analysis completed successfully!")
                st.rerun()

            except Exception as e:
                st.error(f"❌ Error analyzing job description: {str(e)}")

    # Display job requirements if available
    if st.session_state.job_requirements:
        st.subheader("📊 Analysis Results")

        job_req = st.session_state.job_requirements

        # Create tabs for different aspects
        tab1, tab2, tab3, tab4 = st.tabs(["🎯 Skills", "📚 Experience", "🎓 Qualifications", "🔑 Keywords"])

        with tab1:
            required_skills = job_req.required_skills if hasattr(job_req, 'required_skills') else []
            preferred_skills = job_req.preferred_skills if hasattr(job_req, 'preferred_skills') else []

            if required_skills:
                st.write("**Required Skills:**")
                for skill in required_skills:
                    st.write(f"• {skill}")

            if preferred_skills:
                st.write("**Preferred Skills:**")
                for skill in preferred_skills:
                    st.write(f"• {skill}")

        with tab2:
            experience = job_req.required_experience if hasattr(job_req, 'required_experience') else []
            if experience:
                for exp in experience:
                    st.write(f"• {exp}")
            else:
                st.info("No specific experience requirements identified.")

        with tab3:
            qualifications = job_req.required_education if hasattr(job_req, 'required_education') else []
            if qualifications:
                for qual in qualifications:
                    st.write(f"• {qual}")
            else:
                st.info("No specific qualifications identified.")

        with tab4:
            keywords = job_req.keywords if hasattr(job_req, 'keywords') else []
            if keywords:
                # Display keywords as tags
                st.write("**Key Terms:**")
                keyword_text = " • ".join(keywords)
                st.write(keyword_text)
            else:
                st.info("No specific keywords identified.")

def show_resume_upload_page(parser):
    """Display the resume upload page."""
    st.header("🎯 Resume Upload & Analysis")

    st.write("Upload your resume PDF to analyze its content and structure.")

    # File upload
    uploaded_file = st.file_uploader(
        "Choose your resume PDF",
        type=['pdf'],
        help="Upload a PDF version of your resume"
    )

    if uploaded_file is not None:
        col1, col2 = st.columns([1, 4])
        with col1:
            process_button = st.button("📄 Process Resume", type="primary")
        with col2:
            if st.session_state.resume_data:
                st.success("✅ Resume processed!")

        if process_button:
            with st.spinner("Processing resume..."):
                try:
                    # Save uploaded file temporarily
                    temp_path = f"temp_{uploaded_file.name}"
                    with open(temp_path, "wb") as f:
                        f.write(uploaded_file.getbuffer())

                    # Parse resume
                    resume_data = parser.parse_resume(temp_path)
                    st.session_state.resume_data = resume_data

                    # Clean up temp file
                    os.remove(temp_path)

                    # Check if we have both job and resume data for full analysis
                    if st.session_state.job_requirements:
                        perform_full_analysis()

                    st.success("✅ Resume processed successfully!")
                    st.rerun()

                except Exception as e:
                    st.error(f"❌ Error processing resume: {str(e)}")
                    if os.path.exists(temp_path):
                        os.remove(temp_path)

    # Display resume data if available
    if st.session_state.resume_data:
        st.subheader("📊 Resume Analysis")

        resume_data = st.session_state.resume_data

        # Basic info - handle both Pydantic and dict formats
        col1, col2 = st.columns(2)
        with col1:
            if hasattr(resume_data, 'raw_text'):
                word_count = len(resume_data.raw_text.split())
            else:
                word_count = len(resume_data.get("raw_text", "").split())
            st.metric("Total Words", word_count)
        with col2:
            if hasattr(resume_data, 'sections'):
                if hasattr(resume_data.sections, 'model_dump'):
                    sections_count = len([k for k, v in resume_data.sections.model_dump().items() if v])
                else:
                    sections_count = len(resume_data.sections.to_dict())
            else:
                sections_count = len(resume_data.get("sections", {}))
            st.metric("Sections Found", sections_count)

        # Sections
        st.subheader("📋 Resume Sections")

        # Handle both Pydantic and dict formats
        if hasattr(resume_data, 'sections'):
            if hasattr(resume_data.sections, 'model_dump'):
                sections = resume_data.sections.model_dump()
            else:
                sections = resume_data.sections.to_dict()
        else:
            sections = resume_data.get("sections", {})

        for section_name, section_content in sections.items():
            if section_content:  # Only show non-empty sections
                with st.expander(f"{section_name.replace('_', ' ').title()}"):
                    st.write(section_content)

def perform_full_analysis():
    """Perform full analysis when both job and resume data are available."""
    if not st.session_state.job_requirements or not st.session_state.resume_data:
        return

    try:
        components = get_components()

        # Compare resume to job
        comparison_results = components['matcher'].compare_resume_to_job(
            st.session_state.resume_data,
            st.session_state.job_requirements
        )
        st.session_state.comparison_results = comparison_results

        # Generate recommendations - handle both Pydantic and dict formats
        if hasattr(st.session_state.resume_data, 'raw_text'):
            resume_text = st.session_state.resume_data.raw_text
        else:
            resume_text = st.session_state.resume_data.get("raw_text", "")

        recommendations = components['generator'].generate_recommendations(
            resume_text,
            "",  # We already have job requirements analyzed
            comparison_results
        )
        st.session_state.recommendations = recommendations

        # Mark as complete
        st.session_state.analysis_complete = True

    except Exception as e:
        st.error(f"❌ Error during analysis: {str(e)}")

def show_settings_page():
    """Display the settings page."""
    st.header("⚙️ Settings")

    # Model configuration
    st.subheader("🤖 Model Configuration")

    model_name = st.selectbox(
        "LLM Model",
        ["llama3.2", "llama2", "codellama", "mistral"],
        help="Select the Ollama model to use for analysis"
    )

    temperature = st.slider(
        "Temperature",
        min_value=0.0,
        max_value=1.0,
        value=0.1,
        step=0.1,
        help="Controls randomness in model responses"
    )

    # Data management
    st.subheader("🗂️ Data Management")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("🗑️ Clear All Data"):
            st.session_state.clear()
            initialize_session_state()
            st.success("✅ All data cleared!")
            st.rerun()

    with col2:
        if st.button("📊 Show Debug Info"):
            st.subheader("Debug Information")
            st.json({
                "job_requirements_loaded": st.session_state.job_requirements is not None,
                "resume_data_loaded": st.session_state.resume_data is not None,
                "analysis_complete": st.session_state.analysis_complete,
                "session_keys": list(st.session_state.keys())
            })

    # About
    st.subheader("ℹ️ About")
    st.markdown("""
    **Resume Helper** is an AI-powered tool that helps job seekers tailor their resumes
    to specific job postings. It uses local processing to maintain privacy and provides
    specific, actionable recommendations.

    **Features:**
    - PDF resume parsing and analysis
    - Job description requirement extraction
    - Resume-job matching with scoring
    - Specific tailoring recommendations
    - Keyword suggestions
    - Privacy-focused local processing
    """)

if __name__ == "__main__":
    main()
