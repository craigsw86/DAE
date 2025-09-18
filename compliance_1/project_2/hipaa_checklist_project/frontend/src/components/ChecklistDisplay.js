import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { Box, Typography, Button, Table, TableBody, TableCell, TableContainer, TableHead, TableRow, Paper, Alert, Card, CardContent, Grid, Dialog, DialogTitle, DialogContent, DialogContentText, Checkbox, CircularProgress, IconButton, TextField, DialogActions, Snackbar, Tooltip } from '@mui/material';
import EditIcon from '@mui/icons-material/Edit';
import { Tooltip as MuiTooltip } from '@mui/material';
import { Line } from 'react-chartjs-2';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip as ChartTooltip,
  Legend
} from 'chart.js';
ChartJS.register(CategoryScale, LinearScale, PointElement, LineElement, Title, ChartTooltip, Legend);

// Utility to parse API errors
function parseApiError(err) {
  if (err.response) {
    if (err.response.status === 401) {
      return 'Session expired or unauthorized. Please log in again.';
    } else if (err.response.status === 400 && typeof err.response.data === 'object') {
      return Object.entries(err.response.data)
        .map(([field, msgs]) => `${field}: ${Array.isArray(msgs) ? msgs.join(', ') : msgs}`)
        .join(' ');
    } else if (err.response.data && err.response.data.detail) {
      return err.response.data.detail;
    } else {
      return 'Request failed. Please try again.';
    }
  } else if (err.request) {
    return 'Network error. Please check your connection.';
  } else {
    return 'An unexpected error occurred.';
  }
}

// Helper for CSV export
function exportToCSV(data, filename) {
  const replacer = (key, value) => (value === null ? '' : value);
  const header = Object.keys(data[0] || {});
  const csv = [
    header.join(','),
    ...data.map(row => header.map(fieldName => JSON.stringify(row[fieldName], replacer)).join(','))
  ].join('\r\n');
  const blob = new Blob([csv], { type: 'text/csv' });
  const link = document.createElement('a');
  link.href = URL.createObjectURL(blob);
  link.download = filename;
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
}
// Helper for JSON export
function exportToJSON(data, filename) {
  const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
  const link = document.createElement('a');
  link.href = URL.createObjectURL(blob);
  link.download = filename;
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
}

