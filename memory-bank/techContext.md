# Technical Context: Resume Helper

## Technology Stack Overview

Resume Helper is a comprehensive web-based application designed to help job seekers tailor their resumes for specific job postings using AI-powered analysis. The project has been completely restarted and realigned according to the detailed specifications in `/home/ryan/FAFO/Resume Helper/projectPrompt.md`.

### Backend Framework
- **Primary Language**: Python 3.9+
- **API Framework**: FastAPI with asynchronous endpoints and proper routing
- **Environment Management**: Poetry for dependency management and environment isolation

### Document Processing
- **PDF Parsing**: PyPDF2, pdfplumber, or pdf-parse with Llama 3.1 assistance
- **DOCX Parsing**: python-docx integration (mammoth.js as fallback option)
- **Text Extraction**: Custom Python libraries for content analysis and section identification

### Database
- **Local Development**: SQLite for simplicity and ease of setup
- **Production Ready**: PostgreSQL support with proper migrations using Alembic
- **Data Storage**: Local file system with secure handling of resume files

### Frontend Framework
- **React**: Modern JavaScript framework for building the user interface
- **State Management**: Context API and hooks for efficient data flow
- **Routing**: React Router for SPA navigation patterns

### Dependencies and Tools
- **Package Management**: npm/yarn for frontend, Poetry for backend
- **Build Tools**: Vite for fast React development
- **Testing Frameworks**: Jest/Cypress for comprehensive test coverage

## Key Technical Components

### Ollama Integration
The core AI functionality relies on Ollama for natural language processing tasks:
- **Model Selection**: Dynamic selection based on task requirements with Llama 3.1 as default (Llama 3.1, Mistral, Code Llama)
- **API Communication**: Local API calls to maintain privacy and performance
- **Prompt Engineering**: Custom prompts for resume parsing, job analysis, and recommendation generation

### Resume Processing Pipeline
The system processes resumes through a multi-stage pipeline:
1. **Input Stage**: PDF/DOCX/TXT parsing or manual data entry with Pydantic validation
2. **Analysis Stage**: Section identification and content extraction using AI assistance
3. **Comparison Stage**: Matching resume content against job requirements
4. **Tailoring Stage**: Generating AI-powered recommendations
5. **Editing Stage**: User interface for applying changes with real-time feedback
6. **Export Stage**: Output in PDF, DOCX, or plain text formats

### Job Description Processing
Job postings are analyzed to extract key requirements:
- **Text Input**: Direct paste from job boards with markdown support
- **URL Import**: Fetching from popular job sites (LinkedIn, Indeed, Glassdoor) using web scraping
- **Requirement Extraction**: Skills, qualifications, experience levels, and keywords with AI assistance

## Advanced Features Under Development

### Multi-Job Management System
A database-backed system for tracking multiple resume versions:
- **Version Control**: Track changes across different job applications
- **Comparison Tools**: Side-by-side analysis of tailored resumes
- **Application Tracking**: Monitor status of each application with progress indicators

### Template Library
Industry-specific resume templates with ATS optimization:
- **Template Engine**: Dynamic generation based on user preferences and API configuration
- **Styling Options**: Customizable CSS/HTML components via React props
- **Best Practices**: Built-in compliance with ATS formatting requirements

### Batch Processing System
Efficient handling of multiple resumes and job descriptions:
- **Queue Management**: Process large batches efficiently using Celery/RabbitMQ
- **Parallel Execution**: Optimized for multi-core systems with async I/O
- **Progress Tracking**: Real-time status updates via WebSocket integration

## Performance Optimization Strategies

### LLM Response Time
Optimizing AI model usage for faster responses:
- **Prompt Caching**: Store common prompt patterns in Redis cache
- **Model Selection**: Dynamic balancing of capability and speed requirements
- **Streaming Support**: Real-time response updates using WebSockets for better UX

### Database Efficiency
Efficient data storage and retrieval:
- **Indexing Strategies**: Optimize query performance with SQLAlchemy indexes
- **Caching Layer**: Frequently accessed resume versions stored in Redis
- **Connection Pooling**: Manage database connections efficiently using async drivers

## Security & Privacy Considerations

### Data Protection
Local processing ensures user privacy:
- **No Cloud Storage**: Sensitive data never leaves the local system
- **Secure File Handling**: Proper cleanup of temporary files using background tasks
- **User Consent**: Explicit permission for any data retention via authentication flow

### Access Control
System security measures:
- **Authentication System**: JWT-based user login and session management
- **Rate Limiting**: Prevent API abuse with FastAPI middleware
- **Data Encryption**: Secure storage of user preferences using environment variables

## Development Workflow

### Version Control
Git-based development with branch strategy:
- **Main Branch**: Production-ready code with detailed commit history
- **Feature Branches**: Isolated development for new features and bug fixes
- **Release Candidates**: Testing and QA before merges to main

### Continuous Integration
Automated testing and deployment:
- **Unit Tests**: Core functionality validation using pytest
- **Integration Tests**: End-to-end workflow testing with Playwright
- **Performance Benchmarks**: Response time monitoring and optimization

### Code Quality
Maintaining high standards through:
- **Linting & Formatting**: ESLint/Prettier for frontend, Black/Ruff for Python
- **Type Checking**: TypeScript for React components, Mypy for Python
- **Code Reviews**: Peer review process for all changes with detailed PR templates

## Project Structure Overview

```
/resume-helper/
├── backend/               # FastAPI backend
│   ├── app/               # Core application modules
│   ├── api/               # API endpoints
│   ├── core/              # Configuration and dependencies
│   ├── models/            # Database models (SQLAlchemy)
│   ├── services/          # Business logic services
│   ├── tests/             # Backend unit tests
│   ├── main.py            # FastAPI entry point
│   └── requirements.txt   # Python dependencies
├── frontend/              # React frontend
│   ├── public/            # Static assets (images, favicon)
│   ├── src/               # Source code
│   │   ├── api/           # API service layer for frontend
│   │   ├── components/    # UI components
│   │   ├── contexts/      # Context providers and hooks
│   │   ├── pages/         # Route components
│   │   ├── styles/        # CSS and styling
│   │   ├── utils/         # Utility functions
│   │   └── App.tsx       # Main React app component
│   ├── .env               # Environment variables
│   ├── vite.config.ts    # Vite configuration
│   ├── package.json      # Node dependencies
│   └── tsconfig.json     # TypeScript config
├── docs/                  # Documentation
└── README.md              # Project overview

```

This technical context document provides a comprehensive overview of the Resume Helper technology stack and development approach. It will be continuously updated to reflect new implementations and architectural decisions as the project evolves.
