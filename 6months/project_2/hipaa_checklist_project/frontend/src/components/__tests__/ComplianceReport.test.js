import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { ThemeProvider, createTheme } from '@mui/material/styles';
import axios from 'axios';
import ComplianceReport from '../ComplianceReport';

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

// Mock data
const mockComplianceData = [
  {
    id: 1,
    regulation_update: {
      id: 1,
      title: 'HIPAA Security Rule Update 2024',
      description: 'Updated security requirements'
    },
    completed: false,
    likelihood: 4,
    impact: 5,
    notes: 'Critical security requirement',
    mitigation_steps: '1. Deploy MFA\n2. Train staff\n3. Monitor compliance',
    last_updated: '2025-09-02T10:00:00Z',
    user: {
      username: 'testuser',
      email: 'test@example.com'
    }
  },
  {
    id: 2,
    regulation_update: {
      id: 2,
      title: 'HIPAA Privacy Rule Amendment 2024',
      description: 'Updated privacy requirements'
    },
    completed: true,
    likelihood: 3,
    impact: 4,
    notes: 'Completed last month',
    mitigation_steps: '1. Legal review\n2. Staff training',
    last_updated: '2025-09-01T15:30:00Z',
    user: {
      username: 'testuser',
      email: 'test@example.com'
    }
  }
];

const mockTrendsData = [
  {
    date: '2025-09-01',
    total_items: 2,
    completed_items: 1,
    high_risk_items: 1,
    completion_rate: 50
  },
  {
    date: '2025-09-02',
    total_items: 2,
    completed_items: 1,
    high_risk_items: 1,
    completion_rate: 50
  }
];

