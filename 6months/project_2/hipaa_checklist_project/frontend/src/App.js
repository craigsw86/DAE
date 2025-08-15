import React, { useState, useEffect } from 'react';
import ChecklistDisplay from './components/ChecklistDisplay';
import Login from './components/Login';
import { ThemeProvider, createTheme, CssBaseline, AppBar, Toolbar, Typography, Container, Box } from '@mui/material';

const theme = createTheme({
  palette: {
    primary: { main: '#1976d2' },
    secondary: { main: '#388e3c' },
    background: { default: '#f5f5f5' },
  },
});

function App() {
  const [token, setToken] = useState(null);

  useEffect(() => {
    const storedToken = localStorage.getItem('token');
    if (storedToken) {
      setToken(storedToken);
    }
  }, []);

  if (!token) {
    return (
      <ThemeProvider theme={theme}>
        <CssBaseline />
        <Login setToken={setToken} />
      </ThemeProvider>
    );
  }

  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <AppBar position="static">
        <Toolbar>
          <Typography variant="h6" sx={{ flexGrow: 1 }}>
            HIPAA Compliance Checklist
          </Typography>
        </Toolbar>
      </AppBar>
      <Container maxWidth="md" sx={{ mt: 4, mb: 4 }}>
        <ChecklistDisplay />
      </Container>
      <Box component="footer" sx={{ p: 2, textAlign: 'center', bgcolor: 'grey.100' }}>
        <Typography variant="body2" color="text.secondary">
          © 2025 HIPAA Checklist Project
        </Typography>
      </Box>
    </ThemeProvider>
  );
}

export default App;