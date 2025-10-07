import React, { useState, useEffect } from 'react';
import './SecurityDashboard.css';

const SecurityDashboard = () => {
  const [securityData, setSecurityData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [scanning, setScanning] = useState(false);

  // Fetch security report
  const fetchSecurityReport = async () => {
    try {
      setLoading(true);
      setError(null);
      
      const token = localStorage.getItem('access_token');
      const response = await fetch('/api/security/report/', {
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json',
        },
      });

      if (!response.ok) {
        throw new Error('Failed to fetch security report');
      }

      const data = await response.json();
      setSecurityData(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  // Run security scan
  const runSecurityScan = async () => {
    try {
      setScanning(true);
      setError(null);
      
      const token = localStorage.getItem('access_token');
      const response = await fetch('/api/security/scan/', {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json',
        },
      });

      if (!response.ok) {
        throw new Error('Failed to start security scan');
      }

      const data = await response.json();
      alert(`Security scan started successfully! Scan ID: ${data.scan_id}`);
      
      // Refresh the report after a short delay
      setTimeout(() => {
        fetchSecurityReport();
      }, 2000);
    } catch (err) {
      setError(err.message);
    } finally {
      setScanning(false);
    }
  };

  useEffect(() => {
    fetchSecurityReport();
  }, []);

  const getSeverityColor = (severity) => {
    switch (severity.toLowerCase()) {
      case 'critical':
        return '#dc3545';
      case 'high':
        return '#fd7e14';
      case 'medium':
        return '#ffc107';
      case 'low':
        return '#28a745';
      default:
        return '#6c757d';
    }
  };

  const getSeverityIcon = (severity) => {
    switch (severity.toLowerCase()) {
      case 'critical':
        return '';
      case 'high':
        return '🟠';
      case 'medium':
        return '🟡';
      case 'low':
        return '🟢';
      default:
        return '';
    }
  };

  if (loading) {
    return (
      <div className="security-dashboard">
        <div className="loading">
          <div className="spinner"></div>
          <p>Loading security report...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="security-dashboard">
      <div className="security-header">
        <h2>Security Dashboard</h2>
        <div className="security-actions">
          <button 
            onClick={runSecurityScan} 
            disabled={scanning}
            className="scan-button"
          >
            {scanning ? 'Scanning...' : 'Run Security Scan'}
          </button>
          <button 
            onClick={fetchSecurityReport}
            className="refresh-button"
          >
            Refresh
          </button>
        </div>
      </div>

      {error && (
        <div className="error-message">
          <p>Error: {error}</p>
        </div>
      )}

      {securityData && (
        <div className="security-content">
          {securityData.status === 'no_reports' ? (
            <div className="no-reports">
              <h3>No Security Reports Found</h3>
              <p>Run a security scan to analyze your project dependencies for vulnerabilities.</p>
              <button onClick={runSecurityScan} className="scan-button">
                Run First Scan
              </button>
            </div>
          ) : (
            <>
              {/* Summary Cards */}
              <div className="summary-cards">
                <div className="summary-card">
                  <h3>Total Dependencies</h3>
                  <span className="summary-number">
                    {securityData.summary?.total_dependencies || 0}
                  </span>
                </div>
                <div className="summary-card">
                  <h3>Vulnerable Dependencies</h3>
                  <span className="summary-number vulnerable">
                    {securityData.summary?.vulnerable_dependencies || 0}
                  </span>
                </div>
                <div className="summary-card">
                  <h3>High Severity</h3>
                  <span className="summary-number high">
                    {securityData.summary?.high_vulnerabilities || 0}
                  </span>
                </div>
                <div className="summary-card">
                  <h3>Medium Severity</h3>
                  <span className="summary-number medium">
                    {securityData.summary?.medium_vulnerabilities || 0}
                  </span>
                </div>
                <div className="summary-card">
                  <h3>Low Severity</h3>
                  <span className="summary-number low">
                    {securityData.summary?.low_vulnerabilities || 0}
                  </span>
                </div>
              </div>

              {/* Last Scan Info */}
              {securityData.last_scan && (
                <div className="last-scan">
                  <p>Last Scan: {new Date(securityData.last_scan).toLocaleString()}</p>
                </div>
              )}

              {/* Vulnerabilities Table */}
              {securityData.vulnerabilities && securityData.vulnerabilities.length > 0 && (
                <div className="vulnerabilities-section">
                  <h3>Vulnerabilities Found</h3>
                  <div className="vulnerabilities-table">
                    <table>
                      <thead>
                        <tr>
                          <th>ID</th>
                          <th>Severity</th>
                          <th>Component</th>
                          <th>Description</th>
                          <th>CVSS Score</th>
                          <th>Status</th>
                        </tr>
                      </thead>
                      <tbody>
                        {securityData.vulnerabilities.map((vuln, index) => (
                          <tr key={index}>
                            <td className="vuln-id">{vuln.id}</td>
                            <td>
                              <span 
                                className="severity-badge"
                                style={{ backgroundColor: getSeverityColor(vuln.severity) }}
                              >
                                {getSeverityIcon(vuln.severity)} {vuln.severity}
                              </span>
                            </td>
                            <td className="component">{vuln.component}</td>
                            <td className="description">{vuln.description}</td>
                            <td className="cvss-score">{vuln.cvss_score}</td>
                            <td className="status">{vuln.status}</td>
                          </tr>
                        ))}
                      </tbody>
                    </table>
                  </div>
                </div>
              )}

              {/* Dependencies Table */}
              {securityData.dependencies && securityData.dependencies.length > 0 && (
                <div className="dependencies-section">
                  <h3>Dependencies</h3>
                  <div className="dependencies-table">
                    <table>
                      <thead>
                        <tr>
                          <th>Name</th>
                          <th>Version</th>
                          <th>Type</th>
                          <th>Vulnerabilities</th>
                          <th>License</th>
                        </tr>
                      </thead>
                      <tbody>
                        {securityData.dependencies.map((dep, index) => (
                          <tr key={index}>
                            <td className="dep-name">{dep.name}</td>
                            <td className="dep-version">{dep.version}</td>
                            <td className="dep-type">{dep.type}</td>
                            <td className="dep-vulns">
                              {dep.vulnerabilities > 0 ? (
                                <span className="vuln-count">{dep.vulnerabilities}</span>
                              ) : (
                                <span className="no-vulns"></span>
                              )}
                            </td>
                            <td className="dep-license">{dep.license}</td>
                          </tr>
                        ))}
                      </tbody>
                    </table>
                  </div>
                </div>
              )}
            </>
          )}
        </div>
      )}
    </div>
  );
};

export default SecurityDashboard;
