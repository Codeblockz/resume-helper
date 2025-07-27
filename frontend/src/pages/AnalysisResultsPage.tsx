import React, { useState, useEffect } from 'react';
import { Container, Typography, Box, Paper, List, ListItem, ListItemText, CircularProgress, Alert } from '@mui/material';

interface AnalysisResult {
  resumeScore: number;
  jobMatchPercentage: number;
  improvementsSuggested: string[];
  keywordsAnalysis: {
    matched: string[];
    missing: string[];
  };
  tailoredResumePreview: string;
}

const AnalysisResultsPage: React.FC = () => {
  const [analysisData, setAnalysisData] = useState<AnalysisResult | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  // Simulate loading analysis data from backend
  useEffect(() => {
    const fetchSampleData = async () => {
      try {
        // In a real app, this would call the actual API endpoint
        await new Promise(resolve => setTimeout(resolve, 1000));

        const sampleData: AnalysisResult = {
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

        setAnalysisData(sampleData);
      } catch (err) {
        setError('Failed to load analysis data. Please try again.');
      } finally {
        setLoading(false);
      }
    };

    fetchSampleData();
  }, []);

  if (loading) {
    return (
      <Container maxWidth="lg">
        <Box sx={{ mt: 4, textAlign: 'center', py: 10 }}>
          <CircularProgress size={60} />
          <Typography variant="h6" sx={{ mt: 2 }}>Loading analysis results...</Typography>
        </Box>
      </Container>
    );
  }

  if (error) {
    return (
      <Container maxWidth="lg">
        <Box sx={{ mt: 4 }}>
          <Alert severity="error">{error}</Alert>
        </Box>
      </Container>
    );
  }

  if (!analysisData) {
    return (
      <Container maxWidth="lg">
        <Box sx={{ mt: 4 }}>
          <Typography variant="h6">No analysis data available</Typography>
          <Typography>Please complete the job description and resume upload first.</Typography>
        </Box>
      </Container>
    );
  }

  const { resumeScore, jobMatchPercentage, improvementsSuggested, keywordsAnalysis, tailoredResumePreview } = analysisData;

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
                secondary={`${resumeScore}/100`}
              />
            </ListItem>
            <ListItem>
              <ListItemText
                primary="Job Match Percentage"
                secondary={`${jobMatchPercentage}%`}
              />
            </ListItem>
          </List>
        </Paper>

        <Paper elevation={3} sx={{ p: 3, mb:4 }}>
          <Typography variant="h6">Improvements Suggested</Typography>
          <List>
            {improvementsSuggested.map((suggestion, index) => (
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
              {keywordsAnalysis.matched.map((keyword, index) => (
                <Box key={index} sx={{ display: 'inline-block', mr: 1, mb: 1, px: 2, py: 0.5, bgcolor: '#e8f5e9', color: '#4caf50' }}>
                  {keyword}
                </Box>
              ))}
            </Box>
            <Box flex={1}>
              <Typography variant="subtitle1" gutterBottom>Missing Keywords</Typography>
              {keywordsAnalysis.missing.map((keyword, index) => (
                <Box key={index} sx={{ display: 'inline-block', mr: 1, mb: 1, px: 2, py: 0.5, bgcolor: '#ffebee', color: '#d32f2f' }}>
                  {keyword}
                </Box>
              ))}
            </Box>
          </Box>
        </Paper>

        <Paper elevation={3} sx={{ p: 3 }}>
          <Typography variant="h6">Tailored Resume Preview</Typography>
          <pre style={{ whiteSpace: 'pre-wrap', overflowX: 'auto' }}>{tailoredResumePreview}</pre>
        </Paper>
      </Box>
    </Container>
  );
};

export default AnalysisResultsPage;
