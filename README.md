# Resume Tailor App

A comprehensive web-based application that uses AI-powered analysis to help job seekers tailor their resumes for specific job postings. The app optimizes resumes for Applicant Tracking Systems (ATS) and increases interview opportunities.

## Core Features

### 1. Resume Input Methods
- **Upload existing resume**: Support for PDF, DOCX, and TXT formats
- **Manual entry**: Structured form for inputting resume details
- **Resume builder**: Step-by-step guided creation from scratch

### 2. Job Description Analysis
- **Job posting input**: Text area for pasting job descriptions
- **URL import**: Fetch job postings from popular job sites
- **Requirement extraction**: Identify essential skills, qualifications, and keywords

### 3. AI-Powered Resume Tailoring
- **Keyword optimization**: Match resume content with job description keywords
- **Skills alignment**: Emphasize relevant skills and experiences
- **ATS optimization**: Ensure proper formatting and keyword density
- **Content suggestions**: Recommend additions, modifications, or reordering

## Technology Stack

### Backend
- **Framework**: FastAPI (Python)
- **Database**: SQLite for local development, PostgreSQL ready
- **AI Integration**: Ollama with dynamic model selection (Llama 3.1, Mistral, Code Llama)

### Frontend
- **Framework**: React with Vite
- **State Management**: Context API and hooks
- **Routing**: React Router

## Requirements

### Backend
- Python 3.9+
- Required packages (see `backend/requirements.txt`)
- Ollama installed and running locally

### Frontend
- Node.js v18+ (for Vite)
- Required packages (see `frontend/package.json`)

## Installation

1. **Clone the repository**:
   ```
   git clone https://github.com/Codeblockz/resume-tailor.git
   cd resume-tailor
   ```

2. **Set up backend environment**:
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Set up frontend environment**:
   ```bash
   cd frontend
   npm install  # or yarn install
   ```

4. **Ensure Ollama is installed and models are available**:
   ```bash
   ollama --version
   ollama pull llama3.1
   ollama pull mistral:v0.3
   ```

## Usage

### Development Mode

**Backend**: Start the FastAPI server:
```bash
cd backend
source venv/bin/activate  # On Windows: venv\Scripts\activate
uvicorn main:app --reload
```

**Frontend**: Launch the React development server:
```bash
cd frontend
npm run dev  # or yarn dev
```

### Production Mode

To be documented...

## Project Structure

```
resume-tailor/
├── backend/               # FastAPI backend services
│   ├── app/               # Core application modules
│   ├── api/               # API endpoints
│   ├── core/              # Configuration and dependencies
│   ├── models/            # Database models (SQLAlchemy)
│   ├── services/          # Business logic services
│   ├── tests/             # Backend unit tests
│   ├── main.py            # FastAPI entry point
│   └── requirements.txt   # Python dependencies
├── frontend/              # React frontend application
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

## Development Phases

### Phase 1: MVP (Target: 4-6 weeks)
- Basic resume upload and parsing functionality
- Simple job description input interface
- Core Ollama integration for AI-powered tailoring
- PDF export capability

### Phase 2: Enhancement (Target: 3-4 weeks)
- Advanced ATS optimization features
- Improved UI/UX design with modern components
- Multiple export format support (DOCX, plain text)
- Basic analytics dashboard

### Phase 3: Advanced Features (Target: 4-5 weeks)
- Multi-job management system for tracking applications
- Industry-specific resume template library
- Batch processing capabilities
- Performance optimization and response time improvements

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
