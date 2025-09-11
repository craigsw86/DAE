import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { ThemeProvider, createTheme } from '@mui/material/styles';
import axios from 'axios';
import ChecklistDisplay from '../ChecklistDisplay';

// Mock axios
jest.mock('axios');
const mockedAxios = axios;

// Create a test theme
const testTheme = createTheme();

// Helper function to render component with theme
const renderWithTheme = (component) => {
  return render(
    <ThemeProvider theme={testTheme}>
      {component}
    </ThemeProvider>
  );
};

// Mock audit log data
const mockAuditLogData = [
  {
    id: 1,
    timestamp: '2025-09-02T10:30:00Z',
    actor: 'testuser',
    changes: {
      notes: ['Old notes', 'New notes'],
      completed: [false, true],
      likelihood: [3, 4]
    },
    action: 'UPDATE',
    remote_addr: '127.0.0.1'
  },
  {
    id: 2,
    timestamp: '2025-09-02T10:25:00Z',
    actor: 'testuser',
    changes: {
      notes: [null, 'Initial notes'],
      completed: [null, false],
      likelihood: [null, 3],
      impact: [null, 4]
    },
    action: 'CREATE',
    remote_addr: '127.0.0.1'
  },
  {
    id: 3,
    timestamp: '2025-09-02T10:20:00Z',
    actor: 'admin',
    changes: {
      title: ['Old Title', 'New Title'],
      description: ['Old description', 'New description']
    },
    action: 'UPDATE',
    remote_addr: '192.168.1.100'
  }
];

const mockChecklistData = [
  {
    id: 1,
    regulation_update: {
      id: 1,
      title: 'HIPAA Security Rule Update 2024',
      description: 'Updated security requirements'
    },
    completed: true,
    likelihood: 4,
    impact: 5,
    notes: 'Updated notes',
    mitigation_steps: '1. Deploy MFA\n2. Train staff',
    last_updated: '2025-09-02T10:30:00Z'
  }
];