// Mask sensitive fields
const SENSITIVE_FIELDS = ['notes', 'admin_notes', 'mitigation_steps'];
function maskChange(field, change) {
  if (SENSITIVE_FIELDS.includes(field)) {
    return <i>Changed (value hidden)</i>;
  }
  if (Array.isArray(change) && change.length === 2) {
    return <span><b style={{color:'#b71c1c'}}>{change[0]}</b> → <b style={{color:'#1b5e20'}}>{change[1]}</b></span>;
  }
  return Array.isArray(change) ? change.join(' → ') : change;
}

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
  const [retry, setRetry] = useState(false);
  // Add mitigationSteps state for editing
  const [editingMitigationItem, setEditingMitigationItem] = useState(null);
  const [mitigationValue, setMitigationValue] = useState('');
  const [mitigationUpdating, setMitigationUpdating] = useState(false);
  const [auditLogOpen, setAuditLogOpen] = useState(false);
  const [auditLogLoading, setAuditLogLoading] = useState(false);
  const [auditLog, setAuditLog] = useState([]);
  const [auditLogError, setAuditLogError] = useState('');
  const [regAuditLogOpen, setRegAuditLogOpen] = useState(false);
  const [regAuditLogLoading, setRegAuditLogLoading] = useState(false);
  const [regAuditLog, setRegAuditLog] = useState([]);
  const [regAuditLogError, setRegAuditLogError] = useState('');
  const [userProfile, setUserProfile] = useState(null);
  const [profileOpen, setProfileOpen] = useState(false);
  const [profileForm, setProfileForm] = useState({ first_name: '', last_name: '', email: '' });
  const [profileMsg, setProfileMsg] = useState('');
  const [trendData, setTrendData] = useState([]);
  const [trendLoading, setTrendLoading] = useState(false);
  const [trendError, setTrendError] = useState('');

  // Filtering/search state for audit logs
  const [auditLogFilter, setAuditLogFilter] = useState('');
  const [auditLogSearch, setAuditLogSearch] = useState('');
  const [auditLogPage, setAuditLogPage] = useState(0);
  const AUDIT_LOG_PAGE_SIZE = 10;

  const fetchChecklist = async () => {
    setLoading(true);
    setError(null);
    setRetry(false);
    try {
      const token = localStorage.getItem('token');
      const response = await axios.get(`${process.env.REACT_APP_API_BASE_URL || 'http://localhost:8000'}/api/checklist/`, {
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
      setError(parseApiError(err));
      if (err.request && !err.response) setRetry(true);
      if (err.response && err.response.status === 401) {
        localStorage.removeItem('token');
        setTimeout(() => window.location.reload(), 2000);
      }
    } finally {
      setLoading(false);
    }
  };

  const handleToggleCompleted = async (item) => {
    setUpdatingId(item.id);
    setRetry(false);
    try {
      const token = localStorage.getItem('token');
      await axios.patch(`${process.env.REACT_APP_API_BASE_URL || 'http://localhost:8000'}/api/checklist/${item.id}/`, {
        completed: !item.completed
      }, {
        headers: token ? { Authorization: `Bearer ${token}` } : {},
      });
      await fetchChecklist();
    } catch (err) {
      setError(parseApiError(err));
      if (err.request && !err.response) setRetry(true);
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
    setRetry(false);
    try {
      const token = localStorage.getItem('token');
      await axios.patch(`${process.env.REACT_APP_API_BASE_URL || 'http://localhost:8000'}/api/checklist/${editingNotesItem.id}/`, {
        notes: notesValue
      }, {
        headers: token ? { Authorization: `Bearer ${token}` } : {},
      });
      setEditingNotesItem(null);
      setNotesValue('');
      setSnackbarOpen(true);
      await fetchChecklist();
    } catch (err) {
      setError(parseApiError(err));
      if (err.request && !err.response) setRetry(true);
    } finally {
      setNotesUpdating(false);
    }
  };

  const handleEditMitigation = (item) => {
    setEditingMitigationItem(item);
    setMitigationValue(item.mitigation_steps || '');
  };

  const handleSaveMitigation = async () => {
    if (!editingMitigationItem) return;
    setMitigationUpdating(true);
    setRetry(false);
    try {
      const token = localStorage.getItem('token');
      await axios.patch(`${process.env.REACT_APP_API_BASE_URL || 'http://localhost:8000'}/api/checklist/${editingMitigationItem.id}/`, {
        mitigation_steps: mitigationValue
      }, {
        headers: token ? { Authorization: `Bearer ${token}` } : {},
      });
      setEditingMitigationItem(null);
      setMitigationValue('');
      setSnackbarOpen(true);
      await fetchChecklist();
    } catch (err) {
      setError(parseApiError(err));
      if (err.request && !err.response) setRetry(true);
    } finally {
      setMitigationUpdating(false);
    }
  };

  const fetchAuditLog = async (item) => {
    setAuditLogLoading(true);
    setAuditLogError('');
    setAuditLog([]);
    try {
      const token = localStorage.getItem('token');
      const response = await axios.get(`${process.env.REACT_APP_API_BASE_URL || 'http://localhost:8000'}/api/auditlog/checklistitem/${item.id}/`, {
        headers: token ? { Authorization: `Bearer ${token}` } : {},
      });
      setAuditLog(response.data);
    } catch (err) {
      setAuditLogError(parseApiError(err));
    } finally {
      setAuditLogLoading(false);
    }
  };

  const fetchRegAuditLog = async (regulationId) => {
    setRegAuditLogLoading(true);
    setRegAuditLogError('');
    setRegAuditLog([]);
    try {
      const token = localStorage.getItem('token');
      const response = await axios.get(`${process.env.REACT_APP_API_BASE_URL || 'http://localhost:8000'}/api/auditlog/regulationupdate/${regulationId}/`, {
        headers: token ? { Authorization: `Bearer ${token}` } : {},
      });
      setRegAuditLog(response.data);
    } catch (err) {
      setRegAuditLogError(parseApiError(err));
    } finally {
      setRegAuditLogLoading(false);
    }
  };

  const fetchTrendData = async () => {
    setTrendLoading(true);
    setTrendError('');
    try {
      const token = localStorage.getItem('token');
      const res = await axios.get(`${process.env.REACT_APP_API_BASE_URL || 'http://localhost:8000'}/api/report/trends/`, {
        headers: token ? { Authorization: `Bearer ${token}` } : {},
      });
      setTrendData(res.data);
    } catch (err) {
      setTrendError(parseApiError(err));
    } finally {
      setTrendLoading(false);
    }
  };

  useEffect(() => {
    fetchChecklist();
    fetchTrendData();
  }, []);

  useEffect(() => {
    if (error) {
      const timer = setTimeout(() => setError(null), 5000);
      return () => clearTimeout(timer);
    }
  }, [error]);

  // Reset pagination when filters change
  useEffect(() => {
    setAuditLogPage(0);
  }, [auditLogFilter, auditLogSearch]);

  useEffect(() => {
    const fetchProfile = async () => {
      try {
        const token = localStorage.getItem('token');
        const res = await axios.get(`${process.env.REACT_APP_API_BASE_URL || 'http://localhost:8000'}/api/profile/`, {
          headers: token ? { Authorization: `Bearer ${token}` } : {},
        });
        setUserProfile(res.data);
        setProfileForm({
          first_name: res.data.first_name || '',
          last_name: res.data.last_name || '',
          email: res.data.email || '',
        });
      } catch {}
    };
    fetchProfile();
  }, []);

  if (loading) return <div>Loading checklist...</div>;
  if (error) return <div style={{color: 'red'}}>{error}</div>;

  const handleExportCSV = () => {
    window.open(`${process.env.REACT_APP_API_BASE_URL || 'http://localhost:8000'}/api/checklist/export/csv/`, '_blank');
  };
  const handleExportPDF = () => {
    window.open(`${process.env.REACT_APP_API_BASE_URL || 'http://localhost:8000'}/api/checklist/export/pdf/`, '_blank');
  };

  const handleProfileSave = async () => {
    try {
      const token = localStorage.getItem('token');
      const response = await axios.put(`${process.env.REACT_APP_API_BASE_URL || 'http://localhost:8000'}/api/profile/`, profileForm, {
        headers: token ? { Authorization: `Bearer ${token}` } : {},
      });
      setUserProfile(response.data);
      setProfileMsg('Profile updated successfully!');
      setTimeout(() => setProfileMsg(''), 3000);
    } catch (err) {
      setProfileMsg(parseApiError(err));
    }
  };

  // Responsive table container style
  const tableContainerSx = { maxHeight: { xs: 300, sm: 500 }, overflowX: 'auto' };

  // Compute filtered and paged audit log data
  const filteredAuditLog = auditLog.filter(entry => {
    if (auditLogFilter && entry.action !== auditLogFilter) return false;
    if (auditLogSearch) {
      const searchLower = auditLogSearch.toLowerCase();
      return (
        (entry.actor && entry.actor.toLowerCase().includes(searchLower)) ||
        (entry.action && entry.action.toLowerCase().includes(searchLower)) ||
        (entry.changes && JSON.stringify(entry.changes).toLowerCase().includes(searchLower))
      );
    }
    return true;
  });

  const pagedAuditLog = filteredAuditLog.slice(
    auditLogPage * AUDIT_LOG_PAGE_SIZE,
    (auditLogPage + 1) * AUDIT_LOG_PAGE_SIZE
  );

  return (
    <Box sx={{ p: { xs: 1, sm: 2 } }}>
      <Box sx={{ display: 'flex', flexDirection: { xs: 'column', sm: 'row' }, justifyContent: 'space-between', alignItems: { xs: 'stretch', sm: 'center' }, mb: 2 }}>
        <Typography variant="h4" gutterBottom sx={{ fontSize: { xs: '1.5rem', sm: '2.125rem' } }}>Risk Dashboard</Typography>
        <Box sx={{ mt: { xs: 1, sm: 0 }, display: 'flex', gap: 1 }}>
          {userProfile && userProfile.is_staff && (
            <MuiTooltip title="Admin user: can view all checklist items">
              <Button color="secondary" variant="outlined" sx={{ mr: 2 }} aria-label="Admin badge">Admin</Button>
            </MuiTooltip>
          )}
          <Button onClick={() => setProfileOpen(true)} variant="outlined" aria-label="Open user profile">Profile</Button>
        </Box>
      </Box>
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
      {highRiskCount > 0 && <Alert severity="error" sx={{ mb: 2 }} role="alert">High risks detected: {highRiskCount} incomplete recent items!</Alert>}
      {overdueCount > 0 && <Alert severity="warning" sx={{ mb: 2 }} role="alert">Overdue risks detected: {overdueCount} items not updated in 60+ days!</Alert>}
      <Typography variant="h5" gutterBottom>Checklist Items</Typography>
      <Button onClick={fetchChecklist} variant="outlined" sx={{ mb: 2 }} disabled={loading}>
        {loading ? 'Refreshing...' : 'Refresh'}
      </Button>
      {retry && (
        <Button
          variant="outlined"
          color="secondary"
          sx={{ mb: 2, ml: 2 }}
          onClick={fetchChecklist}
          disabled={loading}
        >
          Retry
        </Button>
      )}
      <Box sx={{ display: 'flex', gap: 2, mb: 2, flexWrap: 'wrap' }}>
        <Button onClick={handleExportCSV} variant="outlined" aria-label="Export checklist as CSV">Export CSV</Button>
        <Button onClick={handleExportPDF} variant="outlined" aria-label="Export checklist as PDF">Export PDF</Button>
      </Box>
      <Box sx={{ mb: 4 }}>
        <Typography variant="h6" sx={{ mb: 1, fontSize: { xs: '1rem', sm: '1.25rem' } }}>Risk/Compliance Trends</Typography>
        {trendLoading ? (
          <CircularProgress aria-label="Loading trend data" />
        ) : trendError ? (
          <Alert severity="error" role="alert">{trendError}</Alert>
        ) : trendData.length === 0 ? (
          <div>No trend data available.</div>
        ) : (
          <Box sx={{ maxWidth: '100vw', overflowX: 'auto' }}>
            <Line
              data={{
                labels: trendData.map(d => d.month),
                datasets: [
                  {
                    label: 'Completed',
                    data: trendData.map(d => d.completed),
                    borderColor: '#388e3c',
                    backgroundColor: 'rgba(56,142,60,0.2)',
                    tension: 0.2,
                  },
                  {
                    label: 'Incomplete',
                    data: trendData.map(d => d.incomplete),
                    borderColor: '#d32f2f',
                    backgroundColor: 'rgba(211,47,47,0.2)',
                    tension: 0.2,
                  },
                ],
              }}
              options={{
                responsive: true,
                plugins: {
                  legend: { position: 'top' },
                  title: { display: false },
                },
                maintainAspectRatio: false,
              }}
              height={200}
              aria-label="Risk and compliance trend chart"
            />
          </Box>
        )}
      </Box>
      {items.length === 0 ? (
        <div>No checklist items found.</div>
      ) : (
        <TableContainer component={Paper} sx={tableContainerSx} aria-label="Checklist items table">
          <Table size="small" stickyHeader>
            <TableHead>
              <TableRow>
                <TableCell>User</TableCell>
                <TableCell>Regulation</TableCell>
                <TableCell>Completed</TableCell>
                <TableCell>Notes</TableCell>
                <TableCell>Mitigation Steps</TableCell>
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
                      <IconButton size="small" onClick={() => handleEditNotes(item)} sx={{ ml: 1 }} aria-label="Edit notes">
                        <EditIcon fontSize="small" />
                      </IconButton>
                    </Tooltip>
                  </TableCell>
                  <TableCell onClick={e => e.stopPropagation()}>
                    {item.mitigation_steps}
                    <Tooltip title="Edit mitigation steps">
                      <IconButton size="small" onClick={() => handleEditMitigation(item)} sx={{ ml: 1 }} aria-label="Edit mitigation steps">
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
      {error && <Alert severity="error" sx={{ mb: 2 }} role="alert">{error}</Alert>}
      <Dialog open={!!selectedItem} onClose={() => setSelectedItem(null)} aria-labelledby="risk-details-title" fullWidth maxWidth="sm" scroll="body">
        <DialogTitle id="risk-details-title">Risk Details</DialogTitle>
        <DialogContent dividers>
          {selectedItem && (
            <DialogContentText>
              <strong>User:</strong> {selectedItem.user}<br/>
              <strong>Regulation:</strong> {selectedItem.regulation_update}<br/>
              <strong>Completed:</strong> {selectedItem.completed ? 'Yes' : 'No'}<br/>
              <strong>Notes:</strong> {selectedItem.notes}<br/>
              <strong>Mitigation Steps:</strong> {selectedItem.mitigation_steps}<br/>
              <strong>Last Updated:</strong> {selectedItem.last_updated}<br/>
            </DialogContentText>
          )}
          <Button
            variant="outlined"
            sx={{ mt: 2 }}
            onClick={() => {
              setAuditLogOpen(true);
              fetchAuditLog(selectedItem);
            }}
          >
            View Audit Log
          </Button>
          {selectedItem && selectedItem.regulation_update_id && (
            <Button
              variant="outlined"
              sx={{ mt: 2, ml: 2 }}
              onClick={() => {
                setRegAuditLogOpen(true);
                fetchRegAuditLog(selectedItem.regulation_update_id);
              }}
            >
              View Regulation Audit Log
            </Button>
          )}
        </DialogContent>
      </Dialog>
      <Dialog open={!!editingNotesItem} onClose={() => setEditingNotesItem(null)} aria-labelledby="edit-notes-title" fullWidth maxWidth="sm" scroll="body">
        <DialogTitle id="edit-notes-title">Edit Notes</DialogTitle>
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
      <Dialog open={!!editingMitigationItem} onClose={() => setEditingMitigationItem(null)} aria-labelledby="edit-mitigation-title" fullWidth maxWidth="sm" scroll="body">
        <DialogTitle id="edit-mitigation-title">Edit Mitigation Steps</DialogTitle>
        <DialogContent>
          <TextField
            label="Mitigation Steps"
            multiline
            minRows={3}
            value={mitigationValue}
            onChange={e => setMitigationValue(e.target.value)}
            fullWidth
            autoFocus
          />
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setEditingMitigationItem(null)} disabled={mitigationUpdating}>Cancel</Button>
          <Button onClick={handleSaveMitigation} variant="contained" disabled={mitigationUpdating}>
            {mitigationUpdating ? <CircularProgress size={20} /> : 'Save'}
          </Button>
        </DialogActions>
      </Dialog>
      <Snackbar
        open={snackbarOpen}
        autoHideDuration={3000}
        onClose={() => setSnackbarOpen(false)}
        message="Notes updated successfully!"
        anchorOrigin={{ vertical: 'bottom', horizontal: 'center' }}
        role="status"
      />
      <Dialog open={auditLogOpen} onClose={() => setAuditLogOpen(false)} maxWidth="md" fullWidth aria-labelledby="audit-log-title" scroll="body">
        <DialogTitle id="audit-log-title">Audit Log</DialogTitle>
        <DialogContent>
          <Box sx={{ display: 'flex', gap: 2, mb: 2, flexWrap: 'wrap' }}>
            <TextField
              label="Search actor/field"
              size="small"
              value={auditLogSearch}
              onChange={e => { setAuditLogSearch(e.target.value); setAuditLogPage(0); }}
              sx={{ minWidth: 180 }}
            />
            <TextField
              label="Action"
              size="small"
              select
              SelectProps={{ native: true }}
              value={auditLogFilter}
              onChange={e => { setAuditLogFilter(e.target.value); setAuditLogPage(0); }}
              sx={{ minWidth: 120 }}
            >
              <option value="">All</option>
              <option value="Create">Create</option>
              <option value="Update">Update</option>
              <option value="Delete">Delete</option>
            </TextField>
            <Button onClick={() => exportToCSV(filteredAuditLog, 'audit_log.csv')} size="small" variant="outlined">Export CSV</Button>
            <Button onClick={() => exportToJSON(filteredAuditLog, 'audit_log.json')} size="small" variant="outlined">Export JSON</Button>
          </Box>
          {auditLogLoading ? (
            <CircularProgress />
          ) : auditLogError ? (
            <Alert severity="error">{auditLogError}</Alert>
          ) : filteredAuditLog.length === 0 ? (
            <div>No audit log entries found.</div>
          ) : (
            <TableContainer component={Paper} sx={{ mt: 2 }}>
              <Table size="small">
                <TableHead>
                  <TableRow>
                    <TableCell>Timestamp</TableCell>
                    <TableCell>Actor</TableCell>
                    <TableCell>
                      <MuiTooltip title="Create: new object; Update: field change; Delete: removed object">
                        <span>Action</span>
                      </MuiTooltip>
                    </TableCell>
                    <TableCell>Changes</TableCell>
                    <TableCell>Remote Addr</TableCell>
                  </TableRow>
                </TableHead>
                <TableBody>
                  {pagedAuditLog.map((entry, idx) => (
                    <TableRow key={idx}>
                      <TableCell>{new Date(entry.timestamp).toLocaleString()}</TableCell>
                      <TableCell>{entry.actor || 'System'}</TableCell>
                      <TableCell>{entry.action}</TableCell>
                      <TableCell>
                        {entry.changes && Object.entries(entry.changes).length > 0 ? (
                          <ul style={{ margin: 0, paddingLeft: 16 }}>
                            {Object.entries(entry.changes).map(([field, change]) => (
                              <li key={field}><strong>{field}:</strong> {maskChange(field, change)}</li>
                            ))}
                          </ul>
                        ) : '—'}
                      </TableCell>
                      <TableCell>{entry.remote_addr || '—'}</TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </TableContainer>
          )}
          {filteredAuditLog.length > AUDIT_LOG_PAGE_SIZE && (
            <Box sx={{ display: 'flex', justifyContent: 'center', mt: 2, gap: 2 }}>
              <Button onClick={() => setAuditLogPage(p => Math.max(0, p - 1))} disabled={auditLogPage === 0}>Prev</Button>
              <Typography variant="body2" sx={{ alignSelf: 'center' }}>
                Page {auditLogPage + 1} of {Math.ceil(filteredAuditLog.length / AUDIT_LOG_PAGE_SIZE)}
              </Typography>
              <Button onClick={() => setAuditLogPage(p => p + 1)} disabled={(auditLogPage + 1) * AUDIT_LOG_PAGE_SIZE >= filteredAuditLog.length}>Next</Button>
            </Box>
          )}
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setAuditLogOpen(false)}>Close</Button>
        </DialogActions>
      </Dialog>
      <Dialog open={regAuditLogOpen} onClose={() => setRegAuditLogOpen(false)} maxWidth="md" fullWidth aria-labelledby="reg-audit-log-title" scroll="body">
        <DialogTitle id="reg-audit-log-title">Regulation Update Audit Log</DialogTitle>
        <DialogContent>
          {regAuditLogLoading ? (
            <CircularProgress />
          ) : regAuditLogError ? (
            <Alert severity="error">{regAuditLogError}</Alert>
          ) : regAuditLog.length === 0 ? (
            <div>No audit log entries found.</div>
          ) : (
            <TableContainer component={Paper} sx={{ mt: 2 }}>
              <Table size="small">
                <TableHead>
                  <TableRow>
                    <TableCell>Timestamp</TableCell>
                    <TableCell>Actor</TableCell>
                    <TableCell>Action</TableCell>
                    <TableCell>Changes</TableCell>
                    <TableCell>Remote Addr</TableCell>
                  </TableRow>
                </TableHead>
                <TableBody>
                  {regAuditLog.map((entry, idx) => (
                    <TableRow key={idx}>
                      <TableCell>{new Date(entry.timestamp).toLocaleString()}</TableCell>
                      <TableCell>{entry.actor || 'System'}</TableCell>
                      <TableCell>{entry.action}</TableCell>
                      <TableCell>
                        {entry.changes && Object.entries(entry.changes).length > 0 ? (
                          <ul style={{ margin: 0, paddingLeft: 16 }}>
                            {Object.entries(entry.changes).map(([field, change]) => (
                              <li key={field}><strong>{field}:</strong> {Array.isArray(change) ? change.join(' → ') : change}</li>
                            ))}
                          </ul>
                        ) : '—'}
                      </TableCell>
                      <TableCell>{entry.remote_addr || '—'}</TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </TableContainer>
          )}
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setRegAuditLogOpen(false)}>Close</Button>
        </DialogActions>
      </Dialog>
      <Dialog open={profileOpen} onClose={() => setProfileOpen(false)} aria-labelledby="user-profile-title" fullWidth maxWidth="xs" scroll="body">
        <DialogTitle id="user-profile-title">User Profile</DialogTitle>
        <DialogContent>
          <TextField
            label="First Name"
            value={profileForm.first_name}
            onChange={e => setProfileForm(f => ({ ...f, first_name: e.target.value }))}
            fullWidth
            sx={{ mb: 2 }}
          />
          <TextField
            label="Last Name"
            value={profileForm.last_name}
            onChange={e => setProfileForm(f => ({ ...f, last_name: e.target.value }))}
            fullWidth
            sx={{ mb: 2 }}
          />
          <TextField
            label="Email"
            value={profileForm.email}
            onChange={e => setProfileForm(f => ({ ...f, email: e.target.value }))}
            fullWidth
            sx={{ mb: 2 }}
          />
          {profileMsg && <Alert severity="info">{profileMsg}</Alert>}
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setProfileOpen(false)}>Close</Button>
          <Button onClick={handleProfileSave} variant="contained">Save</Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
}

export default ChecklistDisplay; 