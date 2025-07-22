import React, { useState } from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import Login from './components/Login';
import Checklist from './components/Checklist';
import ComplianceReport from './components/ComplianceReport';
import { AppBar, Tabs, Tab } from '@mui/material';

function App() {
  const [token, setToken] = useState(localStorage.getItem('token'));

  if (!token) {
    return <Login setToken={setToken} />;
  }

  return (
    <Router>
      <AppBar position="static">
        <Tabs>
          <Tab label="Checklist" component={Link} to="/checklist" />
          <Tab label="Report" component={Link} to="/report" />
        </Tabs>
      </AppBar>
      <Routes>
        <Route path="/checklist" element={<Checklist token={token} />} />
        <Route path="/report" element={<ComplianceReport token={token} />} />
      </Routes>
    </Router>
  );
}

export default App;