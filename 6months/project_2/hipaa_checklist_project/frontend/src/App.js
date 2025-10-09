import React, { useState, useEffect } from 'react';
import ChecklistDisplay from './components/ChecklistDisplay';
import Login from './components/Login';
import ComplianceReport from './components/ComplianceReport';
import SecurityDashboard from './components/SecurityDashboard';
import { ThemeProvider, createTheme, CssBaseline, AppBar, Toolbar, Typography, Container, Box, Tabs, Tab, Button } from '@mui/material';

// Material-UI theme configuration for consistent styling
const theme = createTheme({
  palette: {
    primary: { main: '#1976d2' },    // Blue primary color
    secondary: { main: '#388e3c' },   // Green secondary color
    background: { default: '#f5f5f5' }, // Light gray background
  },
});

/**
 * Main App component for the HIPAA Checklist application.
 * 
 * This component manages the overall application state including:
 * - User authentication (JWT token management)
 * - Tab navigation between different sections
 * - Theme and styling configuration
 * 
 * The app uses a tabbed interface with three main sections:
 * 1. Checklist - Main checklist management
 * 2. Compliance Report - Reporting and analytics
 * 3. Security Dashboard - Security monitoring
 */
function App() {
  // State management for authentication and navigation
  const [token, setToken] = useState(null);  // JWT authentication token
  const [tab, setTab] = useState(0);          // Active tab index (0=Checklist, 1=Report, 2=Security)

  /**
   * Effect hook to check for existing authentication token on app load.
   * 
   * Retrieves stored JWT token from localStorage to maintain user session
   * across browser refreshes and page reloads.
   */
  useEffect(() => {
    const storedToken = localStorage.getItem('token');
    if (storedToken) {
      setToken(storedToken);
    }
  }, []);

  /**
   * Handle user logout by clearing authentication token and redirecting to login.
   * 
   * Removes the JWT token from localStorage and resets the application state
   * to force the user back to the login screen.
   */
  const handleLogout = () => {
    localStorage.removeItem('token');
    setToken(null);
  };

  // Render login component if user is not authenticated
  if (!token) {
    return (
      <ThemeProvider theme={theme}>
        <CssBaseline />
        <Login setToken={setToken} />
      </ThemeProvider>
    );
  }

  /**
   * Render the main application interface for authenticated users.
   * 
   * Returns a complete application layout with:
   * - Navigation bar with application title
   * - Tabbed interface for different sections
   * - Footer with copyright information
   * 
   * @returns {JSX.Element} Complete application interface
   */
  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      
      {/* Application header with title and logout button */}
      <AppBar position="static">
        <Toolbar>
          <Typography variant="h6" sx={{ flexGrow: 1 }}>
            HIPAA Compliance Checklist
          </Typography>
          <Button 
            color="inherit" 
            onClick={handleLogout}
            sx={{ 
              ml: 2,
              '&:hover': {
                backgroundColor: 'rgba(255, 255, 255, 0.1)'
              }
            }}
          >
            Logout
          </Button>
        </Toolbar>
      </AppBar>
      
      {/* Main content area with tabbed navigation */}
      <Container maxWidth="md" sx={{ mt: 4, mb: 4 }}>
        <Tabs value={tab} onChange={(_, v) => setTab(v)} centered sx={{ mb: 4 }}>
          <Tab label="Checklist" />
          <Tab label="Compliance Report" />
          <Tab label="Security Dashboard" />
        </Tabs>
        
        {/* Conditional rendering based on active tab */}
        {tab === 0 && <ChecklistDisplay />}
        {tab === 1 && <ComplianceReport />}
        {tab === 2 && <SecurityDashboard />}
      </Container>
      
      {/* Application footer */}
      <Box component="footer" sx={{ p: 2, textAlign: 'center', bgcolor: 'grey.100' }}>
        <Typography variant="body2" color="text.secondary">
          © 2025 HIPAA Checklist Project
        </Typography>
      </Box>
    </ThemeProvider>
  );
}

export default App;