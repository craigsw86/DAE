import React from 'react';

function App() {
    return (
        <div>
            <h1>HIPAA Checklist Mock</h1>
        </div>
    );
}

export default App;

useEffect(() => {
    fetch('http://localhost:8000/') // Django placeholder
        .then(res => res.text())
        .then(data => console.log(data));
}, []);