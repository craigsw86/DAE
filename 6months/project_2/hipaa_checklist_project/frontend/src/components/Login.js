import React, { useState } from 'react';
import axios from 'axios';

function Login({ setToken }) {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [message, setMessage] = useState('');

  const handleLogin = async () => {
    try {
      const response = await axios.post('http://localhost:8000/api/token/', { username, password });
      const { access } = response.data;
      if (access) {
        localStorage.setItem('token', access);
        setMessage('Login successful!');
        if (setToken) setToken(access);
      } else {
        setMessage('Login failed: No access token received.');
      }
    } catch (error) {
      setMessage('Login failed: ' + (error.response?.data?.detail || error.message));
    }
  };

  return (
    <div>
      <input
        type="text"
        value={username}
        onChange={(e) => setUsername(e.target.value)}
        placeholder="Username"
      />
      <input
        type="password"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
        placeholder="Password"
      />
      <button onClick={handleLogin}>Login</button>
      {message && <div>{message}</div>}
    </div>
  );
}

export default Login;