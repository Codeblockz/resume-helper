import React from 'react';
import { useNavigate } from 'react-router-dom';
import { Button, Typography, Container, Box, Paper, List, ListItem, ListItemText } from '@mui/material';
import { useWorkflow } from '../contexts/ResumeTailorContext';

interface KeywordAnalysis {
  matched: string[];
  missing: string[];
}

interface AnalysisResult {
  resumeScore?: number;
  jobMatchPercentage?: number;
  improvementsSuggested?: string[];
  keywordsAnalysis?: KeywordAnalysis;
  tailoredResumePreview?: string;
}

const AnalysisResultsPage: React.FC = () => {
  const { state } = useWorkflow();
  const navigate = useNavigate();

  // Check if we have analysis data
  const hasAnalysisData = !!state.analysisResult;

  if (!hasAnalysisData) {
    return (
      <Container maxWidth="lg">
        <Box sx={{ mt: 4 }}>
          <Typography variant="h6">No analysis data available</Typography>
          <Typography>Please complete the job description and resume upload first.</Typography>
          <Box sx={{ mt: 3 }}>
            <Button
              variant="contained"
              color="primary"
              onClick={() => navigate('/job-description')}
            >
              Start Now
            </Button>
          </Box>
        </Box>
      </Container>
    );
  }

  const analysisResult = state.analysisResult!;

  return (
    <Container maxWidth="lg">
      <Box sx={{ mt: 4 }}>
        <Typography variant="h4" gutterBottom>
          Resume Analysis Results
        </Typography>

        {(analysisResult.resumeScore !== undefined || analysisResult.jobMatchPercentage !== undefined) && (
          <Paper elevation={3} sx={{ p: 3, mb: 4 }}>
            <Typography variant="h6">Overall Assessment</Typography>
            <List>
              {analysisResult.resumeScore !== undefined && (
                <ListItem>
                  <ListItemText
                    primary="Resume Quality Score"
                    secondary={`${analysisResult.resumeScore}/100`}
                  />
                </ListItem>
              )}
              {analysisResult.jobMatchPercentage !== undefined && (
                <ListItem>
                  <ListItemText
                    primary="Job Match Percentage"
                    secondary={`${analysisResult.jobMatchPercentage}%`}
                  />
                </ListItem>
              )}
            </List>
          </Paper>
        )}

        {Array.isArray(analysisResult.improvementsSuggested) && analysisResult.improvementsSuggested.length > 0 && (
          <Paper elevation={3} sx={{ p: 3, mb:4 }}>
            <Typography variant="h6">Improvements Suggested</Typography>
            <List>
              {analysisResult.improvementsSuggested.map((suggestion: string, index: number) => (
                <ListItem key={index}>
                  <ListItemText primary={`• ${suggestion}`} />
                </ListItem>
              ))}
            </List>
          </Paper>
        )}

        {(analysisResult.keywordsAnalysis && (analysisResult.keywordsAnalysis.matched.length > 0 ||
          analysisResult.keywordsAnalysis.missing.length > 0)) && (
          <Paper elevation={3} sx={{ p: 3, mb:4 }}>
            <Typography variant="h6">Keyword Analysis</Typography>
            <Box sx={{ display: 'flex', gap: 2 }}>
              {analysisResult.keywordsAnalysis && analysisResult.keywordsAnalysis.matched.length > 0 && (
                <Box flex={1}>
                  <Typography variant="subtitle1" gutterBottom>Matched Keywords</Typography>
                  {analysisResult.keywordsAnalysis.matched.map((keyword: string, index: number) => (
                    <Box key={index} sx={{ display: 'inline-block', mr: 1, mb: 1, px: 2, py: 0.5, bgcolor: '#e8f5e9', color: '#4caf50' }}>
                      {keyword}
                    </Box>
                  ))}
                </Box>
              )}
              {analysisResult.keywordsAnalysis && analysisResult.keywordsAnalysis.missing.length > 0 && (
                <Box flex={1}>
                  <Typography variant="subtitle1" gutterBottom>Missing Keywords</Typography>
                  {analysisResult.keywordsAnalysis.missing.map((keyword: string, index: number) => (
                    <Box key={index} sx={{ display: 'inline-block', mr: 1, mb: 1, px: 2, py: 0.5, bgcolor: '#ffebee', color: '#d32f2f' }}>
                      {keyword}
                    </Box>
                  ))}
                </Box>
              )}
            </Box>
          </Paper>
        )}

        <Paper elevation={3} sx={{ p: 3 }}>
          <Typography variant="h6">Tailored Resume Preview</Typography>
          <pre style={{ whiteSpace: 'pre-wrap', overflowX: 'auto' }}>{analysisResult.tailoredResumePreview || 'No tailored preview available'}</pre>
        </Box>
      </Box>
    </Container>
  );
};

export default AnalysisResultsPage;
