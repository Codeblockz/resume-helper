import React, { useState, useEffect } from 'react';
import { Button, Typography, Container, Box, TextField, CircularProgress, Alert, Select, MenuItem, FormControl, InputLabel, SelectChangeEvent } from '@mui/material';

const ResumeEditorPage: React.FC = () => {
  // State for managing editor content and UI
  const [sections, setSections] = useState<{ [key: string]: string }>({});
  const [currentSection, setCurrentSection] = useState<string>('');
  const [editedContent, setEditedContent] = useState<string>('');
  const [message, setMessage] = useState<string | null>(null);
  const [loading, setLoading] = useState<boolean>(false);

  // Load sample resume data when component mounts
  useEffect(() => {
    // In a real app, this would load from the backend API
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
  }, []);

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

  const handleSave = () => {
    if (!currentSection) return;

    setLoading(true);

    try {
      // In a real app, this would call the backend API to save changes
      const updatedSections = { ...sections, [currentSection]: editedContent };
      setSections(updatedSections);
      setMessage('Changes saved successfully!');
    } catch (error) {
      setMessage('Failed to save changes. Please try again.');
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

          {/* Save button */}
          <Button
            variant="contained"
            color="primary"
            onClick={handleSave}
            disabled={!currentSection || loading}
          >
            {loading ? <CircularProgress size={24} /> : 'Save Changes'}
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