describe('ComplianceReport Component', () => {
  beforeEach(() => {
    jest.clearAllMocks();
    localStorage.setItem('token', 'mock-token');
    
    // Mock successful API responses
    mockedAxios.get.mockImplementation((url) => {
      if (url.includes('/api/report/')) {
        return Promise.resolve({ data: mockComplianceData });
      }
      if (url.includes('/api/report/trends/')) {
        return Promise.resolve({ data: mockTrendsData });
      }
      return Promise.resolve({ data: [] });
    });
  });

  describe('Rendering', () => {
    test('renders compliance report with all sections', async () => {
      renderWithTheme(<ComplianceReport />);
      
      await waitFor(() => {
        expect(screen.getByText(/compliance report/i)).toBeInTheDocument();
        expect(screen.getByText(/risk matrix/i)).toBeInTheDocument();
        expect(screen.getByText(/compliance summary/i)).toBeInTheDocument();
        expect(screen.getByText(/trends analysis/i)).toBeInTheDocument();
      });
    });

    test('renders risk matrix with correct dimensions', async () => {
      renderWithTheme(<ComplianceReport />);
      
      await waitFor(() => {
        // Check for risk matrix grid (5x5)
        expect(screen.getByText(/likelihood/i)).toBeInTheDocument();
        expect(screen.getByText(/impact/i)).toBeInTheDocument();
        
        // Check for risk levels
        expect(screen.getByText(/low/i)).toBeInTheDocument();
        expect(screen.getByText(/medium/i)).toBeInTheDocument();
        expect(screen.getByText(/high/i)).toBeInTheDocument();
        expect(screen.getByText(/critical/i)).toBeInTheDocument();
      });
    });

    test('displays compliance data in table format', async () => {
      renderWithTheme(<ComplianceReport />);
      
      await waitFor(() => {
        expect(screen.getByText('HIPAA Security Rule Update 2024')).toBeInTheDocument();
        expect(screen.getByText('HIPAA Privacy Rule Amendment 2024')).toBeInTheDocument();
      });
    });

    test('shows risk levels with correct colors', async () => {
      renderWithTheme(<ComplianceReport />);
      
      await waitFor(() => {
        // High risk item (likelihood: 4, impact: 5)
        expect(screen.getByText(/high risk/i)).toBeInTheDocument();
        // Medium risk item (likelihood: 3, impact: 4)
        expect(screen.getByText(/medium risk/i)).toBeInTheDocument();
      });
    });
  });

  describe('Risk Matrix Functionality', () => {
    test('calculates risk scores correctly', async () => {
      renderWithTheme(<ComplianceReport />);
      
      await waitFor(() => {
        // High risk: likelihood 4 * impact 5 = 20
        expect(screen.getByText('20')).toBeInTheDocument();
        // Medium risk: likelihood 3 * impact 4 = 12
        expect(screen.getByText('12')).toBeInTheDocument();
      });
    });

    test('categorizes risks correctly', async () => {
      renderWithTheme(<ComplianceReport />);
      
      await waitFor(() => {
        // Score 20 should be Critical risk
        expect(screen.getByText(/critical/i)).toBeInTheDocument();
        // Score 12 should be High risk
        expect(screen.getByText(/high/i)).toBeInTheDocument();
      });
    });

    test('displays risk distribution in matrix', async () => {
      renderWithTheme(<ComplianceReport />);
      
      await waitFor(() => {
        // Should show count of items in each risk category
        expect(screen.getByText(/1/)).toBeInTheDocument(); // 1 critical risk
        expect(screen.getByText(/1/)).toBeInTheDocument(); // 1 high risk
      });
    });
  });

  describe('Filtering and Sorting', () => {
    test('filters items by completion status', async () => {
      renderWithTheme(<ComplianceReport />);
      
      await waitFor(() => {
        const filterSelect = screen.getByLabelText(/filter by status/i);
        fireEvent.change(filterSelect, { target: { value: 'completed' } });
        
        // Should only show completed items
        expect(screen.getByText('HIPAA Privacy Rule Amendment 2024')).toBeInTheDocument();
        expect(screen.queryByText('HIPAA Security Rule Update 2024')).not.toBeInTheDocument();
      });
    });

    test('filters items by risk level', async () => {
      renderWithTheme(<ComplianceReport />);
      
      await waitFor(() => {
        const riskFilterSelect = screen.getByLabelText(/filter by risk/i);
        fireEvent.change(riskFilterSelect, { target: { value: 'critical' } });
        
        // Should only show critical risk items
        expect(screen.getByText('HIPAA Security Rule Update 2024')).toBeInTheDocument();
        expect(screen.queryByText('HIPAA Privacy Rule Amendment 2024')).not.toBeInTheDocument();
      });
    });

    test('sorts items by risk score', async () => {
      renderWithTheme(<ComplianceReport />);
      
      await waitFor(() => {
        const sortSelect = screen.getByLabelText(/sort by/i);
        fireEvent.change(sortSelect, { target: { value: 'risk_score_desc' } });
        
        // Should sort by risk score descending (highest first)
        const riskScores = screen.getAllByText(/\d+/);
        expect(riskScores[0]).toHaveTextContent('20'); // Highest score first
      });
    });

    test('sorts items by completion status', async () => {
      renderWithTheme(<ComplianceReport />);
      
      await waitFor(() => {
        const sortSelect = screen.getByLabelText(/sort by/i);
        fireEvent.change(sortSelect, { target: { value: 'completion_status' } });
        
        // Should sort by completion status
        const checkboxes = screen.getAllByRole('checkbox');
        // Completed items should come first
        expect(checkboxes[0]).toBeChecked();
        expect(checkboxes[1]).not.toBeChecked();
      });
    });

    test('searches items by title', async () => {
      renderWithTheme(<ComplianceReport />);
      
      await waitFor(() => {
        const searchInput = screen.getByPlaceholderText(/search compliance items/i);
        fireEvent.change(searchInput, { target: { value: 'Security' } });
        
        // Should only show items containing "Security"
        expect(screen.getByText('HIPAA Security Rule Update 2024')).toBeInTheDocument();
        expect(screen.queryByText('HIPAA Privacy Rule Amendment 2024')).not.toBeInTheDocument();
      });
    });
  });

  describe('Export Functionality', () => {
    test('exports report to CSV', async () => {
      renderWithTheme(<ComplianceReport />);
      
      await waitFor(() => {
        const exportButton = screen.getByRole('button', { name: /export csv/i });
        fireEvent.click(exportButton);
        
        // Should call export API
        expect(mockedAxios.get).toHaveBeenCalledWith(
          expect.stringContaining('/api/report/export/'),
          expect.any(Object)
        );
      });
    });

    test('exports report to PDF', async () => {
      renderWithTheme(<ComplianceReport />);
      
      await waitFor(() => {
        const exportButton = screen.getByRole('button', { name: /export pdf/i });
        fireEvent.click(exportButton);
        
        // Should call export API
        expect(mockedAxios.get).toHaveBeenCalledWith(
          expect.stringContaining('/api/report/export/'),
          expect.any(Object)
        );
      });
    });

    test('handles export errors gracefully', async () => {
      mockedAxios.get.mockRejectedValueOnce(new Error('Export failed'));
      
      renderWithTheme(<ComplianceReport />);
      
      await waitFor(() => {
        const exportButton = screen.getByRole('button', { name: /export csv/i });
        fireEvent.click(exportButton);
      });
      
      await waitFor(() => {
        expect(screen.getByText(/export failed/i)).toBeInTheDocument();
      });
    });
  });

  describe('Trends Analysis', () => {
    test('displays trends chart', async () => {
      renderWithTheme(<ComplianceReport />);
      
      await waitFor(() => {
        expect(screen.getByText(/trends analysis/i)).toBeInTheDocument();
        expect(screen.getByTestId('mock-chart')).toBeInTheDocument();
      });
    });

    test('shows trend data correctly', async () => {
      renderWithTheme(<ComplianceReport />);
      
      await waitFor(() => {
        // Should display trend metrics
        expect(screen.getByText(/completion rate/i)).toBeInTheDocument();
        expect(screen.getByText(/50%/)).toBeInTheDocument(); // 50% completion rate
      });
    });

    test('handles empty trends data', async () => {
      mockedAxios.get.mockImplementation((url) => {
        if (url.includes('/api/report/trends/')) {
          return Promise.resolve({ data: [] });
        }
        return Promise.resolve({ data: mockComplianceData });
      });
      
      renderWithTheme(<ComplianceReport />);
      
      await waitFor(() => {
        expect(screen.getByText(/no trend data available/i)).toBeInTheDocument();
      });
    });
  });

  describe('Summary Statistics', () => {
    test('calculates total compliance items', async () => {
      renderWithTheme(<ComplianceReport />);
      
      await waitFor(() => {
        expect(screen.getByText('2')).toBeInTheDocument(); // Total items
      });
    });

    test('calculates completion percentage', async () => {
      renderWithTheme(<ComplianceReport />);
      
      await waitFor(() => {
        expect(screen.getByText('50%')).toBeInTheDocument(); // 1/2 = 50%
      });
    });

    test('calculates risk distribution', async () => {
      renderWithTheme(<ComplianceReport />);
      
      await waitFor(() => {
        // Should show breakdown by risk level
        expect(screen.getByText(/critical/i)).toBeInTheDocument();
        expect(screen.getByText(/high/i)).toBeInTheDocument();
        expect(screen.getByText(/medium/i)).toBeInTheDocument();
        expect(screen.getByText(/low/i)).toBeInTheDocument();
      });
    });

    test('shows average risk score', async () => {
      renderWithTheme(<ComplianceReport />);
      
      await waitFor(() => {
        // Average of 20 and 12 = 16
        expect(screen.getByText('16')).toBeInTheDocument();
      });
    });
  });

  describe('Error Handling', () => {
    test('displays error message when API call fails', async () => {
      mockedAxios.get.mockRejectedValueOnce(new Error('Network Error'));
      
      renderWithTheme(<ComplianceReport />);
      
      await waitFor(() => {
        expect(screen.getByText(/error loading compliance report/i)).toBeInTheDocument();
      });
    });

    test('displays retry button when error occurs', async () => {
      mockedAxios.get.mockRejectedValueOnce(new Error('Network Error'));
      
      renderWithTheme(<ComplianceReport />);
      
      await waitFor(() => {
        expect(screen.getByRole('button', { name: /retry/i })).toBeInTheDocument();
      });
    });

    test('retries API call when retry button is clicked', async () => {
      mockedAxios.get
        .mockRejectedValueOnce(new Error('Network Error'))
        .mockResolvedValueOnce({ data: mockComplianceData });
      
      renderWithTheme(<ComplianceReport />);
      
      await waitFor(() => {
        const retryButton = screen.getByRole('button', { name: /retry/i });
        fireEvent.click(retryButton);
      });
      
      // Should make another API call
      expect(mockedAxios.get).toHaveBeenCalledTimes(2);
    });
  });

  describe('Loading States', () => {
    test('displays loading spinner while fetching data', () => {
      mockedAxios.get.mockImplementation(() => 
        new Promise(resolve => setTimeout(() => resolve({ data: mockComplianceData }), 100))
      );
      
      renderWithTheme(<ComplianceReport />);
      
      expect(screen.getByRole('progressbar')).toBeInTheDocument();
    });

    test('hides loading spinner when data is loaded', async () => {
      renderWithTheme(<ComplianceReport />);
      
      await waitFor(() => {
        expect(screen.queryByRole('progressbar')).not.toBeInTheDocument();
      });
    });
  });

  describe('Responsive Design', () => {
    test('adapts to mobile viewport', () => {
      Object.defineProperty(window, 'innerWidth', {
        writable: true,
        configurable: true,
        value: 375,
      });

      renderWithTheme(<ComplianceReport />);
      
      // Should render without errors on mobile
      expect(screen.getByText(/compliance report/i)).toBeInTheDocument();
    });

    test('adapts to tablet viewport', () => {
      Object.defineProperty(window, 'innerWidth', {
        writable: true,
        configurable: true,
        value: 768,
      });

      renderWithTheme(<ComplianceReport />);
      
      // Should render without errors on tablet
      expect(screen.getByText(/compliance report/i)).toBeInTheDocument();
    });

    test('adapts to desktop viewport', () => {
      Object.defineProperty(window, 'innerWidth', {
        writable: true,
        configurable: true,
        value: 1200,
      });

      renderWithTheme(<ComplianceReport />);
      
      // Should render without errors on desktop
      expect(screen.getByText(/compliance report/i)).toBeInTheDocument();
    });
  });

  describe('Accessibility', () => {
    test('has proper ARIA labels for interactive elements', async () => {
      renderWithTheme(<ComplianceReport />);
      
      await waitFor(() => {
        expect(screen.getByLabelText(/filter by status/i)).toBeInTheDocument();
        expect(screen.getByLabelText(/filter by risk/i)).toBeInTheDocument();
        expect(screen.getByLabelText(/sort by/i)).toBeInTheDocument();
        expect(screen.getByPlaceholderText(/search compliance items/i)).toBeInTheDocument();
      });
    });

    test('supports keyboard navigation', async () => {
      renderWithTheme(<ComplianceReport />);
      
      await waitFor(() => {
        const firstButton = screen.getAllByRole('button')[0];
        firstButton.focus();
        expect(firstButton).toHaveFocus();
        
        // Tab to next interactive element
        fireEvent.keyDown(firstButton, { key: 'Tab' });
      });
    });

    test('announces data changes to screen readers', async () => {
      renderWithTheme(<ComplianceReport />);
      
      await waitFor(() => {
        // Should have proper ARIA attributes for dynamic content
        expect(screen.getByRole('table')).toHaveAttribute('aria-label');
      });
    });
  });

  describe('Print Functionality', () => {
    test('has print button for report', async () => {
      renderWithTheme(<ComplianceReport />);
      
      await waitFor(() => {
        expect(screen.getByRole('button', { name: /print report/i })).toBeInTheDocument();
      });
    });

    test('opens print dialog when print button is clicked', async () => {
      // Mock window.print
      window.print = jest.fn();
      
      renderWithTheme(<ComplianceReport />);
      
      await waitFor(() => {
        const printButton = screen.getByRole('button', { name: /print report/i });
        fireEvent.click(printButton);
        
        expect(window.print).toHaveBeenCalled();
      });
    });
  });
});
