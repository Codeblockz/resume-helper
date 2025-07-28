import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { Button, Typography, Container, Box, TextField, CircularProgress, Alert, Select, MenuItem, FormControl, InputLabel, SelectChangeEvent } from '@mui/material';
import { useWorkflow, setResumeData, setAnalysisResult } from '../contexts/ResumeTailorContext';

const ResumeEditorPage: React.FC = () => {
  // State for managing editor content and UI
  const [sections, setSections] = useState<{ [key: string]: string }>({});
  const [currentSection, setCurrentSection] = useState<string>('');
  const [editedContent, setEditedContent] = useState<string>('');
  const [message, setMessage] = useState<string | null>(null);
  const [loading, setLoading] = useState<boolean>(false);

  const { state, dispatch } = useWorkflow();
  const navigate = useNavigate();

  // Load sample resume data when component mounts
  useEffect(() => {
    // In a real app, this would load from the backend API
    if (!state.resumeData) {
      const sampleResume = `=== Contact Information ===
John Doe
john.doe@example.com
(123) 456-7890

=== Summary ===
Highly skilled software engineer with over 5 years of experience in web development.

=== Skills ===
Python
Django
Flask
JavaScript
AWS

=== Experience ===
Senior Software Engineer, TechCorp (2018-Present)
- Led development of high-traffic web services using Python and Django
- Implemented microservices architecture for scalability`;

      // Parse the sample resume into sections
      const parsedSections = parseResume(sampleResume);
      setSections(parsedSections);

      if (Object.keys(parsedSections).length > 0) {
        setCurrentSection(Object.keys(parsedSections)[0]);
        setEditedContent(parsedSections[Object.keys(parsedSections)[0]]);
      }
    } else {
      // Use resume data from context
      const { content, sections: savedSections } = state.resumeData;
      setSections(savedSections || parseResume(content));
      if (savedSections && Object.keys(savedSections).length > 0) {
        setCurrentSection(Object.keys(savedSections)[0]);
        setEditedContent(savedSections[Object.keys(savedSections)[0]]);
      }
    }
  }, [state.resumeData]);

  // Parse resume text into sections
  const parseResume = (resumeText: string): { [key: string]: string } => {
    const sections: { [key: string]: string } = {};
    const lines = resumeText.split('\n');

    let currentSection = '';
    let contentLines: string[] = [];

    for (const line of lines) {
      if (line.startsWith('=== ')) {
        // Save previous section
        if (currentSection && contentLines.length > 0) {
          sections[currentSection] = contentLines.join('\n');
        }

        // Start new section
        currentSection = line.substring(3, line.length - 3);
        contentLines = [];
      } else {
        contentLines.push(line);
      }
    }

    // Add last section
    if (currentSection && contentLines.length > 0) {
      sections[currentSection] = contentLines.join('\n');
    }

    return sections;
  };

  const handleSectionChange = (event: SelectChangeEvent<string>) => {
    const newSection = event.target.value as string;
    setCurrentSection(newSection);
    if (sections[newSection]) {
      setEditedContent(sections[newSection]);
    }
  };

  const handleContentChange = (event: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    setEditedContent(event.target.value);
  };

  const handleSaveAndAnalyze = async () => {
    if (!currentSection) return;

    try {
      setLoading(true);

      // Save resume data to context
      dispatch(setResumeData({
        content: Object.values(sections).join('\n\n'),
        sections
      }));

      // Call backend for analysis (simulated)
      const isLocalhost = typeof window !== 'undefined' && window.location.hostname === 'localhost';
      const apiUrl = isLocalhost ? 'http://localhost:8010/api/analyze-resume' : '/api/analyze-resume';

      // Simulate API call with sample data for now
      await new Promise(resolve => setTimeout(resolve, 500));

      const sampleAnalysisResult = {
        resumeScore: 85,
        jobMatchPercentage: 72,
        improvementsSuggested: [
          "Add 'Python' to skills section",
          "Highlight AWS experience",
          "Reorder sections to emphasize relevant experience"
        ],
        keywordsAnalysis: {
          matched: ["Python", "Web Development"],
          missing: ["Django"]
        },
        tailoredResumePreview: editedContent + "\n\n-- Tailored by Resume Tailor --\n\nKey Improvements:\n- Added job-specific keywords\n- Emphasized relevant experience"
      };

      // Save analysis result to context
      dispatch(setAnalysisResult(sampleAnalysisResult));

      navigate('/analysis-results');
    } catch (error) {
      setMessage('Failed to analyze resume. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <Container maxWidth="lg">
      <Box sx={{ mt: 4, p: 4 }}>
        <Typography variant="h4" gutterBottom>
          Resume Editor
        </Typography>

        {message && (
          <Alert severity={message.includes('successfully') ? 'success' : 'error'} sx={{ mb: 3 }}>
            {message}
          </Alert>
        )}

        <Box sx={{ display: 'flex', gap: 4, mb: 4 }}>
          {/* Section selector */}
          <FormControl fullWidth>
            <InputLabel>Section</InputLabel>
            <Select
              value={currentSection}
              onChange={handleSectionChange}
              label="Section"
            >
              {Object.keys(sections).map((sectionName) => (
                <MenuItem key={sectionName} value={sectionName}>
                  {sectionName}
                </MenuItem>
              ))}
            </Select>
          </FormControl>

          {/* Save and analyze button */}
          <Button
            variant="contained"
            color="primary"
            onClick={handleSaveAndAnalyze}
            disabled={!currentSection || loading}
          >
            {loading ? <CircularProgress size={24} /> : 'Analyze & Get Results'}
          </Button>
        </Box>

        {/* Content editor */}
        <TextField
          label={`Edit ${currentSection}`}
          value={editedContent}
          onChange={handleContentChange}
          multiline
          rows={15}
          fullWidth
          sx={{ mb: 3 }}
        />

        {/* Preview section */}
        <Box sx={{
          p: 2,
          border: '1px solid #ddd',
          borderRadius: 1,
          bgColor: '#f8f9fa'
        }}>
          <Typography variant="h6" gutterBottom>
            Live Preview
          </Typography>
          <pre style={{ whiteSpace: 'pre-wrap', overflowX: 'auto' }}>{editedContent}</pre>
        </Box>
      </Box>
    </Container>
  );
};

export default ResumeEditorPage;
