import React, { useState } from 'react';
import { BrowserRouter as Router, Route, Switch, Link } from 'react-router-dom';  // Install react-router-dom
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
      <Switch>
        <Route path="/checklist"><Checklist token={token} /></Route>
        <Route path="/report"><ComplianceReport token={token} /></Route>
      </Switch>
    </Router>
  );
}

export default App;