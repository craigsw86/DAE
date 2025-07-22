import React, { useState, useEffect } from 'react';
import { Table, TableBody, TableCell, TableHead, TableRow, Checkbox, TextField, Alert } from '@mui/material';
import axios from 'axios';

function Checklist({ token }) {
  const [items, setItems] = useState([]);
  const [alerts, setAlerts] = useState([]);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const config = { headers: { Authorization: `Bearer ${token}` } };
        const res = await axios.get('http://localhost:8000/api/checklist/', config);
        setItems(res.data);

        const updatesRes = await axios.get('http://localhost:8000/api/updates/', config);
        if (updatesRes.data.length > 0) {
          setAlerts([`New regulations added manually from HHS emails! (${updatesRes.data.length} items)`]);
        }
      } catch (error) {
        console.error(error);  // Governance: Log frontend errors to SIEM
      }
    };
    fetchData();
  }, [token]);

  const handleToggle = async (id, completed) => {
    await axios.patch(`http://localhost:8000/api/checklist/${id}/`, { completed: !completed }, { headers: { Authorization: `Bearer ${token}` } });
    setItems(items.map(item => item.id === id ? { ...item, completed: !completed } : item));
  };

  const handleNotes = async (id, notes) => {
    await axios.patch(`http://localhost:8000/api/checklist/${id}/`, { notes }, { headers: { Authorization: `Bearer ${token}` } });
  };

  return (
    <>
      {alerts.map(alert => <Alert severity="info">{alert}</Alert>)}
      <Table>
        <TableHead>
          <TableRow>
            <TableCell>Regulation</TableCell>
            <TableCell>Description</TableCell>
            <TableCell>Completed</TableCell>
            <TableCell>Notes</TableCell>
            <TableCell>Last Updated</TableCell>
          </TableRow>
        </TableHead>
        <TableBody>
          {items.map(item => (
            <TableRow key={item.id}>
              <TableCell>{item.regulation.title}</TableCell>
              <TableCell>{item.regulation.description}</TableCell>
              <TableCell><Checkbox checked={item.completed} onChange={() => handleToggle(item.id, item.completed)} /></TableCell>
              <TableCell><TextField value={item.notes} onBlur={(e) => handleNotes(item.id, e.target.value)} /></TableCell>
              <TableCell>{item.last_updated}</TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </>
  );
}

export default Checklist;