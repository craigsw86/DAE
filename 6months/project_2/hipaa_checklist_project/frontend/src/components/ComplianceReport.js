import React, { useEffect, useState, useMemo } from 'react';
import axios from 'axios';
import { Card, CardContent, Typography, Table, TableBody, TableCell, TableContainer, TableHead, TableRow, Paper, Box, CircularProgress, Alert, Tooltip, Chip, Stack, Button, MenuItem, Select, FormControl, InputLabel, IconButton } from '@mui/material';
import RefreshIcon from '@mui/icons-material/Refresh';
import DownloadIcon from '@mui/icons-material/Download';

const RISK_MATRIX_SIZE = 5;
const riskColors = [
  ['#e0f7fa', '#b2ebf2', '#80deea', '#4dd0e1', '#26c6da'], // Low
  ['#fffde7', '#fff9c4', '#fff59d', '#fff176', '#ffee58'], // Moderate
  ['#f1f8e9', '#dcedc8', '#c5e1a5', '#aed581', '#9ccc65'], // Moderate-High
  ['#fff3e0', '#ffe0b2', '#ffcc80', '#ffb74d', '#ffa726'], // High
  ['#ffebee', '#ffcdd2', '#ef9a9a', '#e57373', '#ef5350'], // Critical
];

function RiskMatrix({ risks, isAdmin }) {
  const grid = Array.from({ length: RISK_MATRIX_SIZE }, () =>
    Array.from({ length: RISK_MATRIX_SIZE }, () => [])
  );
  risks.forEach(risk => {
    const l = Math.max(1, Math.min(RISK_MATRIX_SIZE, risk.likelihood));
    const i = Math.max(1, Math.min(RISK_MATRIX_SIZE, risk.impact));
    grid[RISK_MATRIX_SIZE - l][i - 1].push(risk);
  });
  return (
    <Box sx={{ mt: 4, mb: 2 }}>
      <Typography variant="h6" gutterBottom>Risk Matrix (Likelihood vs. Impact)</Typography>
      <TableContainer component={Paper} sx={{ maxWidth: 500 }}>
        <Table size="small">
          <TableHead>
            <TableRow>
              <TableCell></TableCell>
              {[...Array(RISK_MATRIX_SIZE)].map((_, i) => (
                <TableCell key={i} align="center">Impact {i + 1}</TableCell>
              ))}
            </TableRow>
          </TableHead>
          <TableBody>
            {[...Array(RISK_MATRIX_SIZE)].map((_, row) => (
              <TableRow key={row}>
                <TableCell>Likelihood {RISK_MATRIX_SIZE - row}</TableCell>
                {[...Array(RISK_MATRIX_SIZE)].map((_, col) => (
                  <TableCell key={col} style={{ background: riskColors[row][col], height: 48, width: 48, padding: 0 }} align="center">
                    <Stack direction="column" spacing={0.5} alignItems="center">
                      {grid[row][col].map(risk => (
                        <Tooltip key={risk.id} title={
                          <Box>
                            <Typography variant="subtitle2">{risk.regulation}</Typography>
                            <Typography variant="body2">{risk.completed ? 'Completed' : 'Incomplete'}</Typography>
                            {risk.notes && <Typography variant="caption">Notes: {risk.notes}</Typography>}
                            {isAdmin && risk.admin_notes && <Typography variant="caption" color="secondary">Admin: {risk.admin_notes}</Typography>}
                          </Box>
                        } placement="top" arrow>
                          <Chip
                            label={risk.regulation}
                            color={risk.completed ? 'success' : 'warning'}
                            size="small"
                            sx={{ maxWidth: 80, fontSize: 10 }}
                          />
                        </Tooltip>
                      ))}
                    </Stack>
                  </TableCell>
                ))}
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>
    </Box>
  );
}

function downloadCSV(risks) {
  const header = ['Regulation', 'Status', 'Likelihood', 'Impact', 'Notes'];
  const rows = risks.map(r => [
    r.regulation,
    r.completed ? 'Completed' : 'Incomplete',
    r.likelihood,
    r.impact,
    r.notes || ''
  ]);
  const csv = [header, ...rows].map(row => row.map(field => `"${String(field).replace(/"/g, '""')}"`).join(',')).join('\r\n');
  const blob = new Blob([csv], { type: 'text/csv' });
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = 'compliance_report.csv';
  document.body.appendChild(a);
  a.click();
  document.body.removeChild(a);
  URL.revokeObjectURL(url);
}

const likelihoodOptions = [1, 2, 3, 4, 5];
const impactOptions = [1, 2, 3, 4, 5];

export default function ComplianceReport() {
  const [report, setReport] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [filters, setFilters] = useState({ status: '', likelihood: '', impact: '' });
  const [sort, setSort] = useState({ field: '', order: 'asc' });
  // For demo: treat user as admin if localStorage.getItem('is_staff') === 'true'
  const isAdmin = localStorage.getItem('is_staff') === 'true' || localStorage.getItem('is_superuser') === 'true';

  const fetchReport = async () => {
    setLoading(true);
    setError(null);
    try {
      const token = localStorage.getItem('token');
      if (!token) {
        setError('Authentication token not found. Please log in again.');
        return;
      }
      
      const res = await axios.get('http://localhost:8000/api/report/', {
        headers: { Authorization: `Bearer ${token}` },
        timeout: 10000, // 10 second timeout
      });
      
      if (res.data && res.data.risks) {
        setReport(res.data);
      } else {
        setError('Invalid response format from server.');
      }
    } catch (err) {
      if (err.response) {
        // Server responded with error status
        if (err.response.status === 401) {
          setError('Authentication failed. Please log in again.');
        } else if (err.response.status === 500) {
          setError('Server error. Please try again later.');
        } else {
          setError(`Request failed: ${err.response.status}`);
        }
      } else if (err.request) {
        // Network error
        setError('Network error. Please check your connection and try again.');
      } else {
        // Other error
        setError('An unexpected error occurred. Please try again.');
      }
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchReport();
    // eslint-disable-next-line
  }, []);

  // Optimized filtering and sorting with useMemo
  const filteredRisks = useMemo(() => {
    if (!report || !report.risks) return [];
    
    let filtered = report.risks.filter(risk => {
      if (filters.status === 'completed' && !risk.completed) return false;
      if (filters.status === 'incomplete' && risk.completed) return false;
      if (filters.likelihood && String(risk.likelihood) !== String(filters.likelihood)) return false;
      if (filters.impact && String(risk.impact) !== String(filters.impact)) return false;
      return true;
    });
    
    // Sorting
    if (sort.field) {
      filtered = [...filtered].sort((a, b) => {
        let aVal = a[sort.field];
        let bVal = b[sort.field];
        if (sort.field === 'regulation' || sort.field === 'notes' || sort.field === 'admin_notes') {
          aVal = aVal ? aVal.toLowerCase() : '';
          bVal = bVal ? bVal.toLowerCase() : '';
        }
        if (aVal < bVal) return sort.order === 'asc' ? -1 : 1;
        if (aVal > bVal) return sort.order === 'asc' ? 1 : -1;
        return 0;
      });
    }
    
    return filtered;
  }, [report, filters, sort]);

  if (loading) return <Box sx={{ display: 'flex', justifyContent: 'center', mt: 4 }}><CircularProgress /></Box>;
  if (error) return <Alert severity="error">{error}</Alert>;
  if (!report) return null;

  const handleFilterChange = (field, value) => {
    setFilters(f => ({ ...f, [field]: value }));
  };
  const handleSort = (field) => {
    setSort(s => ({
      field,
      order: s.field === field ? (s.order === 'asc' ? 'desc' : 'asc') : 'asc',
    }));
  };

  return (
    <Box>
      <Card sx={{ mb: 4 }}>
        <CardContent>
          <Typography variant="h5" gutterBottom>Compliance Report</Typography>
          <TableContainer component={Paper} sx={{ maxWidth: 500 }}>
            <Table>
              <TableBody>
                <TableRow>
                  <TableCell>User</TableCell>
                  <TableCell>{report.user}</TableCell>
                </TableRow>
                <TableRow>
                  <TableCell>Total Checklist Items</TableCell>
                  <TableCell>{report.total_items}</TableCell>
                </TableRow>
                <TableRow>
                  <TableCell>Completed Items</TableCell>
                  <TableCell>{report.completed_items}</TableCell>
                </TableRow>
                <TableRow>
                  <TableCell>Completion %</TableCell>
                  <TableCell>{report.completion_percentage}%</TableCell>
                </TableRow>
              </TableBody>
            </Table>
          </TableContainer>
          <Box sx={{ mt: 2, display: 'flex', gap: 2, flexWrap: 'wrap', alignItems: 'center' }}>
            <FormControl size="small" sx={{ minWidth: 120 }}>
              <InputLabel>Status</InputLabel>
              <Select
                value={filters.status}
                label="Status"
                onChange={e => handleFilterChange('status', e.target.value)}
              >
                <MenuItem value="">All</MenuItem>
                <MenuItem value="completed">Completed</MenuItem>
                <MenuItem value="incomplete">Incomplete</MenuItem>
              </Select>
            </FormControl>
            <FormControl size="small" sx={{ minWidth: 120 }}>
              <InputLabel>Likelihood</InputLabel>
              <Select
                value={filters.likelihood}
                label="Likelihood"
                onChange={e => handleFilterChange('likelihood', e.target.value)}
              >
                <MenuItem value="">All</MenuItem>
                {likelihoodOptions.map(l => <MenuItem key={l} value={l}>{l}</MenuItem>)}
              </Select>
            </FormControl>
            <FormControl size="small" sx={{ minWidth: 120 }}>
              <InputLabel>Impact</InputLabel>
              <Select
                value={filters.impact}
                label="Impact"
                onChange={e => handleFilterChange('impact', e.target.value)}
              >
                <MenuItem value="">All</MenuItem>
                {impactOptions.map(i => <MenuItem key={i} value={i}>{i}</MenuItem>)}
              </Select>
            </FormControl>
            <Button variant="outlined" onClick={() => setFilters({ status: '', likelihood: '', impact: '' })}>Clear Filters</Button>
            <IconButton onClick={fetchReport} title="Refresh"><RefreshIcon /></IconButton>
            <Button variant="outlined" startIcon={<DownloadIcon />} onClick={() => downloadCSV(filteredRisks)}>Export CSV</Button>
          </Box>
        </CardContent>
      </Card>
      <RiskMatrix risks={filteredRisks} isAdmin={isAdmin} />
      <Box sx={{ mt: 4 }}>
        <Typography variant="h6" gutterBottom>Risks Table</Typography>
        <TableContainer component={Paper}>
          <Table size="small">
            <TableHead>
              <TableRow>
                {[
                  { field: 'regulation', label: 'Regulation' },
                  { field: 'completed', label: 'Status' },
                  { field: 'likelihood', label: 'Likelihood' },
                  { field: 'impact', label: 'Impact' },
                  { field: 'notes', label: 'Notes' },
                  ...(isAdmin ? [{ field: 'admin_notes', label: 'Admin Notes' }] : []),
                ].map(col => (
                  <TableCell key={col.field} onClick={() => handleSort(col.field)} style={{ cursor: 'pointer', fontWeight: 'bold' }}>
                    {col.label}
                    {sort.field === col.field ? (sort.order === 'asc' ? ' ' : ' ') : ''}
                  </TableCell>
                ))}
              </TableRow>
            </TableHead>
            <TableBody>
              {filteredRisks.length === 0 ? (
                <TableRow><TableCell colSpan={isAdmin ? 6 : 5}>No risks match the selected filters.</TableCell></TableRow>
              ) : filteredRisks.map(risk => (
                <TableRow key={risk.id} className={risk.completed ? 'completed' : 'incomplete'}>
                  <TableCell>{risk.regulation}</TableCell>
                  <TableCell>{risk.completed ? 'Completed' : 'Incomplete'}</TableCell>
                  <TableCell>{risk.likelihood}</TableCell>
                  <TableCell>{risk.impact}</TableCell>
                  <TableCell>{risk.notes || '-'}</TableCell>
                  {isAdmin && <TableCell>{risk.admin_notes || '-'}</TableCell>}
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </TableContainer>
      </Box>
    </Box>
  );
}
