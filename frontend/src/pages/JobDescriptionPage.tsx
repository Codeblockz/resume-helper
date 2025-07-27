import React, { useState } from 'react';
import { Button, Typography, Container, Box, TextField, CircularProgress, Alert } from '@mui/material';

const JobDescriptionPage: React.FC = () => {
  const [jobTitle, setJobTitle] = useState("");
  const [company, setCompany] = useState("");
  const [description, setDescription] = useState("");
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState<string | null>(null);

  const handleSubmit = async () => {
    if (!jobTitle || !description) return;

    try {
      setLoading(true);
      setMessage(null);

      // Simulate API call
      await new Promise(resolve => setTimeout(resolve, 1500));

      setMessage(`Job description submitted: ${jobTitle}`);
    } catch (error) {
      setMessage('Failed to submit job description. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <Container maxWidth="md">
      <Box
        sx={{
          mt: 8,
          p: 4,
          border: '1px solid #ddd',
          borderRadius: 2,
        }}
      >
        <Typography variant="h5" gutterBottom>
          Enter Job Description
        </Typography>

        {message && (
          <Alert severity={message.includes('submitted') ? 'success' : 'error'} sx={{ mb: 3 }}>
            {message}
          </Alert>
        )}

        <TextField
          label="Job Title"
          value={jobTitle}
          onChange={(e) => setJobTitle(e.target.value)}
          fullWidth
          margin="normal"
          required
        />

        <TextField
          label="Company (optional)"
          value={company}
          onChange={(e) => setCompany(e.target.value)}
          fullWidth
          margin="normal"
        />

        <TextField
          label="Job Description"
          value={description}
          onChange={(e) => setDescription(e.target.value)}
          multiline
          rows={8}
          fullWidth
          margin="normal"
          required
        />

        <Box sx={{ mt: 3 }}>
          <Button
            variant="contained"
            color="primary"
            onClick={handleSubmit}
            disabled={!jobTitle || !description || loading}
            fullWidth
          >
            {loading ? <CircularProgress size={24} /> : 'Analyze Job Description'}
          </Button>
        </Box>
      </Box>
    </Container>
  );
};

export default JobDescriptionPage;
