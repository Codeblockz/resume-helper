# Test-Driven Development (TDD) Task Breakdown: Resume Input Methods

## Feature Overview
Implement three methods for users to input their resumes into the system:
1. **Upload existing resume**: Support PDF, DOCX, and TXT formats
2. **Manual entry form**: Structured data input with validation
3. **Guided resume builder**: Step-by-step creation from scratch

## Development Phases

### Phase 0: Preparation (Pre-TDD)
- ✅ Set up testing framework (Jest + React Testing Library for frontend, pytest for backend)
- ✅ Create mock data for resumes in different formats
- ✅ Set up API endpoints for resume upload and processing

### Phase 1: Upload Existing Resume

#### Test Cases
**Frontend Tests:**
```javascript
// FileUpload.test.tsx
describe('Resume Upload Component', () => {
  test('should accept PDF, DOCX, and TXT files', async () => {
    // Mock file inputs for different formats
    const pdfFile = new File(['pdf content'], 'resume.pdf', { type: 'application/pdf' });
    const docxFile = new File(['docx content'], 'resume.docx', { type: 'application/vnd.openxmlformats-officedocument.wordprocessingml.document' });
    const txtFile = new File(['txt content'], 'resume.txt', { type: 'text/plain' });

    // Render component and test file acceptance
  });

  test('should show error for unsupported formats', async () => {
    // Mock unsupported file format
    const mp4File = new File(['video content'], 'unacceptable.mp4', { type: 'video/mp4' });
  });

  test('should display loading state during upload', async () => {
    // Mock slow response to test loading state
  });
});

**Backend Tests:**
```python
# test_upload_api.py
def test_upload_resume_pdf():
    # Test PDF parsing endpoint

def test_upload_resume_docx():
    # Test DOCX parsing endpoint

def test_upload_resume_txt():
    # Test TXT parsing endpoint

def test_file_format_validation():
    # Test that unsupported formats are rejected
```

#### Development Steps
1. **Frontend Implementation:**
   - Create `FileUpload` component with drag-and-drop support
   - Add file format validation (PDF, DOCX, TXT only)
   - Implement API integration for file upload

2. **Backend Implementation:**
   - Create `/upload/resume` endpoint in FastAPI
   - Implement file parsing logic:
     - PDF: Use PyPDF2 and pdfplumber
     - DOCX: Use python-docx
     - TXT: Simple text reading
   - Add temporary file storage solution

### Phase 2: Manual Entry Form

#### Test Cases
**Frontend Tests:**
```javascript
// ManualEntryForm.test.tsx
describe('Manual Resume Entry', () => {
  test('should validate required fields', async () => {
    // Test form validation for empty fields
  });

  test('should display real-time character count', async () => {
    // Test experience section character limit
  });

  test('should handle special characters in input', async () => {
    // Test for proper encoding/decoding
  });
});

**Backend Tests:**
```python
# test_manual_entry_api.py
def test_manual_entry_validation():
    # Test required field validation

def test_manual_entry_storage():
    # Test that submitted data is properly stored
```

#### Development Steps
1. **Frontend Implementation:**
   - Create multi-step form with sections: Contact Info, Summary, Experience, Skills, Education
   - Add form validation and real-time feedback
   - Implement API integration for form submission

2. **Backend Implementation:**
   - Create `/upload/manual` endpoint in FastAPI
   - Implement data validation and storage
   - Develop structured resume model using Pydantic

### Phase 3: Guided Resume Builder

#### Test Cases
**Frontend Tests:**
```javascript
// ResumeBuilder.test.tsx
describe('Guided Resume Builder', () => {
  test('should guide users through steps', async () => {
    // Test navigation between builder steps
  });

  test('should save progress', async () => {
    // Test local storage or backend session saving
  });

  test('should provide contextual help', async () => {
    // Test tooltip and hint functionality
  });
});

**Backend Tests:**
```python
# test_resume_builder_api.py
def test_builder_progress_storage():
    # Test progress tracking endpoint

def test_builder_suggestions():
    # Test AI-powered content suggestions
```

#### Development Steps
1. **Frontend Implementation:**
   - Create step-by-step builder with clear progression indicators
   - Add context-sensitive help and tips
   - Implement progress saving and recovery

2. **Backend Implementation:**
   - Create `/builder` endpoint group in FastAPI
   - Develop AI-powered content suggestions using Ollama
   - Implement session-based progress tracking

### Phase 4: Integration & Testing

#### Cross-Component Tests:
```javascript
// Integration.test.tsx
describe('Resume Input Methods Integration', () => {
  test('should properly route to analysis page after successful upload', async () => {
    // Test file upload -> analysis flow
  });

  test('should validate all input methods equally', async () => {
    // Ensure consistent data structure from all input sources
  });
});
```

#### API Testing:
```python
# test_integration.py
def test_all_input_methods_produce_valid_resume_data():
    # Test that all three methods produce comparable resume objects

def test_end_to_end_workflow():
    # Test complete workflow: input -> analysis -> tailoring -> output
```

## Deployment Considerations
- Load testing for file upload endpoints
- Security reviews for file handling
- Cross-browser compatibility testing
- Mobile responsiveness verification

## Timeline Estimate
| Phase | Estimated Time |
|-------|---------------|
| Preparation | 1 day |
| Upload Existing Resume | 3 days |
| Manual Entry Form | 2 days |
| Guided Resume Builder | 4 days |
| Integration & Testing | 3 days |
| **Total** | **13 days** |

This TDD task breakdown provides a comprehensive roadmap for implementing the resume input methods feature while ensuring high code quality through thorough testing at each stage.
