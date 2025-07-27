import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { Container, CssBaseline, Box, Typography } from '@mui/material';
import Header from './components/Header';
import ResumeUploadPage from './pages/ResumeUploadPage';
import JobDescriptionPage from './pages/JobDescriptionPage';
import AnalysisResultsPage from './pages/AnalysisResultsPage';

const App: React.FC = () => {
  return (
    <Router>
      <Container maxWidth="lg">
        <CssBaseline />
        <Header />

        <Box mt={4} mb={4}>
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/upload-resume" element={<ResumeUploadPage />} />
            <Route path="/job-description" element={<JobDescriptionPage />} />
            <Route path="/results" element={<AnalysisResultsPage />} />
          </Routes>
        </Box>

        <Box textAlign="center" mt={4} mb={2}>
          <Typography variant="body2" color="textSecondary">
            © {new Date().getFullYear()} Resume Tailor. All rights reserved.
          </Typography>
        </Box>
      </Container>
    </Router>
  );
};

const Home: React.FC = () => (
  <Box textAlign="center" py={8}>
    <Typography variant="h3" gutterBottom>
      Welcome to Resume Tailor
    </Typography>
    <Typography variant="body1" paragraph>
      Optimize your resume with AI-powered analysis and tailoring.
    </Typography>
    <Box mt={4}>
      <a href="/upload-resume">
        <button>Upload Your Resume</button>
      </a>
      <a href="/job-description" style={{ marginLeft: '16px' }}>
        <button>Analyze Job Description</button>
      </a>
    </Box>
  </Box>
);

export default App;
