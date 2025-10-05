import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Box, Paper, Typography, TextField, Button, Alert } from '@mui/material';

/**
 * Utility function to parse and format API error messages.
 * 
 * Provides user-friendly error messages by analyzing different types
 * of API errors including authentication, validation, and network issues.
 * 
 * @param {Error} err - The error object from axios request
 * @returns {string} User-friendly error message
 */
function parseApiError(err) {
  if (err.response) {
    // Handle HTTP response errors
    if (err.response.status === 401) {
      return 'Invalid username or password.';
    } else if (err.response.status === 400 && typeof err.response.data === 'object') {
      // Handle field validation errors
      return Object.entries(err.response.data)
        .map(([field, msgs]) => `${field}: ${Array.isArray(msgs) ? msgs.join(', ') : msgs}`)
        .join(' ');
    } else if (err.response.data && err.response.data.detail) {
      return err.response.data.detail;
    } else {
      return 'Login failed. Please try again.';
    }
  } else if (err.request) {
    // Handle network errors
    return 'Network error. Please check your connection.';
  } else {
    // Handle unexpected errors
    return 'An unexpected error occurred.';
  }
}

/**
 * Login component for user authentication.
 * 
 * Provides a secure login interface with JWT token authentication.
 * Handles form submission, error display, and token storage.
 * 
 * @param {Object} props - Component props
 * @param {Function} props.setToken - Function to set authentication token
 * @returns {JSX.Element} Login form component
 */
function Login({ setToken }) {
  // Component state management
  const [username, setUsername] = useState('');     // Username input value
  const [password, setPassword] = useState('');     // Password input value
  const [error, setError] = useState('');          // Error message display
  const [loading, setLoading] = useState(false);   // Loading state for form submission
  const [retry, setRetry] = useState(false);       // Retry button visibility

  /**
   * Effect hook to auto-hide error messages after 5 seconds.
   * 
   * Provides better UX by automatically clearing error messages
   * to avoid cluttering the interface.
   */
  useEffect(() => {
    if (error) {
      const timer = setTimeout(() => setError(''), 5000);
      return () => clearTimeout(timer);
    }
  }, [error]);

  /**
   * Handle form submission for user authentication.
   * 
   * Sends credentials to the backend API, stores JWT token on success,
   * and handles various error scenarios with user-friendly messages.
   * 
   * @param {Event} e - Form submission event
   */
  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);
    setRetry(false);
    
    try {
      // Send authentication request to backend
      const response = await axios.post(`${process.env.REACT_APP_API_BASE_URL || 'http://localhost:8000'}/api/token/`, { username, password });
      
      // Store JWT token in localStorage for session persistence
      localStorage.setItem('token', response.data.access);
      setToken(response.data.access);
    } catch (err) {
      setError(parseApiError(err));
      // Show retry button for network errors
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