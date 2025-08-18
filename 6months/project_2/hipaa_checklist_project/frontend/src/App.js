import React, { useState, useEffect } from 'react';
import ChecklistDisplay from './components/ChecklistDisplay';
import Login from './components/Login';
import ComplianceReport from './components/ComplianceReport';
import { ThemeProvider, createTheme, CssBaseline, AppBar, Toolbar, Typography, Container, Box, Tabs, Tab } from '@mui/material';

const theme = createTheme({
  palette: {
    primary: { main: '#1976d2' },
    secondary: { main: '#388e3c' },
    background: { default: '#f5f5f5' },
  },
});

function App() {
  const [token, setToken] = useState(null);
  const [tab, setTab] = useState(0);

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
        <Tabs value={tab} onChange={(_, v) => setTab(v)} centered sx={{ mb: 4 }}>
          <Tab label="Checklist" />
          <Tab label="Compliance Report" />
        </Tabs>
        {tab === 0 && <ChecklistDisplay />}
        {tab === 1 && <ComplianceReport />}
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