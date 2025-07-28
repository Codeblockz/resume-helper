import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import { Container, Typography, Box, Button, Grid } from '@mui/material';
import JobDescriptionPage from './pages/JobDescriptionPage';
import ResumeEditorPage from './pages/ResumeEditorPage';
import AnalysisResultsPage from './pages/AnalysisResultsPage';
import { ResumeTailorProvider } from './contexts/ResumeTailorContext';

const HomePage: React.FC = () => (
  <Container maxWidth="md">
    <Box sx={{ mt: 8, textAlign: 'center' }}>
      <Typography variant="h3" gutterBottom>
        Welcome to Resume Tailor
      </Typography>
      <Typography variant="h6" color="textSecondary" paragraph>
        The intelligent resume optimization platform
      </Typography>

      <Grid container spacing={4} sx={{ mt: 6, justifyContent: 'center' }}>
        <Grid item>
          <Button
            variant="contained"
            size="large"
            color="primary"
            href="/job-description"
          >
            Enter Job Description
          </Button>
        </Grid>

        <Grid item>
          <Button
            variant="outlined"
            size="large"
            color="secondary"
            href="/resume-editor"
          >
            Edit Resume
          </Button>
        </Grid>
      </Grid>
    </Box>
  </Container>
);

const App: React.FC = () => {
  return (
    <Router>
      <ResumeTailorProvider>
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/job-description" element={<JobDescriptionPage />} />
          <Route path="/resume-editor" element={<ResumeEditorPage />} />
          <Route path="/analysis-results" element={<AnalysisResultsPage />} />
        </Routes>
      </ResumeTailorProvider>
    </Router>
  );
};

export default App;
