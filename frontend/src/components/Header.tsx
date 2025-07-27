import React from 'react';
import { AppBar, Toolbar, Typography, Button } from '@mui/material';
import { Link as RouterLink } from 'react-router-dom';

const Header: React.FC = () => {
  return (
    <AppBar position="static" color="primary">
      <Toolbar sx={{ display: 'flex', justifyContent: 'space-between' }}>
        <Typography variant="h6" component={RouterLink} to="/" style={{ textDecoration: 'none', color: 'inherit' }}>
          Resume Tailor
        </Typography>
        <div>
          <Button component={RouterLink} to="/upload-resume" color="inherit">
            Upload Resume
          </Button>
          <Button component={RouterLink} to="/job-description" color="inherit" sx={{ ml: 2 }}>
            Job Description
          </Button>
        </div>
      </Toolbar>
    </AppBar>
  );
};

export default Header;
