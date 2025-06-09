# Resume Helper

A tool to help job seekers tailor their resumes to specific job postings. This application analyzes your resume and a job description, identifies matches and gaps, and provides specific recommendations for improving your resume.

## Features

- **Resume Parsing**: Extract text and structure from PDF resume files
- **Job Description Analysis**: Process job posting text to identify key requirements and keywords
- **Resume Comparison**: Compare resume content against job description to identify matches and gaps
- **Recommendation Generation**: Create specific, actionable suggestions for improving your resume
- **User-Friendly Interface**: Simple GUI for uploading resumes and entering job descriptions

## Requirements

- Python 3.9 or higher
- Ollama with Llama 3 model installed
- Required Python packages (see requirements.txt)

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/yourusername/resume-helper.git
   cd resume-helper
   ```

2. Create and activate a virtual environment:
   ```
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

4. Ensure Ollama is installed and the Llama 3 model is available:
   ```
   # Check if Ollama is installed
   ollama --version
   
   # Pull the Llama 3 model if not already available
   ollama pull llama3
   ```

## Usage

1. Run the application:
   ```
   python main.py
   ```

2. In the application:
   - Click "Browse..." to select your resume PDF file
   - Enter or paste the job description in the text area
   - Click "Analyze and Generate Recommendations"
   - View the results in the "Results" tab
   - See detailed matches and gaps in the "Details" tab

## How It Works

1. **Resume Parsing**: The application extracts text from your PDF resume and identifies different sections (contact information, education, experience, skills, etc.).

2. **Job Description Analysis**: The application processes the job description to extract required skills, preferred skills, required experience, education requirements, and key responsibilities.

3. **Comparison**: The application compares your resume against the job requirements to identify matches and gaps.

4. **Recommendation Generation**: Based on the comparison results, the application generates specific recommendations for tailoring your resume to better match the job description.

## Project Structure

```
resume-helper/
├── app/
│   ├── parser/         # Resume parsing functionality
│   ├── analyzer/       # Job description analysis
│   ├── comparison/     # Resume-job comparison
│   ├── recommendation/ # Recommendation generation
│   ├── editor/         # (Future) Resume editing
│   └── exporter/       # (Future) PDF export
├── config/             # Configuration files
├── tests/              # Test cases
├── data/               # Sample data
│   ├── sample_resumes/
│   └── sample_job_descriptions/
├── docs/               # Documentation
├── main.py             # Main application entry point
├── requirements.txt    # Required packages
└── README.md           # This file
```

## Future Enhancements

- Resume editing functionality
- PDF export of tailored resume
- Support for DOCX resume files
- Resume version management
- Cover letter generation
- Integration with job search platforms

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
