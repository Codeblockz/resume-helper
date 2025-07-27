import React from 'react';
import { Container, Typography, Box, Paper, List, ListItem, ListItemText } from '@mui/material';

const AnalysisResultsPage: React.FC = () => {
  // This would be populated from API response in a real app
  const sampleData = {
    resumeScore: 85,
    jobMatchPercentage: 72,
    improvementsSuggested: [
      "Add 'Python' to skills section",
      "Highlight AWS experience",
      "Reorder sections to emphasize relevant experience",
      "Update certifications list"
    ],
    keywordsAnalysis: {
      matched: ["Python", "Web Development", "API Design"],
      missing: ["Django", "Microservices"]
    },
    tailoredResumePreview: `John Doe
Software Developer | Python Specialist

Experience:
- Senior Software Engineer, TechCorp (2018-Present)
  - Led development of high-traffic web services using Python and Django
  - Implemented microservices architecture for scalability
  - ...

Skills:
- Python 3.x
- Web Development (Django, Flask)
- AWS Certified Developer`
  };

  return (
    <Container maxWidth="lg">
      <Box sx={{ mt: 4 }}>
        <Typography variant="h4" gutterBottom>
          Resume Analysis Results
        </Typography>

        <Paper elevation={3} sx={{ p: 3, mb: 4 }}>
          <Typography variant="h6">Overall Assessment</Typography>
          <List>
            <ListItem>
              <ListItemText
                primary="Resume Quality Score"
                secondary={`${sampleData.resumeScore}/100`}
              />
            </ListItem>
            <ListItem>
              <ListItemText
                primary="Job Match Percentage"
                secondary={`${sampleData.jobMatchPercentage}%`}
              />
            </ListItem>
          </List>
        </Paper>

        <Paper elevation={3} sx={{ p: 3, mb:4 }}>
          <Typography variant="h6">Improvements Suggested</Typography>
          <List>
            {sampleData.improvementsSuggested.map((suggestion, index) => (
              <ListItem key={index}>
                <ListItemText primary={`• ${suggestion}`} />
              </ListItem>
            ))}
          </List>
        </Paper>

        <Paper elevation={3} sx={{ p: 3, mb:4 }}>
          <Typography variant="h6">Keyword Analysis</Typography>
          <Box sx={{ display: 'flex', gap: 2 }}>
            <Box flex={1}>
              <Typography variant="subtitle1" gutterBottom>Matched Keywords</Typography>
              {sampleData.keywordsAnalysis.matched.map((keyword, index) => (
                <Box key={index} sx={{ display: 'inline-block', mr: 1, mb: 1, px: 2, py: 0.5, bgcolor: '#e8f5e9', color: '#4caf50' }}>
                  {keyword}
                </Box>
              ))}
            </Box>
            <Box flex={1}>
              <Typography variant="subtitle1" gutterBottom>Missing Keywords</Typography>
              {sampleData.keywordsAnalysis.missing.map((keyword, index) => (
                <Box key={index} sx={{ display: 'inline-block', mr: 1, mb: 1, px: 2, py: 0.5, bgcolor: '#ffebee', color: '#d32f2f' }}>
                  {keyword}
                </Box>
              ))}
            </Box>
          </Box>
        </Paper>

        <Paper elevation={3} sx={{ p: 3 }}>
          <Typography variant="h6">Tailored Resume Preview</Typography>
          <pre style={{ whiteSpace: 'pre-wrap', overflowX: 'auto' }}>{sampleData.tailoredResumePreview}</pre>
        </Paper>
      </Box>
    </Container>
  );
};

export default AnalysisResultsPage;
