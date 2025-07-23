```
import React from 'react';
import { Button } from '@mui/material';
import { displayMessage, calculateComplianceScore } from './main';

function App() {
  const handleClick = () => {
    // Call main.js function to display message
    displayMessage();
    // Output compliance score to DOM
    const score = calculateComplianceScore(5, 10);
    document.getElementById('output').innerText = `Compliance Score: ${score}%`;
  };

  return (
    <div style={{ padding: '20px', textAlign: 'center' }}>
      <h1>HIPAA Checklist</h1>
      <Button variant="contained" onClick={handleClick}>
        Check Compliance
      </Button>
      <div id="output"></div>
    </div>
  );
}

export default App;
```