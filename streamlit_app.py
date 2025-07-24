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
from app.parser.pdf_parser import ResumeParser
from app.analyzer.job_analyzer import JobAnalyzer
from app.comparison.matcher import ResumeMatcher
from app.recommendation.generator import RecommendationGenerator

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
        ["📊 Analysis", "📝 Job Requirements", "🎯 Resume Upload", "⚙️ Settings"]
    )
    
    # Main content based on selected page
    if page == "📊 Analysis":
        show_analysis_page()
    elif page == "📝 Job Requirements":
        show_job_requirements_page(components['analyzer'])
    elif page == "🎯 Resume Upload":
        show_resume_upload_page(components['parser'])
    elif page == "⚙️ Settings":
        show_settings_page()

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
