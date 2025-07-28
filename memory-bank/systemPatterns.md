# System Architecture: Resume Helper

## Overview Diagram

```mermaid
graph TD
    A[User Interface] -->|1. Upload/Input Resume| B[Resume Input Module]
    A -->|2. Enter Job Description| C[Job Analysis Module]

    subgraph Backend Services
        B -->|3. Parse & Analyze| D[Resume Parser]
        C -->|4. Extract Requirements| E[Job Description Processor]

        D -->|5. Identify Sections| F[Resume Data Model (Pydantic)]
        E -->|6. Map Keywords/Skills| G[Job Requirements Model (Pydantic)]

        F -->|7. Compare Content| H[Comparison Engine]
        G -->|8. Match Requirements| H

        H -->|9. Generate Recommendations| I[AI Tailoring Module]
    end

    subgraph User Interaction
        A -->|10. View Results| J[Results Display]
        A -->|11. Edit Resume| K[Rich Text Editor]

        K -->|12. Apply Changes| L[Resume Editor Controller]
        L -->|13. Save Drafts| M[Version Control System]
    end

    subgraph Export Pipeline
        L -->|14. Export Final Version| N[Export Manager]
        N -->|15. PDF/DOCX/TXT| O[Output Formatter]
        N -->|16. Apply Templates| P[Template Engine]

        O -->|17. Return Output| A
    end

    subgraph Supporting Systems
        Q[Configuration Database] --> B
        Q --> C
        Q --> H
        Q --> I
        Q --> N

        R[Analytics Dashboard] --> J
        S[User Authentication] --> A
        T[Multi-Job Manager] --> M
    end
```

## Core System Components

### 1. Resume Input Module (FastAPI)
**Purpose**: Handle all resume input methods (PDF, DOCX, manual entry, guided builder)
- **PDF Parsing**: Extract text and sections using PyPDF2/pdfplumber with Llama 3.1 assistance
- **DOCX Support**: Parse Word documents with python-docx/mammoth.js integration
- **Manual Entry**: Structured form-based data collection with Pydantic validation
- **Guided Builder**: Step-by-step resume creation workflow

### 2. Job Analysis Module (FastAPI)
**Purpose**: Process job descriptions to extract requirements and keywords
- **Text Input**: Direct paste functionality
- **URL Import**: Fetch from LinkedIn, Indeed, Glassdoor using web scraping
- **Requirement Extraction**: Skills, qualifications, experience levels with AI assistance

### 3. Resume Data Model (Pydantic)
**Purpose**: Structured representation of resume content and metadata
- **Sections**: Contact info, summary, education, experience, skills, etc.
- **Formatting**: Style information from original document preserved for export
- **Version History**: Track changes across edits

### 4. Job Requirements Model (Pydantic)
**Purpose**: Structured representation of job description analysis results
- **Skills Categories**: Required vs. preferred
- **Experience Levels**: Years required, specific roles
- **Education Requirements**: Degree types and institutions
- **Keyword Lists**: Important phrases for ATS matching

### 5. Comparison Engine (FastAPI)
**Purpose**: Match resume content against job requirements
- **Section Mapping**: Align resume sections with job categories
- **Skill Matching**: Identify relevant skills in resume text using AI
- **Gap Analysis**: Find missing requirements and suggest additions
- **Scoring System**: Calculate overall match percentage

### 6. AI Tailoring Module (FastAPI + Ollama)
**Purpose**: Generate intelligent recommendations using local LLM models
- **Keyword Optimization**: Suggest content additions to match job keywords naturally
- **Achievement Quantification**: Recommend metrics for impact statements
- **ATS Formatting**: Ensure proper structure and keyword density
- **Content Reordering**: Prioritize most relevant sections

### 7. Rich Text Editor (React)
**Purpose**: User interface for applying AI recommendations
- **Section-Based Editing**: Edit individual resume components
- **Style Preservation**: Maintain original formatting while applying changes
- **Side-by-Side View**: Compare original vs. tailored versions in real-time
- **Real-time Feedback**: Show match score as edits are made

### 8. Version Control System (FastAPI + Database)
**Purpose**: Track multiple resume versions for different job applications
- **Version History**: Store previous iterations of each resume
- **Comparison Tools**: Side-by-side analysis of different versions
- **Job-Specific Tailoring**: Manage tailored resumes per application

