import React, { useEffect, useState } from 'react';
import axios from 'axios';

function ChecklistDisplay() {
  const [items, setItems] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const fetchChecklist = async () => {
    setLoading(true);
    setError(null);
    try {
      const token = localStorage.getItem('token');
      const response = await axios.get('http://localhost:8000/api/checklist/', {
        headers: token ? { Authorization: `Bearer ${token}` } : {},
      });
      setItems(response.data);
    } catch (err) {
      if (err.response && err.response.status === 401) {
        setError('Authentication required. Please log in.');
      } else {
        setError('Failed to fetch checklist items.');
      }
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchChecklist();
  }, []);

  if (loading) return <div>Loading checklist...</div>;
  if (error) return <div style={{color: 'red'}}>{error}</div>;

  return (
    <div>
      <h2>Checklist Items</h2>
      <button onClick={fetchChecklist} style={{marginBottom: '10px'}}>Refresh</button>
      {items.length === 0 ? (
        <div>No checklist items found.</div>
      ) : (
        <table border="1" cellPadding="6">
          <thead>
            <tr>
              <th>User</th>
              <th>Regulation</th>
              <th>Completed</th>
              <th>Notes</th>
              <th>Last Updated</th>
            </tr>
          </thead>
          <tbody>
            {items.map(item => (
              <tr key={item.id}>
                <td>{item.user}</td>
                <td>{item.regulation_update}</td>
                <td>{item.completed ? 'Yes' : 'No'}</td>
                <td>{item.notes}</td>
                <td>{item.last_updated}</td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
}

export default ChecklistDisplay; 