import React, { useEffect, useState } from 'react';
import axios from 'axios';

function ChecklistDisplay() {
  const [items, setItems] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchChecklist = async () => {
      try {
        const token = localStorage.getItem('token');
        const response = await axios.get('http://localhost:8000/api/checklist/', {
          headers: token ? { Authorization: `Bearer ${token}` } : {},
        });
        setItems(response.data);
      } catch (err) {
        setError('Failed to fetch checklist items.');
      } finally {
        setLoading(false);
      }
    };
    fetchChecklist();
  }, []);

  if (loading) return <div>Loading checklist...</div>;
  if (error) return <div>{error}</div>;

  return (
    <div>
      <h2>Checklist Items</h2>
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
    </div>
  );
}

export default ChecklistDisplay; 