### 9. Export Manager (FastAPI)
**Purpose**: Generate final resume outputs in various formats
- **PDF Export**: Professional formatting with ATS optimization using weasyprint or wkhtmltopdf
- **DOCX Support**: Editable Word documents for further customization
- **Plain Text**: Simple format for easy editing
- **Template Engine**: Apply industry-specific styles and layouts

## Advanced System Features

### Multi-Job Management System (FastAPI + Database)
**Purpose**: Handle multiple job applications efficiently
- **Batch Processing**: Process large sets of resumes/job descriptions
- **Queue Management**: Optimize system resource usage with Celery/RabbitMQ
- **Progress Tracking**: Real-time status updates via WebSocket

### Analytics Dashboard (React + FastAPI)
**Purpose**: Provide insights into application success and resume effectiveness
- **Keyword Effectiveness**: Track which keywords lead to interviews
- **ATS Compatibility**: Monitor how often resumes pass filters
- **Conversion Rates**: Measure interview success from optimized resumes

## Integration Patterns

### LLM Model Selection (Ollama)
Dynamic model choice based on task requirements with Llama 3.1 as the default:
- **Llama 3.1**: General purpose resume analysis and tailoring (default)
- **Mistral**: Specialized in technical skill identification
- **Code Llama**: Best for parsing complex document structures

### Template System (FastAPI + React)
Industry-specific resume formatting with ATS optimization:
- **Template Engine**: Generate resumes based on user preferences
- **Customizable Styles**: Adjust colors, fonts, and layouts via API
- **ATS Compliance**: Built-in best practices for applicant tracking systems

## Security & Privacy Patterns

### Local Processing Advantage (FastAPI + Ollama)
- **No Cloud Storage**: Sensitive data never leaves the local system
- **Secure File Handling**: Proper cleanup of temporary files using background tasks
- **User Consent**: Explicit permission for any data retention via authentication system

### Data Protection Measures
- **Encryption**: Secure storage of user preferences and templates with environment variables
- **Access Control**: User authentication and JWT session management
- **Rate Limiting**: Prevent API abuse from external sources using FastAPI middleware

## Performance Optimization Strategies (FastAPI + Celery)

### LLM Response Time
Improving AI model usage efficiency:
- **Prompt Caching**: Store common prompt patterns for reuse with Redis caching
- **Model Selection**: Balance capability with speed requirements dynamically
- **Streaming Support**: Real-time response updates via WebSocket

### Database Efficiency (SQLite/PostgreSQL)
Optimizing data storage and retrieval:
- **Indexing Strategies**: Optimize query performance for common operations
- **Caching Layer**: Frequently accessed resume versions with Redis
- **Connection Pooling**: Manage database connections efficiently using SQLAlchemy

## Development Patterns (FastAPI + React)

### Modular Architecture
Separation of concerns across system components:
- **Microservices Approach**: Independent modules with clear APIs
- **Loose Coupling**: Easy replacement or upgrading of individual components
- **Interface Consistency**: Standardized data models and communication patterns

### Testing Strategy
Comprehensive validation framework:
- **Unit Tests**: Core functionality isolation and validation using pytest
- **Integration Tests**: End-to-end workflow testing with pytest and Playwright
- **Performance Benchmarks**: Response time monitoring and optimization

## Frontend Architecture (React)

### Component Hierarchy
Organized React component structure:
```
src/
├── components/       # Reusable UI components
│   ├── Editor.js     # Main editor interface
│   ├── Upload.js      # File upload component
│   └── Analysis.js    # Job analysis display
├── pages/            # Page-level components
│   ├── Dashboard.js  # Main application dashboard
│   └── EditorPage.js # Editor workspace page
├── services/         # API integration layer
│   ├── apiClient.js  # Axios/Fetch wrapper for FastAPI calls
│   └── auth.js       # Authentication service
└── App.js            # Root React component
```

### State Management
Efficient data flow using React context and hooks:
- **User Context**: Authentication state and preferences
- **Editor Context**: Resume editing state management
- **Analysis Context**: Job analysis results and recommendations

This system architecture document provides a comprehensive overview of the Resume Helper's technical design, integration patterns, and development approach. It will be continuously updated to reflect new implementations and architectural decisions as the project evolves.
