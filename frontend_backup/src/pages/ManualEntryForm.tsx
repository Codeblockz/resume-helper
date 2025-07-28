import React, { useState } from 'react';
import { Button, Typography, Container, Box, TextField, MenuItem, CircularProgress, Alert } from '@mui/material';

interface FormData {
  firstName: string;
  lastName: string;
  email: string;
  phone: string;
  jobTitle: string;
  summary: string;
  experiences: { company: string; title: string; startDate: string; endDate: string; description: string }[];
  skills: string[];
  education: { school: string; degree: string; fieldOfStudy: string; graduationYear: string }[];
}

const ManualEntryForm: React.FC = () => {
  const [formData, setFormData] = useState<FormData>({
    firstName: '',
    lastName: '',
    email: '',
    phone: '',
    jobTitle: '',
    summary: '',
    experiences: [{ company: '', title: '', startDate: '', endDate: '', description: '' }],
    skills: [''],
    education: [{ school: '', degree: '', fieldOfStudy: '', graduationYear: '' }],
  });

  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState<string | null>(null);

  // Simplified handlers that use type assertion to avoid TypeScript issues
  const handleChange = (field: string) => (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    setFormData({ ...formData, [field]: e.target.value } as never);
  };

  const handleExperienceChange = (index: number, field: string) => (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    const newExperiences = [...formData.experiences];
    newExperiences[index] = { ...newExperiences[index], [field]: e.target.value } as never;
    setFormData({ ...formData, experiences: newExperiences });
  };

  const addExperience = () => {
    setFormData({
      ...formData,
      experiences: [...formData.experiences, { company: '', title: '', startDate: '', endDate: '', description: '' }],
    });
  };

  const handleSkillChange = (index: number) => (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    const newSkills = [...formData.skills];
    newSkills[index] = e.target.value;
    setFormData({ ...formData, skills: newSkills });
  };

  const addSkill = () => {
    setFormData({ ...formData, skills: [...formData.skills, ''] });
  };

  const handleEducationChange = (index: number, field: string) => (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    const newEducation = [...formData.education];
    newEducation[index] = { ...newEducation[index], [field]: e.target.value } as never;
    setFormData({ ...formData, education: newEducation });
  };

  const addEducation = () => {
    setFormData({
      ...formData,
      education: [...formData.education, { school: '', degree: '', fieldOfStudy: '', graduationYear: '' }],
    });
  };

  const handleSubmit = async () => {
    // Validate required fields
    if (!formData.firstName || !formData.lastName || !formData.jobTitle) {
      setMessage('Please fill in all required fields.');
      return;
    }

    try {
      setLoading(true);
      setMessage(null);

      const resumeData = {
        firstName: formData.firstName,
        lastName: formData.lastName,
        jobTitle: formData.jobTitle,
        email: formData.email,
        phone: formData.phone,
        summary: formData.summary,
        experiences: formData.experiences.filter(exp => exp.company && exp.title),
        skills: formData.skills.filter(skill => skill),
        education: formData.education.filter(edu => edu.school && edu.degree)
      };

      // Make actual API call to backend
      // Use backend service name when running with Docker Compose
      const apiUrl = (typeof process !== 'undefined' && process.env.NODE_ENV === 'development' &&
                   window.location.hostname === 'localhost')
        ? 'http://localhost:8002/api/upload/manual-form-json'
        : 'http://backend/api/upload/manual-form-json';

      const response = await fetch(apiUrl, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(resumeData)
      });

      if (!response.ok) {
        const errorData = await response.json() as { detail?: string };
        throw new Error(errorData.detail || 'Failed to submit resume');
      }

      const result = await response.json();

      console.log('API Response:', result);
      setMessage('Resume submitted successfully!');
    } catch (error) {
      // Type assertion for error
      const errorMsg = (error as Error).message;
      setMessage(`Failed to submit resume: ${errorMsg}`);
    } finally {
      setLoading(false);
    }
  };

  return (
    <Container maxWidth="lg">
      <Box
        sx={{
          mt: 4,
          p: 4,
          border: '1px solid #ddd',
          borderRadius: 2,
        }}
      >
        <Typography variant="h5" gutterBottom>
          Manual Resume Entry
        </Typography>

        {message && (
          <Alert severity={message.includes('Successfully') ? 'success' : 'error'} sx={{ mb: 3 }}>
            {message}
          </Alert>
        )}

        {/* Contact Information */}
        <Box sx={{ mb: 4 }}>
          <Typography variant="h6">Contact Information</Typography>

          <TextField
            label="First Name *"
            value={formData.firstName}
            onChange={handleChange('firstName')}
            fullWidth
            margin="normal"
            required
          />

          <TextField
            label="Last Name *"
            value={formData.lastName}
            onChange={handleChange('lastName')}
            fullWidth
            margin="normal"
            required
          />

          <TextField
            label="Email"
            type="email"
            value={formData.email}
            onChange={handleChange('email')}
            fullWidth
            margin="normal"
          />

          <TextField
            label="Phone"
            value={formData.phone}
            onChange={handleChange('phone')}
            fullWidth
            margin="normal"
          />
        </Box>

        {/* Job Title */}
        <Box sx={{ mb: 4 }}>
          <Typography variant="h6">Professional Summary</Typography>

          <TextField
            label="Job Title *"
            value={formData.jobTitle}
            onChange={handleChange('jobTitle')}
            fullWidth
            margin="normal"
            required
          />

          <TextField
            label="Summary"
            value={formData.summary}
            onChange={handleChange('summary')}
            multiline
            rows={4}
            fullWidth
            margin="normal"
          />
        </Box>

        {/* Work Experience */}
        <Box sx={{ mb: 4 }}>
          <Typography variant="h6">Work Experience</Typography>
          {formData.experiences.map((exp, index) => (
            <Box key={index} sx={{ mb: 3, p: 2, border: '1px solid #eee', borderRadius: 1 }}>
              <TextField
                label="Company"
                value={exp.company}
                onChange={handleExperienceChange(index, 'company')}
                fullWidth
                margin="normal"
              />

              <TextField
                label="Job Title"
                value={exp.title}
                onChange={handleExperienceChange(index, 'title')}
                fullWidth
                margin="normal"
              />

              <Box sx={{ display: 'flex', gap: 2 }}>
                <TextField
                  label="Start Date (MM/YYYY)"
                  value={exp.startDate}
                  onChange={handleExperienceChange(index, 'startDate')}
                  fullWidth
                  margin="normal"
                />

                <TextField
                  label="End Date (MM/YYYY)"
                  value={exp.endDate}
                  onChange={handleExperienceChange(index, 'endDate')}
                  fullWidth
                  margin="normal"
                />
              </Box>

              <TextField
                label="Description"
                value={exp.description}
                onChange={handleExperienceChange(index, 'description')}
                multiline
                rows={3}
                fullWidth
                margin="normal"
              />

              {index === formData.experiences.length - 1 && (
                <Button variant="outlined" color="primary" onClick={addExperience}>
                  Add Another Experience
                </Button>
              )}
            </Box>
          ))}
        </Box>

        {/* Skills */}
        <Box sx={{ mb: 4 }}>
          <Typography variant="h6">Skills</Typography>
          {formData.skills.map((skill, index) => (
            <TextField
              key={index}
              label={`Skill ${index + 1}`}
              value={skill}
              onChange={handleSkillChange(index)}
              fullWidth
              margin="normal"
            />
          ))}

          {formData.skills.length < 5 && (
            <Button variant="outlined" color="primary" onClick={addSkill}>
              Add Another Skill
            </Button>
          )}
        </Box>

        {/* Education */}
        <Box sx={{ mb: 4 }}>
          <Typography variant="h6">Education</Typography>
          {formData.education.map((edu, index) => (
            <Box key={index} sx={{ mb: 3, p: 2, border: '1px solid #eee', borderRadius: 1 }}>
              <TextField
                label="School"
                value={edu.school}
                onChange={handleEducationChange(index, 'school')}
                fullWidth
                margin="normal"
              />

              <Box sx={{ display: 'flex', gap: 2 }}>
                <TextField
                  label="Degree"
                  value={edu.degree}
                  onChange={handleEducationChange(index, 'degree')}
                  fullWidth
                  margin="normal"
                />

                <TextField
                  label="Field of Study"
                  value={edu.fieldOfStudy}
                  onChange={handleEducationChange(index, 'fieldOfStudy')}
                  fullWidth
                  margin="normal"
                />
              </Box>

              <TextField
                label="Graduation Year"
                type="number"
                value={edu.graduationYear}
                onChange={handleEducationChange(index, 'graduationYear')}
                fullWidth
                margin="normal"
              />

              {index === formData.education.length - 1 && (
                <Button variant="outlined" color="primary" onClick={addEducation}>
                  Add Another Education Entry
                </Button>
              )}
            </Box>
          ))}
        </Box>

        <Box sx={{ mt: 3 }}>
          <Button
            variant="contained"
            color="primary"
            onClick={handleSubmit}
            disabled={loading}
            fullWidth
          >
            {loading ? <CircularProgress size={24} /> : 'Submit Resume'}
          </Button>
        </Box>
      </Box>
    </Container>
  );
};

export default ManualEntryForm;
