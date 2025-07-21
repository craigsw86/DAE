import React, { useState, useEffect } from 'react';
import { Table, TableBody, TableCell, TableHead, TableRow } from '@mui/material';
import axios from 'axios';

function ComplianceReport({ token }) {
  const [report, setReport] = useState({});

  useEffect(() => {
    const fetchReport = async () => {
      const config = { headers: { Authorization: `Bearer ${token}` } };
      const res = await axios.get('http://localhost:8000/api/report/', config);
      setReport(res.data);
    };
    fetchReport();
  }, [token]);

  return (
    <Table>
      <TableHead>
        <TableRow>
          <TableCell>Username</TableCell>
          <TableCell>Total Items</TableCell>
          <TableCell>Completed Items</TableCell>
          <TableCell>Completion %</TableCell>
        </TableRow>
      </TableHead>
      <TableBody>
        <TableRow>
          <TableCell>{report.username}</TableCell>
          <TableCell>{report.total_items}</TableCell>
          <TableCell>{report.completed_items}</TableCell>
          <TableCell>{report.completion_percentage}%</TableCell>
        </TableRow>
      </TableBody>
    </Table>
  );
}

export default ComplianceReport;