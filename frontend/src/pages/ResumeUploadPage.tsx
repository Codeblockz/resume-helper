import React, { useState } from 'react';
import { Button, Typography, Container, Box, CircularProgress, Alert } from '@mui/material';
import { styled } from '@mui/system';

const VisuallyHiddenInput = styled('input')({
  clip: 'rect(0 0 0 0)',
  clipPath: 'inset(50%)',
  height: 1,
  overflow: 'hidden',
  position: 'absolute',
  bottom: 0,
  left: 0,
  whiteSpace: 'nowrap',
  width: 1,
});

const ResumeUploadPage: React.FC = () => {
  const [file, setFile] = useState<File | null>(null);
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState<string | null>(null);

  const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    if (event.target.files && event.target.files[0]) {
      setFile(event.target.files[0]);
      setMessage(null); // Reset message when new file is selected
    }
  };

  const handleUpload = async () => {
    if (!file) return;

    const formData = new FormData();
    formData.append('file', file);

    try {
      setLoading(true);
      setMessage(null);

      // Simulate API call (replace with actual API call)
      await new Promise(resolve => setTimeout(resolve, 1500));

      setMessage(`Successfully uploaded: ${file.name}`);
    } catch (error) {
      setMessage('Failed to upload file. Please try again.');
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
          textAlign: 'center',
        }}
      >
        <Typography variant="h5" gutterBottom>
          Upload Your Resume
        </Typography>

        {message && (
          <Alert severity={message.includes('Successfully') ? 'success' : 'error'} sx={{ mb: 3 }}>
            {message}
          </Alert>
        )}

        <Box sx={{ display: 'flex', justifyContent: 'center', mb: 2 }}>
          <Button
            component="label"
            variant="contained"
            color="primary"
            disabled={loading}
          >
            {file ? file.name : 'Choose Resume File'}
            <VisuallyHiddenInput
              type="file"
              accept=".pdf,.docx,.txt"
              onChange={handleFileChange}
            />
          </Button>
        </Box>

        {file && (
          <Typography variant="body2" color="textSecondary">
            Selected file: {file.name} ({(file.size / 1024).toFixed(2)} KB)
          </Typography>
        )}

        <Box sx={{ mt: 3 }}>
          <Button
            variant="contained"
            color="secondary"
            onClick={handleUpload}
            disabled={!file || loading}
            fullWidth
          >
            {loading ? <CircularProgress size={24} /> : 'Upload and Analyze'}
          </Button>
        </Box>
      </Box>
    </Container>
  );
};

export default ResumeUploadPage;
