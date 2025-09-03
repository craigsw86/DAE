import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Box, Paper, Typography, TextField, Button, Alert } from '@mui/material';

// Utility to parse API errors
function parseApiError(err) {
  if (err.response) {
    if (err.response.status === 401) {
      return 'Invalid username or password.';
    } else if (err.response.status === 400 && typeof err.response.data === 'object') {
      // Handle field errors
      return Object.entries(err.response.data)
        .map(([field, msgs]) => `${field}: ${Array.isArray(msgs) ? msgs.join(', ') : msgs}`)
        .join(' ');
    } else if (err.response.data && err.response.data.detail) {
      return err.response.data.detail;
    } else {
      return 'Login failed. Please try again.';
    }
  } else if (err.request) {
    return 'Network error. Please check your connection.';
  } else {
    return 'An unexpected error occurred.';
  }
}

function Login({ setToken }) {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const [retry, setRetry] = useState(false);

  useEffect(() => {
    if (error) {
      const timer = setTimeout(() => setError(''), 5000);
      return () => clearTimeout(timer);
    }
  }, [error]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);
    setRetry(false);
    try {
      const response = await axios.post(`${process.env.REACT_APP_API_BASE_URL}/api/token/`, { username, password });
      localStorage.setItem('token', response.data.access);
      setToken(response.data.access);
    } catch (err) {
      setError(parseApiError(err));
      if (err.request && !err.response) setRetry(true);
    } finally {
      setLoading(false);
    }
  };

  return (
    <Box display="flex" justifyContent="center" alignItems="center" minHeight="100vh" bgcolor="#f5f5f5">
      <Paper elevation={3} sx={{ p: 4, minWidth: 320 }}>
        <Typography variant="h5" component="h2" gutterBottom align="center">
          Login
        </Typography>
        <form onSubmit={handleSubmit}>
          <TextField
            label="Username"
            variant="outlined"
            fullWidth
            margin="normal"
            value={username}
            onChange={e => setUsername(e.target.value)}
            required
          />
          <TextField
            label="Password"
            type="password"
            variant="outlined"
            fullWidth
            margin="normal"
            value={password}
            onChange={e => setPassword(e.target.value)}
            required
          />
          <Button
            type="submit"
            variant="contained"
            color="primary"
            fullWidth
            sx={{ mt: 2 }}
            disabled={loading}
            aria-busy={loading}
          >
            {loading ? 'Logging in...' : 'Login'}
          </Button>
          {retry && (
            <Button
              variant="outlined"
              color="secondary"
              fullWidth
              sx={{ mt: 1 }}
              onClick={handleSubmit}
              disabled={loading}
            >
              Retry
            </Button>
          )}
          {error && <Alert severity="error" sx={{ mt: 2 }} role="alert">{error}</Alert>}
        </form>
      </Paper>
    </Box>
  );
}

export default Login;