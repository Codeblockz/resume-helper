# Resume Tailor Project Brief

## Project Overview
The Resume Tailor is a web-based application that uses local large language models (Ollama) to automatically customize resumes for specific job postings. The goal is to help users optimize their resumes for Applicant Tracking Systems (ATS), improve keyword matching, and increase interview opportunities.

## Key Objectives
1. Replace the existing Streamlit implementation with a modern React frontend
2. Maintain the FastAPI backend architecture
3. Preserve existing Ollama integration while updating according to project specifications
4. Implement all core functionality outlined in the project prompt

## Technical Stack
- **Frontend**: React with Vite, TypeScript, Material-UI
- **Backend**: FastAPI, Python 3.10+
- **AI Integration**: Ollama (local LLM models)
- **Document Processing**: PyPDF2, pdfplumber, python-docx
- **Database**: SQLite for development, PostgreSQL for production

## Project Structure
```
resume-tailor/
├── backend/      # FastAPI backend services
│   ├── api/       # API endpoints
│   ├── models/    # Pydantic models
│   ├── services/  # Business logic
│   └── main.py    # Entry point
├── frontend/     # React frontend
│   ├── src/       # Source files
│   │   ├── components/
│   │   ├── pages/
│   │   └── theme.ts
│   ├── public/    # Static assets
│   └── package.json
└── memory-bank/  # Documentation and planning
```

## Implementation Plan

### Phase 1: Foundational Setup (Completed)
- ✅ Set up Vite project with proper configuration
- ✅ Create React components and routing structure
- ✅ Configure FastAPI backend with CORS
- ✅ Install all dependencies (frontend + backend)

### Phase 2: Core Functionality Implementation
1. **Resume Input Methods**
   - PDF, DOCX upload support
   - Manual resume entry form
   - Resume builder workflow

2. **Job Description Analysis**
   - Text area for job descriptions
   - URL import functionality
   - Key requirements extraction

3. **AI Tailoring Engine**
   - Ollama integration for resume optimization
   - Keyword matching and ATS optimization
   - Real-time content suggestions

4. **Results Presentation**
   - Side-by-side comparison view
   - Export to PDF, DOCX, TXT

### Phase 3: Advanced Features
- Multi-job management system
- Analytics dashboard
- Template library
- Batch processing capabilities

## Success Metrics
- ATS compatibility score improvement
- Increased keyword match percentage
- Positive user feedback on tailoring quality
- Fast response times (<30s for full tailoring)
