import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { Box, Typography, Button, Table, TableBody, TableCell, TableContainer, TableHead, TableRow, Paper, Alert, Card, CardContent, Grid, Dialog, DialogTitle, DialogContent, DialogContentText } from '@mui/material';

function ChecklistDisplay() {
  const [items, setItems] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [selectedItem, setSelectedItem] = useState(null);
  const [highRiskCount, setHighRiskCount] = useState(0);
  const [overdueCount, setOverdueCount] = useState(0);

  const fetchChecklist = async () => {
    setLoading(true);
    setError(null);
    try {
      const token = localStorage.getItem('token');
      const response = await axios.get('http://localhost:8000/api/checklist/', {
        headers: token ? { Authorization: `Bearer ${token}` } : {},
      });
      setItems(response.data);
      // Calculate KPIs
      const now = new Date();
      const highRisks = response.data.filter(item => !item.completed && new Date(item.last_updated) > new Date(now.getTime() - 30*24*60*60*1000));
      const overdueRisks = response.data.filter(item => !item.completed && new Date(item.last_updated) < new Date(now.getTime() - 60*24*60*60*1000));
      setHighRiskCount(highRisks.length);
      setOverdueCount(overdueRisks.length);
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
    <Box sx={{ p: 2 }}>
      <Typography variant="h4" gutterBottom>Risk Dashboard</Typography>
      <Grid container spacing={2} sx={{ mb: 2 }}>
        <Grid item xs={12} sm={6} md={3}>
          <Card>
            <CardContent>
              <Typography variant="h6">Total Risks</Typography>
              <Typography variant="h5">{items.length}</Typography>
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <Card>
            <CardContent>
              <Typography variant="h6">High Risks</Typography>
              <Typography variant="h5" color={highRiskCount > 0 ? 'error' : 'textPrimary'}>{highRiskCount}</Typography>
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <Card>
            <CardContent>
              <Typography variant="h6">Overdue Risks</Typography>
              <Typography variant="h5" color={overdueCount > 0 ? 'error' : 'textPrimary'}>{overdueCount}</Typography>
            </CardContent>
          </Card>
        </Grid>
      </Grid>
      {highRiskCount > 0 && <Alert severity="error" sx={{ mb: 2 }}>High risks detected: {highRiskCount} incomplete recent items!</Alert>}
      {overdueCount > 0 && <Alert severity="warning" sx={{ mb: 2 }}>Overdue risks detected: {overdueCount} items not updated in 60+ days!</Alert>}
      <Typography variant="h5" gutterBottom>Checklist Items</Typography>
      <Button onClick={fetchChecklist} variant="outlined" sx={{ mb: 2 }}>Refresh</Button>
      {items.length === 0 ? (
        <div>No checklist items found.</div>
      ) : (
        <TableContainer component={Paper}>
          <Table>
            <TableHead>
              <TableRow>
                <TableCell>User</TableCell>
                <TableCell>Regulation</TableCell>
                <TableCell>Completed</TableCell>
                <TableCell>Notes</TableCell>
                <TableCell>Last Updated</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {items.map(item => (
                <TableRow key={item.id} hover onClick={() => setSelectedItem(item)} style={{ cursor: 'pointer' }}>
                  <TableCell>{item.user}</TableCell>
                  <TableCell>{item.regulation_update}</TableCell>
                  <TableCell>{item.completed ? 'Yes' : 'No'}</TableCell>
                  <TableCell>{item.notes}</TableCell>
                  <TableCell>{item.last_updated}</TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </TableContainer>
      )}
      <Dialog open={!!selectedItem} onClose={() => setSelectedItem(null)}>
        <DialogTitle>Risk Details</DialogTitle>
        <DialogContent>
          {selectedItem && (
            <DialogContentText>
              <strong>User:</strong> {selectedItem.user}<br/>
              <strong>Regulation:</strong> {selectedItem.regulation_update}<br/>
              <strong>Completed:</strong> {selectedItem.completed ? 'Yes' : 'No'}<br/>
              <strong>Notes:</strong> {selectedItem.notes}<br/>
              <strong>Last Updated:</strong> {selectedItem.last_updated}<br/>
            </DialogContentText>
          )}
        </DialogContent>
      </Dialog>
    </Box>
  );
}

export default ChecklistDisplay; 