describe('Audit Log Functionality Tests', () => {
  beforeEach(() => {
    jest.clearAllMocks();
    localStorage.setItem('token', 'mock-token');
    
    // Mock successful API responses
    mockedAxios.get.mockImplementation((url) => {
      if (url.includes('/api/checklist/')) {
        return Promise.resolve({ data: mockChecklistData });
      }
      if (url.includes('/api/auditlog/')) {
        return Promise.resolve({ data: mockAuditLogData });
      }
      if (url.includes('/api/profile/')) {
        return Promise.resolve({ 
          data: {
            id: 1,
            username: 'testuser',
            email: 'test@example.com',
            first_name: 'Test',
            last_name: 'User'
          }
        });
      }
      return Promise.resolve({ data: [] });
    });
    
    mockedAxios.patch.mockResolvedValue({ data: {} });
  });

  describe('Audit Log Dialog Display', () => {
    test('opens audit log dialog when audit button is clicked', async () => {
      renderWithTheme(<ChecklistDisplay />);
      
      await waitFor(() => {
        expect(screen.getByText('HIPAA Security Rule Update 2024')).toBeInTheDocument();
      });
      
      const auditButtons = screen.getAllByLabelText(/view audit log/i);
      fireEvent.click(auditButtons[0]);
      
      await waitFor(() => {
        expect(screen.getByText(/audit log/i)).toBeInTheDocument();
        expect(screen.getByText(/testuser/i)).toBeInTheDocument();
        expect(screen.getByText(/admin/i)).toBeInTheDocument();
      });
    });

    test('displays audit log entries with correct information', async () => {
      renderWithTheme(<ChecklistDisplay />);
      
      await waitFor(() => {
        expect(screen.getByText('HIPAA Security Rule Update 2024')).toBeInTheDocument();
      });
      
      const auditButtons = screen.getAllByLabelText(/view audit log/i);
      fireEvent.click(auditButtons[0]);
      
      await waitFor(() => {
        // Check for audit log entries
        expect(screen.getByText(/UPDATE/i)).toBeInTheDocument();
        expect(screen.getByText(/CREATE/i)).toBeInTheDocument();
        expect(screen.getByText(/testuser/i)).toBeInTheDocument();
        expect(screen.getByText(/admin/i)).toBeInTheDocument();
      });
    });

    test('displays timestamps in readable format', async () => {
      renderWithTheme(<ChecklistDisplay />);
      
      await waitFor(() => {
        expect(screen.getByText('HIPAA Security Rule Update 2024')).toBeInTheDocument();
      });
      
      const auditButtons = screen.getAllByLabelText(/view audit log/i);
      fireEvent.click(auditButtons[0]);
      
      await waitFor(() => {
        // Check for formatted timestamps
        expect(screen.getByText(/2025-09-02/i)).toBeInTheDocument();
        expect(screen.getByText(/10:30/i)).toBeInTheDocument();
      });
    });

    test('displays IP addresses for audit entries', async () => {
      renderWithTheme(<ChecklistDisplay />);
      
      await waitFor(() => {
        expect(screen.getByText('HIPAA Security Rule Update 2024')).toBeInTheDocument();
      });
      
      const auditButtons = screen.getAllByLabelText(/view audit log/i);
      fireEvent.click(auditButtons[0]);
      
      await waitFor(() => {
        expect(screen.getByText(/127.0.0.1/i)).toBeInTheDocument();
        expect(screen.getByText(/192.168.1.100/i)).toBeInTheDocument();
      });
    });
  });

  describe('Audit Log Filtering', () => {
    test('filters audit logs by action type', async () => {
      renderWithTheme(<ChecklistDisplay />);
      
      await waitFor(() => {
        expect(screen.getByText('HIPAA Security Rule Update 2024')).toBeInTheDocument();
      });
      
      const auditButtons = screen.getAllByLabelText(/view audit log/i);
      fireEvent.click(auditButtons[0]);
      
      await waitFor(() => {
        const filterSelect = screen.getByLabelText(/filter by action/i);
        fireEvent.change(filterSelect, { target: { value: 'UPDATE' } });
        
        // Should only show UPDATE actions
        expect(screen.getByText(/UPDATE/i)).toBeInTheDocument();
        expect(screen.queryByText(/CREATE/i)).not.toBeInTheDocument();
      });
    });

    test('filters audit logs by actor', async () => {
      renderWithTheme(<ChecklistDisplay />);
      
      await waitFor(() => {
        expect(screen.getByText('HIPAA Security Rule Update 2024')).toBeInTheDocument();
      });
      
      const auditButtons = screen.getAllByLabelText(/view audit log/i);
      fireEvent.click(auditButtons[0]);
      
      await waitFor(() => {
        const actorFilter = screen.getByLabelText(/filter by actor/i);
        fireEvent.change(actorFilter, { target: { value: 'testuser' } });
        
        // Should only show entries by testuser
        expect(screen.getByText(/testuser/i)).toBeInTheDocument();
        expect(screen.queryByText(/admin/i)).not.toBeInTheDocument();
      });
    });

    test('searches audit logs by content', async () => {
      renderWithTheme(<ChecklistDisplay />);
      
      await waitFor(() => {
        expect(screen.getByText('HIPAA Security Rule Update 2024')).toBeInTheDocument();
      });
      
      const auditButtons = screen.getAllByLabelText(/view audit log/i);
      fireEvent.click(auditButtons[0]);
      
      await waitFor(() => {
        const searchInput = screen.getByPlaceholderText(/search audit logs/i);
        fireEvent.change(searchInput, { target: { value: 'notes' } });
        
        // Should show entries containing 'notes'
        expect(screen.getByText(/notes/i)).toBeInTheDocument();
      });
    });
  });

  describe('Audit Log Change Display', () => {
    test('displays field changes in audit log entries', async () => {
      renderWithTheme(<ChecklistDisplay />);
      
      await waitFor(() => {
        expect(screen.getByText('HIPAA Security Rule Update 2024')).toBeInTheDocument();
      });
      
      const auditButtons = screen.getAllByLabelText(/view audit log/i);
      fireEvent.click(auditButtons[0]);
      
      await waitFor(() => {
        // Check for field changes
        expect(screen.getByText(/notes/i)).toBeInTheDocument();
        expect(screen.getByText(/completed/i)).toBeInTheDocument();
        expect(screen.getByText(/likelihood/i)).toBeInTheDocument();
      });
    });

    test('shows before and after values for changes', async () => {
      renderWithTheme(<ChecklistDisplay />);
      
      await waitFor(() => {
        expect(screen.getByText('HIPAA Security Rule Update 2024')).toBeInTheDocument();
      });
      
      const auditButtons = screen.getAllByLabelText(/view audit log/i);
      fireEvent.click(auditButtons[0]);
      
      await waitFor(() => {
        // Check for before/after values
        expect(screen.getByText(/Old notes/i)).toBeInTheDocument();
        expect(screen.getByText(/New notes/i)).toBeInTheDocument();
        expect(screen.getByText(/false/i)).toBeInTheDocument();
        expect(screen.getByText(/true/i)).toBeInTheDocument();
      });
    });

    test('handles null values in changes gracefully', async () => {
      renderWithTheme(<ChecklistDisplay />);
      
      await waitFor(() => {
        expect(screen.getByText('HIPAA Security Rule Update 2024')).toBeInTheDocument();
      });
      
      const auditButtons = screen.getAllByLabelText(/view audit log/i);
      fireEvent.click(auditButtons[0]);
      
      await waitFor(() => {
        // Should handle null values (CREATE operations)
        expect(screen.getByText(/null/i)).toBeInTheDocument();
      });
    });
  });

  describe('Audit Log Export', () => {
    test('exports audit logs to CSV', async () => {
      renderWithTheme(<ChecklistDisplay />);
      
      await waitFor(() => {
        expect(screen.getByText('HIPAA Security Rule Update 2024')).toBeInTheDocument();
      });
      
      const auditButtons = screen.getAllByLabelText(/view audit log/i);
      fireEvent.click(auditButtons[0]);
      
      await waitFor(() => {
        const exportButton = screen.getByRole('button', { name: /export audit log/i });
        fireEvent.click(exportButton);
        
        // Should call export API
        expect(mockedAxios.get).toHaveBeenCalledWith(
          expect.stringContaining('/api/auditlog/export/'),
          expect.any(Object)
        );
      });
    });

    test('handles export errors gracefully', async () => {
      mockedAxios.get.mockRejectedValueOnce(new Error('Export failed'));
      
      renderWithTheme(<ChecklistDisplay />);
      
      await waitFor(() => {
        expect(screen.getByText('HIPAA Security Rule Update 2024')).toBeInTheDocument();
      });
      
      const auditButtons = screen.getAllByLabelText(/view audit log/i);
      fireEvent.click(auditButtons[0]);
      
      await waitFor(() => {
        const exportButton = screen.getByRole('button', { name: /export audit log/i });
        fireEvent.click(exportButton);
      });
      
      await waitFor(() => {
        expect(screen.getByText(/export failed/i)).toBeInTheDocument();
      });
    });
  });

  describe('Audit Log Error Handling', () => {
    test('displays error message when audit log API fails', async () => {
      mockedAxios.get.mockImplementation((url) => {
        if (url.includes('/api/auditlog/')) {
          return Promise.reject(new Error('Audit log API error'));
        }
        if (url.includes('/api/checklist/')) {
          return Promise.resolve({ data: mockChecklistData });
        }
        return Promise.resolve({ data: [] });
      });
      
      renderWithTheme(<ChecklistDisplay />);
      
      await waitFor(() => {
        expect(screen.getByText('HIPAA Security Rule Update 2024')).toBeInTheDocument();
      });
      
      const auditButtons = screen.getAllByLabelText(/view audit log/i);
      fireEvent.click(auditButtons[0]);
      
      await waitFor(() => {
        expect(screen.getByText(/error loading audit log/i)).toBeInTheDocument();
      });
    });

    test('displays retry button when audit log error occurs', async () => {
      mockedAxios.get.mockImplementation((url) => {
        if (url.includes('/api/auditlog/')) {
          return Promise.reject(new Error('Audit log API error'));
        }
        if (url.includes('/api/checklist/')) {
          return Promise.resolve({ data: mockChecklistData });
        }
        return Promise.resolve({ data: [] });
      });
      
      renderWithTheme(<ChecklistDisplay />);
      
      await waitFor(() => {
        expect(screen.getByText('HIPAA Security Rule Update 2024')).toBeInTheDocument();
      });
      
      const auditButtons = screen.getAllByLabelText(/view audit log/i);
      fireEvent.click(auditButtons[0]);
      
      await waitFor(() => {
        expect(screen.getByRole('button', { name: /retry/i })).toBeInTheDocument();
      });
    });

    test('retries audit log API call when retry button is clicked', async () => {
      mockedAxios.get
        .mockRejectedValueOnce(new Error('Audit log API error'))
        .mockResolvedValueOnce({ data: mockAuditLogData });
      
      renderWithTheme(<ChecklistDisplay />);
      
      await waitFor(() => {
        expect(screen.getByText('HIPAA Security Rule Update 2024')).toBeInTheDocument();
      });
      
      const auditButtons = screen.getAllByLabelText(/view audit log/i);
      fireEvent.click(auditButtons[0]);
      
      await waitFor(() => {
        const retryButton = screen.getByRole('button', { name: /retry/i });
        fireEvent.click(retryButton);
      });
      
      // Should make another API call
      expect(mockedAxios.get).toHaveBeenCalledTimes(2);
    });
  });

  describe('Audit Log Loading States', () => {
    test('displays loading spinner while fetching audit logs', () => {
      mockedAxios.get.mockImplementation((url) => {
        if (url.includes('/api/auditlog/')) {
          return new Promise(resolve => setTimeout(() => resolve({ data: mockAuditLogData }), 100));
        }
        if (url.includes('/api/checklist/')) {
          return Promise.resolve({ data: mockChecklistData });
        }
        return Promise.resolve({ data: [] });
      });
      
      renderWithTheme(<ChecklistDisplay />);
      
      // Click audit button to trigger loading
      const auditButtons = screen.getAllByLabelText(/view audit log/i);
      fireEvent.click(auditButtons[0]);
      
      expect(screen.getByRole('progressbar')).toBeInTheDocument();
    });

    test('hides loading spinner when audit logs are loaded', async () => {
      renderWithTheme(<ChecklistDisplay />);
      
      await waitFor(() => {
        expect(screen.getByText('HIPAA Security Rule Update 2024')).toBeInTheDocument();
      });
      
      const auditButtons = screen.getAllByLabelText(/view audit log/i);
      fireEvent.click(auditButtons[0]);
      
      await waitFor(() => {
        expect(screen.queryByRole('progressbar')).not.toBeInTheDocument();
      });
    });
  });

  describe('Audit Log Accessibility', () => {
    test('has proper ARIA labels for audit log elements', async () => {
      renderWithTheme(<ChecklistDisplay />);
      
      await waitFor(() => {
        expect(screen.getByText('HIPAA Security Rule Update 2024')).toBeInTheDocument();
      });
      
      const auditButtons = screen.getAllByLabelText(/view audit log/i);
      fireEvent.click(auditButtons[0]);
      
      await waitFor(() => {
        expect(screen.getByLabelText(/filter by action/i)).toBeInTheDocument();
        expect(screen.getByLabelText(/filter by actor/i)).toBeInTheDocument();
        expect(screen.getByPlaceholderText(/search audit logs/i)).toBeInTheDocument();
      });
    });

    test('supports keyboard navigation in audit log dialog', async () => {
      renderWithTheme(<ChecklistDisplay />);
      
      await waitFor(() => {
        expect(screen.getByText('HIPAA Security Rule Update 2024')).toBeInTheDocument();
      });
      
      const auditButtons = screen.getAllByLabelText(/view audit log/i);
      fireEvent.click(auditButtons[0]);
      
      await waitFor(() => {
        const firstButton = screen.getAllByRole('button')[0];
        firstButton.focus();
        expect(firstButton).toHaveFocus();
        
        // Tab navigation should work
        fireEvent.keyDown(firstButton, { key: 'Tab' });
      });
    });

    test('announces audit log changes to screen readers', async () => {
      renderWithTheme(<ChecklistDisplay />);
      
      await waitFor(() => {
        expect(screen.getByText('HIPAA Security Rule Update 2024')).toBeInTheDocument();
      });
      
      const auditButtons = screen.getAllByLabelText(/view audit log/i);
      fireEvent.click(auditButtons[0]);
      
      await waitFor(() => {
        // Should have proper ARIA attributes for dynamic content
        expect(screen.getByRole('table')).toHaveAttribute('aria-label');
      });
    });
  });

  describe('Audit Log Security', () => {
    test('masks sensitive data in audit log display', async () => {
      const sensitiveAuditData = [
        {
          id: 1,
          timestamp: '2025-09-02T10:30:00Z',
          actor: 'testuser',
          changes: {
            notes: ['Patient ID: 12345', 'Patient ID: 12345 - Updated'],
            ssn: ['123-45-6789', '123-45-6789 - Updated']
          },
          action: 'UPDATE',
          remote_addr: '127.0.0.1'
        }
      ];
      
      mockedAxios.get.mockImplementation((url) => {
        if (url.includes('/api/auditlog/')) {
          return Promise.resolve({ data: sensitiveAuditData });
        }
        if (url.includes('/api/checklist/')) {
          return Promise.resolve({ data: mockChecklistData });
        }
        return Promise.resolve({ data: [] });
      });
      
      renderWithTheme(<ChecklistDisplay />);
      
      await waitFor(() => {
        expect(screen.getByText('HIPAA Security Rule Update 2024')).toBeInTheDocument();
      });
      
      const auditButtons = screen.getAllByLabelText(/view audit log/i);
      fireEvent.click(auditButtons[0]);
      
      await waitFor(() => {
        // Should mask sensitive data
        expect(screen.getByText(/\*\*\*\*\*/)).toBeInTheDocument();
        expect(screen.queryByText(/123-45-6789/)).not.toBeInTheDocument();
      });
    });

    test('validates user permissions for audit log access', async () => {
      mockedAxios.get.mockImplementation((url) => {
        if (url.includes('/api/auditlog/')) {
          return Promise.reject({
            response: { status: 403, data: { detail: 'Forbidden' } }
          });
        }
        if (url.includes('/api/checklist/')) {
          return Promise.resolve({ data: mockChecklistData });
        }
        return Promise.resolve({ data: [] });
      });
      
      renderWithTheme(<ChecklistDisplay />);
      
      await waitFor(() => {
        expect(screen.getByText('HIPAA Security Rule Update 2024')).toBeInTheDocument();
      });
      
      const auditButtons = screen.getAllByLabelText(/view audit log/i);
      fireEvent.click(auditButtons[0]);
      
      await waitFor(() => {
        expect(screen.getByText(/access denied/i)).toBeInTheDocument();
      });
    });
  });

  describe('Audit Log Performance', () => {
    test('handles large audit log datasets efficiently', async () => {
      const largeAuditData = Array.from({ length: 100 }, (_, i) => ({
        id: i + 1,
        timestamp: `2025-09-02T${10 + Math.floor(i / 10)}:${(i % 10) * 6}:00Z`,
        actor: i % 2 === 0 ? 'testuser' : 'admin',
        changes: {
          notes: [`Old notes ${i}`, `New notes ${i}`],
          completed: [false, true]
        },
        action: i % 3 === 0 ? 'CREATE' : 'UPDATE',
        remote_addr: '127.0.0.1'
      }));
      
      mockedAxios.get.mockImplementation((url) => {
        if (url.includes('/api/auditlog/')) {
          return Promise.resolve({ data: largeAuditData });
        }
        if (url.includes('/api/checklist/')) {
          return Promise.resolve({ data: mockChecklistData });
        }
        return Promise.resolve({ data: [] });
      });
      
      const startTime = performance.now();
      
      renderWithTheme(<ChecklistDisplay />);
      
      await waitFor(() => {
        expect(screen.getByText('HIPAA Security Rule Update 2024')).toBeInTheDocument();
      });
      
      const auditButtons = screen.getAllByLabelText(/view audit log/i);
      fireEvent.click(auditButtons[0]);
      
      await waitFor(() => {
        expect(screen.getByText(/audit log/i)).toBeInTheDocument();
      });
      
      const endTime = performance.now();
      const renderTime = endTime - startTime;
      
      // Should render within reasonable time (less than 1 second)
      expect(renderTime).toBeLessThan(1000);
    });

    test('implements pagination for large audit log datasets', async () => {
      const largeAuditData = Array.from({ length: 50 }, (_, i) => ({
        id: i + 1,
        timestamp: `2025-09-02T10:${i}:00Z`,
        actor: 'testuser',
        changes: { notes: [`Notes ${i}`, `Updated notes ${i}`] },
        action: 'UPDATE',
        remote_addr: '127.0.0.1'
      }));
      
      mockedAxios.get.mockImplementation((url) => {
        if (url.includes('/api/auditlog/')) {
          return Promise.resolve({ data: largeAuditData });
        }
        if (url.includes('/api/checklist/')) {
          return Promise.resolve({ data: mockChecklistData });
        }
        return Promise.resolve({ data: [] });
      });
      
      renderWithTheme(<ChecklistDisplay />);
      
      await waitFor(() => {
        expect(screen.getByText('HIPAA Security Rule Update 2024')).toBeInTheDocument();
      });
      
      const auditButtons = screen.getAllByLabelText(/view audit log/i);
      fireEvent.click(auditButtons[0]);
      
      await waitFor(() => {
        // Should show pagination controls
        expect(screen.getByText(/page/i)).toBeInTheDocument();
        expect(screen.getByRole('button', { name: /next/i })).toBeInTheDocument();
      });
    });
  });
});
