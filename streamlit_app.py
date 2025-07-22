"""
Resume Helper - Streamlit Web Application

A modern web-based tool to help job seekers tailor their resumes to specific job postings.
This application provides an intuitive interface for uploading resumes, analyzing job descriptions,
and generating tailored recommendations with interactive visualizations.
"""

import streamlit as st
import time
import sys
import os
from pathlib import Path

# Add the project root to the path for imports
sys.path.append(str(Path(__file__).parent))

# Import our enhanced components
from app.analyzer.job_analyzer import JobAnalyzer
from app.models.responses import JobRequirements, ResumeData

# Configure the Streamlit page
st.set_page_config(
    page_title="Resume Helper",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'About': "# Resume Helper\nTailor your resume to match job descriptions with AI-powered analysis!"
    }
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        text-align: center;
        padding: 2rem 0;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 10px;
        margin-bottom: 2rem;
    }
    .metric-card {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid #667eea;
        margin: 0.5rem 0;
    }
    .recommendation-card {
        background: white;
        padding: 1rem;
        border-radius: 8px;
        border: 1px solid #dee2e6;
        margin: 0.5rem 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .priority-high {
        border-left: 4px solid #dc3545;
    }
    .priority-medium {
        border-left: 4px solid #ffc107;
    }
    .priority-low {
        border-left: 4px solid #28a745;
    }
</style>
""", unsafe_allow_html=True)


def init_session_state():
    """Initialize Streamlit session state variables."""
    if 'analyzer' not in st.session_state:
        st.session_state.analyzer = JobAnalyzer()
    if 'job_requirements' not in st.session_state:
        st.session_state.job_requirements = None
    if 'resume_data' not in st.session_state:
        st.session_state.resume_data = None
    if 'analysis_complete' not in st.session_state:
        st.session_state.analysis_complete = False


def main():
    """Main Streamlit application function."""
    init_session_state()
    
    # Header
    st.markdown("""
    <div class="main-header">
        <h1>📄 Resume Helper</h1>
        <p>Tailor your resume to match job descriptions with AI-powered analysis</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar for navigation and controls
    with st.sidebar:
        st.header("Navigation")
        page = st.radio(
            "Choose a section:",
            ["📊 Analysis", "📝 Job Requirements", "🎯 Resume Upload", "⚙️ Settings"]
        )
        
        st.divider()
        
        # Quick stats if analysis is complete
        if st.session_state.analysis_complete:
            st.success("✅ Analysis Complete!")
            if st.session_state.job_requirements:
                st.metric("Required Skills", len(st.session_state.job_requirements.required_skills))
                st.metric("Preferred Skills", len(st.session_state.job_requirements.preferred_skills))
                st.metric("Keywords", len(st.session_state.job_requirements.keywords))
    
    # Main content area based on selected page
    if page == "📊 Analysis":
        show_analysis_page()
    elif page == "📝 Job Requirements":
        show_job_requirements_page()
    elif page == "🎯 Resume Upload":
        show_resume_upload_page()
    elif page == "⚙️ Settings":
        show_settings_page()


def show_job_requirements_page():
    """Display the job requirements analysis page."""
    st.header("📝 Job Description Analysis")
    st.write("Enter a job description to analyze its requirements and extract key information.")
    
    # Job description input
    job_description = st.text_area(
        "Job Description",
        placeholder="Paste the job description here...",
        height=300,
        help="Enter the complete job description including requirements, responsibilities, and qualifications."
    )
    
    # Analysis button and processing
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        analyze_button = st.button("🔍 Analyze Job Description", use_container_width=True)
    
    if analyze_button and job_description.strip():
        with st.spinner("Analyzing job description..."):
            try:
                # Analyze the job description
                progress_bar = st.progress(0)
                progress_bar.progress(25, "Initializing analysis...")
                
                time.sleep(0.5)  # Simulate processing time
                progress_bar.progress(50, "Extracting requirements...")
                
                requirements = st.session_state.analyzer.analyze_job_description(job_description)
                
                progress_bar.progress(75, "Structuring results...")
                time.sleep(0.5)
                
                # Store results in session state
                st.session_state.job_requirements = requirements
                progress_bar.progress(100, "Analysis complete!")
                time.sleep(0.5)
                progress_bar.empty()
                
                st.success("✅ Job description analyzed successfully!")
                
                # Display results
                display_job_analysis_results(requirements)
                
            except Exception as e:
                st.error(f"❌ Error analyzing job description: {str(e)}")
    
    elif analyze_button and not job_description.strip():
        st.warning("⚠️ Please enter a job description to analyze.")
    
    # Display existing results if available
    elif st.session_state.job_requirements:
        st.info("📋 Showing previously analyzed job description")
        display_job_analysis_results(st.session_state.job_requirements)


def display_job_analysis_results(requirements: JobRequirements):
    """Display the job analysis results in a structured format."""
    st.subheader("🎯 Analysis Results")
    
    # Create tabs for different sections
    tab1, tab2, tab3, tab4 = st.tabs(["Skills", "Experience & Education", "Responsibilities", "Keywords"])
    
    with tab1:
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 🔴 Required Skills")
            if requirements.required_skills:
                for skill in requirements.required_skills:
                    st.markdown(f"• {skill}")
            else:
                st.info("No required skills identified")
        
        with col2:
            st.markdown("#### 🟡 Preferred Skills")
            if requirements.preferred_skills:
                for skill in requirements.preferred_skills:
                    st.markdown(f"• {skill}")
            else:
                st.info("No preferred skills identified")
    
    with tab2:
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 💼 Required Experience")
            if requirements.required_experience:
                for exp in requirements.required_experience:
                    st.markdown(f"• {exp}")
            else:
                st.info("No specific experience requirements identified")
        
        with col2:
            st.markdown("#### 🎓 Required Education")
            if requirements.required_education:
                for edu in requirements.required_education:
                    st.markdown(f"• {edu}")
            else:
                st.info("No specific education requirements identified")
    
    with tab3:
        st.markdown("#### 📋 Key Responsibilities")
        if requirements.responsibilities:
            for i, resp in enumerate(requirements.responsibilities, 1):
                st.markdown(f"{i}. {resp}")
        else:
            st.info("No specific responsibilities identified")
    
    with tab4:
        st.markdown("#### 🔍 ATS Keywords")
        if requirements.keywords:
            # Display keywords as tags
            keyword_cols = st.columns(4)
            for i, keyword in enumerate(requirements.keywords):
                with keyword_cols[i % 4]:
                    st.markdown(f"<span style='background-color: #e1f5fe; padding: 4px 8px; border-radius: 12px; margin: 2px; display: inline-block;'>{keyword}</span>", 
                               unsafe_allow_html=True)
        else:
            st.info("No specific keywords identified")


def show_analysis_page():
    """Display the main analysis dashboard."""
    st.header("📊 Resume Analysis Dashboard")
    
    if not st.session_state.job_requirements:
        st.warning("⚠️ Please analyze a job description first in the 'Job Requirements' section.")
        st.info("💡 Start by pasting a job description to extract requirements and keywords.")
    else:
        st.success("✅ Job requirements loaded! Upload a resume to begin comparison.")
        
        # Display quick overview
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Required Skills", len(st.session_state.job_requirements.required_skills))
        
        with col2:
            st.metric("Preferred Skills", len(st.session_state.job_requirements.preferred_skills))
        
        with col3:
            st.metric("Experience Items", len(st.session_state.job_requirements.required_experience))
        
        with col4:
            st.metric("Keywords", len(st.session_state.job_requirements.keywords))
        
        st.info("🎯 Next: Upload your resume in the 'Resume Upload' section to see how well it matches!")


def show_resume_upload_page():
    """Display the resume upload and parsing page."""
    st.header("🎯 Resume Upload & Analysis")
    st.write("Upload your resume (PDF format) to analyze how well it matches the job requirements.")
    
    if not st.session_state.job_requirements:
        st.warning("⚠️ Please analyze a job description first to enable resume comparison.")
        return
    
    # File upload
    uploaded_file = st.file_uploader(
        "Choose your resume file",
        type=['pdf'],
        help="Upload a PDF resume file for analysis"
    )
    
    if uploaded_file is not None:
        st.success(f"✅ Resume uploaded: {uploaded_file.name}")
        
        # Display file info
        st.info(f"📄 File size: {uploaded_file.size:,} bytes")
        
        # Process button
        if st.button("🔍 Analyze Resume Match", use_container_width=True):
            with st.spinner("Processing resume..."):
                st.info("🚧 Resume processing functionality coming soon!")
                st.write("This will include:")
                st.write("• PDF text extraction")
                st.write("• Resume section identification") 
                st.write("• Skills and experience matching")
                st.write("• Gap analysis and recommendations")
                st.write("• Match score calculation")


def show_settings_page():
    """Display the application settings page."""
    st.header("⚙️ Settings")
    
    st.subheader("🤖 AI Model Configuration")
    current_model = st.selectbox(
        "Ollama Model",
        ["qwen3:32b", "llama3", "mistral", "codellama"],
        index=0,
        help="Select the Ollama model to use for analysis"
    )
    
    if current_model != "qwen3:32b":
        st.warning("⚠️ Changing the model will require restarting the analysis.")
    
    st.subheader("📊 Display Options")
    show_debug = st.checkbox("Show debug information", value=False)
    show_raw_data = st.checkbox("Show raw analysis data", value=False)
    
    st.subheader("🔄 Reset Options")
    if st.button("🗑️ Clear All Data", type="secondary"):
        # Clear session state
        for key in ['job_requirements', 'resume_data', 'analysis_complete']:
            if key in st.session_state:
                del st.session_state[key]
        st.success("✅ All data cleared!")
        st.rerun()
    
    if show_debug and st.session_state.job_requirements:
        st.subheader("🐛 Debug Information")
        st.json(st.session_state.job_requirements.model_dump())


if __name__ == "__main__":
    main()
