import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { Box, Typography, Button, Table, TableBody, TableCell, TableContainer, TableHead, TableRow, Paper, Alert, Card, CardContent, Grid, Dialog, DialogTitle, DialogContent, DialogContentText, Checkbox, CircularProgress, IconButton, TextField, DialogActions, Snackbar, Tooltip } from '@mui/material';
import EditIcon from '@mui/icons-material/Edit';

function ChecklistDisplay() {
  const [items, setItems] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [selectedItem, setSelectedItem] = useState(null);
  const [highRiskCount, setHighRiskCount] = useState(0);
  const [overdueCount, setOverdueCount] = useState(0);
  const [updatingId, setUpdatingId] = useState(null);
  const [editingNotesItem, setEditingNotesItem] = useState(null);
  const [notesValue, setNotesValue] = useState('');
  const [notesUpdating, setNotesUpdating] = useState(false);
  const [snackbarOpen, setSnackbarOpen] = useState(false);

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

  const handleToggleCompleted = async (item) => {
    setUpdatingId(item.id);
    try {
      const token = localStorage.getItem('token');
      await axios.patch(`http://localhost:8000/api/checklist/${item.id}/`, {
        completed: !item.completed
      }, {
        headers: token ? { Authorization: `Bearer ${token}` } : {},
      });
      await fetchChecklist();
    } catch (err) {
      setError('Failed to update checklist item.');
    } finally {
      setUpdatingId(null);
    }
  };

  const handleEditNotes = (item) => {
    setEditingNotesItem(item);
    setNotesValue(item.notes || '');
  };

  const handleSaveNotes = async () => {
    if (!editingNotesItem) return;
    setNotesUpdating(true);
    try {
      const token = localStorage.getItem('token');
      await axios.patch(`http://localhost:8000/api/checklist/${editingNotesItem.id}/`, {
        notes: notesValue
      }, {
        headers: token ? { Authorization: `Bearer ${token}` } : {},
      });
      setEditingNotesItem(null);
      setNotesValue('');
      setSnackbarOpen(true);
      await fetchChecklist();
    } catch (err) {
      setError('Failed to update notes.');
    } finally {
      setNotesUpdating(false);
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
                  <TableCell onClick={e => e.stopPropagation()}>
                    <Tooltip title="Toggle completed status">
                      <span>
                        <Checkbox
                          checked={!!item.completed}
                          onChange={() => handleToggleCompleted(item)}
                          disabled={updatingId === item.id}
                          color="primary"
                          inputProps={{ 'aria-label': 'Toggle completed' }}
                        />
                        {updatingId === item.id && <CircularProgress size={20} sx={{ ml: 1 }} />}
                      </span>
                    </Tooltip>
                  </TableCell>
                  <TableCell onClick={e => e.stopPropagation()}>
                    {item.notes}
                    <Tooltip title="Edit notes">
                      <IconButton size="small" onClick={() => handleEditNotes(item)} sx={{ ml: 1 }}>
                        <EditIcon fontSize="small" />
                      </IconButton>
                    </Tooltip>
                  </TableCell>
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
      <Dialog open={!!editingNotesItem} onClose={() => setEditingNotesItem(null)}>
        <DialogTitle>Edit Notes</DialogTitle>
        <DialogContent>
          <TextField
            label="Notes"
            multiline
            minRows={3}
            value={notesValue}
            onChange={e => setNotesValue(e.target.value)}
            fullWidth
            autoFocus
          />
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setEditingNotesItem(null)} disabled={notesUpdating}>Cancel</Button>
          <Button onClick={handleSaveNotes} variant="contained" disabled={notesUpdating}>
            {notesUpdating ? <CircularProgress size={20} /> : 'Save'}
          </Button>
        </DialogActions>
      </Dialog>
      <Snackbar
        open={snackbarOpen}
        autoHideDuration={3000}
        onClose={() => setSnackbarOpen(false)}
        message="Notes updated successfully!"
        anchorOrigin={{ vertical: 'bottom', horizontal: 'center' }}
      />
    </Box>
  );
}

export default ChecklistDisplay; 