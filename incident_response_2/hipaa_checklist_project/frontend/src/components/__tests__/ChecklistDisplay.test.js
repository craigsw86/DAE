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

// Mock data
const mockChecklistData = [
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
    last_updated: '2025-09-02T10:00:00Z'
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
    last_updated: '2025-09-01T15:30:00Z'
  }
];

const mockUserProfile = {
  id: 1,
  username: 'testuser',
  email: 'test@example.com',
  first_name: 'Test',
  last_name: 'User'
};

describe('ChecklistDisplay Component', () => {
  beforeEach(() => {
    jest.clearAllMocks();
    localStorage.setItem('token', 'mock-token');
    
    // Mock successful API responses
    mockedAxios.get.mockImplementation((url) => {
      if (url.includes('/api/checklist/')) {
        return Promise.resolve({ data: mockChecklistData });
      }
      if (url.includes('/api/profile/')) {
        return Promise.resolve({ data: mockUserProfile });
      }
      if (url.includes('/api/auditlog/')) {
        return Promise.resolve({ data: [] });
      }
      return Promise.resolve({ data: [] });
    });
    
    mockedAxios.patch.mockResolvedValue({ data: {} });
  });

  describe('Rendering', () => {
    test('renders checklist dashboard with KPI cards', async () => {
      renderWithTheme(<ChecklistDisplay />);
      
      await waitFor(() => {
        expect(screen.getByText(/total items/i)).toBeInTheDocument();
        expect(screen.getByText(/completed items/i)).toBeInTheDocument();
        expect(screen.getByText(/high risk items/i)).toBeInTheDocument();
        expect(screen.getByText(/completion rate/i)).toBeInTheDocument();
      });
    });

    test('renders checklist items table', async () => {
      renderWithTheme(<ChecklistDisplay />);
      
      await waitFor(() => {
        expect(screen.getByText('HIPAA Security Rule Update 2024')).toBeInTheDocument();
        expect(screen.getByText('HIPAA Privacy Rule Amendment 2024')).toBeInTheDocument();
      });
    });

    test('displays risk levels correctly', async () => {
      renderWithTheme(<ChecklistDisplay />);
      
      await waitFor(() => {
        // High risk item (likelihood: 4, impact: 5)
        expect(screen.getByText(/high risk/i)).toBeInTheDocument();
        // Medium risk item (likelihood: 3, impact: 4)
        expect(screen.getByText(/medium risk/i)).toBeInTheDocument();
      });
    });

    test('shows completion status correctly', async () => {
      renderWithTheme(<ChecklistDisplay />);
      
      await waitFor(() => {
        // Check for completed and incomplete items
        const checkboxes = screen.getAllByRole('checkbox');
        expect(checkboxes[0]).not.toBeChecked(); // First item not completed
        expect(checkboxes[1]).toBeChecked(); // Second item completed
      });
    });
  });

  describe('KPI Calculations', () => {
    test('calculates total items correctly', async () => {
      renderWithTheme(<ChecklistDisplay />);
      
      await waitFor(() => {
        expect(screen.getByText('2')).toBeInTheDocument(); // Total items
      });
    });

    test('calculates completed items correctly', async () => {
      renderWithTheme(<ChecklistDisplay />);
      
      await waitFor(() => {
        expect(screen.getByText('1')).toBeInTheDocument(); // Completed items
      });
    });

    test('calculates completion rate correctly', async () => {
      renderWithTheme(<ChecklistDisplay />);
      
      await waitFor(() => {
        expect(screen.getByText('50%')).toBeInTheDocument(); // 1/2 = 50%
      });
    });

    test('calculates high risk items correctly', async () => {
      renderWithTheme(<ChecklistDisplay />);
      
      await waitFor(() => {
        expect(screen.getByText('1')).toBeInTheDocument(); // High risk items
      });
    });
  });

  describe('User Interactions', () => {
    test('toggles completion status when checkbox is clicked', async () => {
      renderWithTheme(<ChecklistDisplay />);
      
      await waitFor(() => {
        const checkboxes = screen.getAllByRole('checkbox');
        const firstCheckbox = checkboxes[0];
        
        // Initially not checked
        expect(firstCheckbox).not.toBeChecked();
        
        // Click to toggle
        fireEvent.click(firstCheckbox);
        
        // Should call API to update
        expect(mockedAxios.patch).toHaveBeenCalledWith(
          expect.stringContaining('/api/checklist/1/'),
          { completed: true },
          expect.any(Object)
        );
      });
    });

    test('opens notes dialog when edit button is clicked', async () => {
      renderWithTheme(<ChecklistDisplay />);
      
      await waitFor(() => {
        const editButtons = screen.getAllByLabelText(/edit notes/i);
        fireEvent.click(editButtons[0]);
        
        expect(screen.getByText(/edit notes/i)).toBeInTheDocument();
        expect(screen.getByDisplayValue('Critical security requirement')).toBeInTheDocument();
      });
    });

    test('saves notes when save button is clicked in dialog', async () => {
      renderWithTheme(<ChecklistDisplay />);
      
      await waitFor(() => {
        const editButtons = screen.getAllByLabelText(/edit notes/i);
        fireEvent.click(editButtons[0]);
        
        const notesInput = screen.getByDisplayValue('Critical security requirement');
        const saveButton = screen.getByRole('button', { name: /save/i });
        
        // Update notes
        fireEvent.change(notesInput, { target: { value: 'Updated notes' } });
        fireEvent.click(saveButton);
        
        // Should call API to update
        expect(mockedAxios.patch).toHaveBeenCalledWith(
          expect.stringContaining('/api/checklist/1/'),
          { notes: 'Updated notes' },
          expect.any(Object)
        );
      });
    });

    test('opens mitigation steps dialog when mitigation button is clicked', async () => {
      renderWithTheme(<ChecklistDisplay />);
      
      await waitFor(() => {
        const mitigationButtons = screen.getAllByLabelText(/view mitigation steps/i);
        fireEvent.click(mitigationButtons[0]);
        
        expect(screen.getByText(/mitigation steps/i)).toBeInTheDocument();
        expect(screen.getByText('1. Deploy MFA')).toBeInTheDocument();
        expect(screen.getByText('2. Train staff')).toBeInTheDocument();
        expect(screen.getByText('3. Monitor compliance')).toBeInTheDocument();
      });
    });

    test('opens audit log dialog when audit button is clicked', async () => {
      renderWithTheme(<ChecklistDisplay />);
      
      await waitFor(() => {
        const auditButtons = screen.getAllByLabelText(/view audit log/i);
        fireEvent.click(auditButtons[0]);
        
        expect(screen.getByText(/audit log/i)).toBeInTheDocument();
      });
    });
  });

  describe('Filtering and Search', () => {
    test('filters items by completion status', async () => {
      renderWithTheme(<ChecklistDisplay />);
      
      await waitFor(() => {
        const filterSelect = screen.getByLabelText(/filter by status/i);
        fireEvent.change(filterSelect, { target: { value: 'completed' } });
        
        // Should only show completed items
        expect(screen.getByText('HIPAA Privacy Rule Amendment 2024')).toBeInTheDocument();
        expect(screen.queryByText('HIPAA Security Rule Update 2024')).not.toBeInTheDocument();
      });
    });

    test('filters items by risk level', async () => {
      renderWithTheme(<ChecklistDisplay />);
      
      await waitFor(() => {
        const riskFilterSelect = screen.getByLabelText(/filter by risk/i);
        fireEvent.change(riskFilterSelect, { target: { value: 'high' } });
        
        // Should only show high risk items
        expect(screen.getByText('HIPAA Security Rule Update 2024')).toBeInTheDocument();
        expect(screen.queryByText('HIPAA Privacy Rule Amendment 2024')).not.toBeInTheDocument();
      });
    });

    test('searches items by title', async () => {
      renderWithTheme(<ChecklistDisplay />);
      
      await waitFor(() => {
        const searchInput = screen.getByPlaceholderText(/search items/i);
        fireEvent.change(searchInput, { target: { value: 'Security' } });
        
        // Should only show items containing "Security"
        expect(screen.getByText('HIPAA Security Rule Update 2024')).toBeInTheDocument();
        expect(screen.queryByText('HIPAA Privacy Rule Amendment 2024')).not.toBeInTheDocument();
      });
    });
  });

  describe('Export Functionality', () => {
    test('exports data to CSV', async () => {
      renderWithTheme(<ChecklistDisplay />);
      
      await waitFor(() => {
        const exportButton = screen.getByRole('button', { name: /export csv/i });
        fireEvent.click(exportButton);
        
        // Should call export API
        expect(mockedAxios.get).toHaveBeenCalledWith(
          expect.stringContaining('/api/checklist/export/'),
          expect.any(Object)
        );
      });
    });

    test('exports data to PDF', async () => {
      renderWithTheme(<ChecklistDisplay />);
      
      await waitFor(() => {
        const exportButton = screen.getByRole('button', { name: /export pdf/i });
        fireEvent.click(exportButton);
        
        // Should call export API
        expect(mockedAxios.get).toHaveBeenCalledWith(
          expect.stringContaining('/api/checklist/export/'),
          expect.any(Object)
        );
      });
    });
  });

  describe('Error Handling', () => {
    test('displays error message when API call fails', async () => {
      mockedAxios.get.mockRejectedValueOnce(new Error('Network Error'));
      
      renderWithTheme(<ChecklistDisplay />);
      
      await waitFor(() => {
        expect(screen.getByText(/error loading checklist/i)).toBeInTheDocument();
      });
    });

    test('displays retry button when error occurs', async () => {
      mockedAxios.get.mockRejectedValueOnce(new Error('Network Error'));
      
      renderWithTheme(<ChecklistDisplay />);
      
      await waitFor(() => {
        expect(screen.getByRole('button', { name: /retry/i })).toBeInTheDocument();
      });
    });

    test('retries API call when retry button is clicked', async () => {
      mockedAxios.get
        .mockRejectedValueOnce(new Error('Network Error'))
        .mockResolvedValueOnce({ data: mockChecklistData });
      
      renderWithTheme(<ChecklistDisplay />);
      
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
      // Mock a delayed response
      mockedAxios.get.mockImplementation(() => 
        new Promise(resolve => setTimeout(() => resolve({ data: mockChecklistData }), 100))
      );
      
      renderWithTheme(<ChecklistDisplay />);
      
      expect(screen.getByRole('progressbar')).toBeInTheDocument();
    });

    test('hides loading spinner when data is loaded', async () => {
      renderWithTheme(<ChecklistDisplay />);
      
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

      renderWithTheme(<ChecklistDisplay />);
      
      // Should render without errors on mobile
      expect(screen.getByText(/total items/i)).toBeInTheDocument();
    });

    test('adapts to tablet viewport', () => {
      Object.defineProperty(window, 'innerWidth', {
        writable: true,
        configurable: true,
        value: 768,
      });

      renderWithTheme(<ChecklistDisplay />);
      
      // Should render without errors on tablet
      expect(screen.getByText(/total items/i)).toBeInTheDocument();
    });

    test('adapts to desktop viewport', () => {
      Object.defineProperty(window, 'innerWidth', {
        writable: true,
        configurable: true,
        value: 1200,
      });

      renderWithTheme(<ChecklistDisplay />);
      
      // Should render without errors on desktop
      expect(screen.getByText(/total items/i)).toBeInTheDocument();
    });
  });

  describe('Accessibility', () => {
    test('has proper ARIA labels for interactive elements', async () => {
      renderWithTheme(<ChecklistDisplay />);
      
      await waitFor(() => {
        expect(screen.getByLabelText(/filter by status/i)).toBeInTheDocument();
        expect(screen.getByLabelText(/filter by risk/i)).toBeInTheDocument();
        expect(screen.getByPlaceholderText(/search items/i)).toBeInTheDocument();
      });
    });

    test('supports keyboard navigation', async () => {
      renderWithTheme(<ChecklistDisplay />);
      
      await waitFor(() => {
        const firstCheckbox = screen.getAllByRole('checkbox')[0];
        firstCheckbox.focus();
        expect(firstCheckbox).toHaveFocus();
        
        // Tab to next interactive element
        fireEvent.keyDown(firstCheckbox, { key: 'Tab' });
      });
    });

    test('announces status changes to screen readers', async () => {
      renderWithTheme(<ChecklistDisplay />);
      
      await waitFor(() => {
        const checkboxes = screen.getAllByRole('checkbox');
        fireEvent.click(checkboxes[0]);
        
        // Should have proper ARIA attributes for status changes
        expect(checkboxes[0]).toHaveAttribute('aria-checked');
      });
    });
  });
});
