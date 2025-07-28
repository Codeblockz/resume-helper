# Resume Tailor App

AI-powered resume tailoring and job analysis platform.

## Project Overview

Resume Tailor is an application designed to help job seekers optimize their resumes for specific job opportunities. The app features:

- **React frontend**: Modern, responsive user interface built with React and Vite
- **FastAPI backend**: Robust RESTful API using FastAPI
- **AI integration**: Ollama-powered resume tailoring and analysis

## Project Structure

```
resume-tailor/
├── backend/          # Backend services (FastAPI)
│   ├── api/         # API endpoints
│   ├── config/      # Configuration files
│   ├── core/        # Core services
│   ├── models/      # Data models
│   └── services/    # Business logic
└── frontend/        # Frontend application (React + Vite)
    ├── public/      # Static assets
    └── src/         # Source code
```

## Setup Instructions

### Backend Requirements

```bash
cd backend
pip install -r requirements.txt
```

Create a `.env` file with:

```
API_HOST=0.0.0.0
API_PORT=8000
DATABASE_URL=sqlite:///./data/resume_tailor.db
OLLAMA_API_KEY=your_ollama_api_key_here
```

### Frontend Requirements

```bash
cd frontend
npm install
```

## Development with Docker (Recommended)

The easiest way to run the application is using Docker Compose, which sets up both services with proper networking and configuration.

### Prerequisites

- [Docker](https://www.docker.com/) installed on your machine
- [Docker Compose](https://docs.docker.com/compose/) (usually included with Docker)

### First-time setup

1. Create a `.env` file in the `backend` directory with:

```bash
cd backend
cp .env.example .env
```

2. Update environment variables as needed

### Running the application

To start both frontend and backend services:

```bash
docker-compose up --build
```

This will:
- Build Docker images for both frontend and backend
- Start containers on ports 3000 (frontend) and 8000 (backend)
- Enable live reloading for development

### Accessing the application

- Frontend: http://localhost:3000
- Backend API documentation: http://localhost:3000/docs (proxy through frontend)

## Development without Docker

If you prefer to run services manually:

### Backend Requirements

```bash
cd backend
pip install -r requirements.txt
```

Create a `.env` file with:

```
API_HOST=0.0.0.0
API_PORT=8000
DATABASE_URL=sqlite:///./data/resume_tailor.db
OLLAMA_API_KEY=your_ollama_api_key_here
```

### Frontend Requirements

```bash
cd frontend
npm install
```

Start backend API:

```bash
cd backend
uvicorn main:app --reload
```

Start frontend development server:

```bash
cd frontend
npm run dev
```

## Features

- Resume upload and parsing (PDF, DOCX, TXT)
- Job description analysis
- AI-powered resume tailoring
- Keyword matching and optimization
- User-friendly interface with real-time feedback

## Deployment

To build and serve the production version:

```bash
# Build frontend
cd frontend
npm run build

# Copy frontend to backend static directory
cp -r dist/ ../backend/static/
```

Start the FastAPI app in production mode:

```bash
cd backend
uvicorn main:app --host 0.0.0.0 --port 8000
```

## API Documentation

Swagger UI is available at `/docs` when running the backend server.

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/your-feature`)
3. Commit your changes (`git commit -am 'Add some feature'`)
4. Push to the branch (`git push origin feature/your-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License.