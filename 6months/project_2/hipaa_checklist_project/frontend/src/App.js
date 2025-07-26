import React from 'react';

function App() {
  const handleClick = () => {
    const complianceScore = 50;
    const regulationName = "HIPAA Privacy Rule";
    
    console.log(`Checking compliance for: ${regulationName}`);
    
    const resultElement = document.getElementById("complianceResult");
    if (resultElement) {
      resultElement.innerText = `Compliance Score: ${complianceScore}%`;
    }
  };

  return (
    <div style={{padding: '20px'}}>
      <h1>HIPAA Compliance Checklist</h1>
      <button onClick={handleClick} style={{padding: '10px 20px', fontSize: '16px'}}>
        Check Compliance
      </button>
      <p id="complianceResult">Ready for compliance check</p>
    </div>
  );
}

export default App;