import React, { useState } from 'react';
function Login() {
    const [username, setUsername] = useState('');
    return (
        <div>
            <input value={username} onChange={e => setUsername(e.target.value)}/>
            <button onClick={() => fetch('http://localhost:8000/api/placeholder').then(res => console.log(res))}>Login</button>
        </div>
    );
}
export default Login;