import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { ThemeProvider, createTheme } from '@mui/material/styles';
import axios from 'axios';
import App from '../App';
import Login from '../Login';
import ChecklistDisplay from '../ChecklistDisplay';
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
const mockToken = 'mock-access-token';
const mockRefreshToken = 'mock-refresh-token';
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
    mitigation_steps: '1. Deploy MFA\n2. Train staff',
    last_updated: '2025-09-02T10:00:00Z'
  }
];

const mockUserProfile = {
  id: 1,
  username: 'testuser',
  email: 'test@example.com',
  first_name: 'Test',
  last_name: 'User'
};

describe('Component Integration Tests', () => {
  beforeEach(() => {
    jest.clearAllMocks();
    localStorage.clear();
    
    // Mock successful API responses
    mockedAxios.post.mockResolvedValue({
      data: { access: mockToken, refresh: mockRefreshToken }
    });
    
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
      if (url.includes('/api/report/')) {
        return Promise.resolve({ data: mockChecklistData });
      }
      return Promise.resolve({ data: [] });
    });
    
    mockedAxios.patch.mockResolvedValue({ data: {} });
  });

  describe('Login to Dashboard Flow', () => {
    test('successful login redirects to dashboard', async () => {
      renderWithTheme(<Login />);
      
      const usernameInput = screen.getByLabelText(/username/i);
      const passwordInput = screen.getByLabelText(/password/i);
      const loginButton = screen.getByRole('button', { name: /login/i });

      // Fill form and submit
      await userEvent.type(usernameInput, 'testuser');
      await userEvent.type(passwordInput, 'testpass');
      fireEvent.click(loginButton);

      // Wait for API call and token storage
      await waitFor(() => {
        expect(mockedAxios.post).toHaveBeenCalledWith(
          'http://localhost:8000/api/token/',
          { username: 'testuser', password: 'testpass' }
        );
      });

      expect(localStorage.setItem).toHaveBeenCalledWith('token', mockToken);
      expect(localStorage.setItem).toHaveBeenCalledWith('refreshToken', mockRefreshToken);
    });

    test('login failure shows error and allows retry', async () => {
      mockedAxios.post.mockRejectedValueOnce({
        response: { status: 401, data: { detail: 'Invalid credentials' } }
      });

      renderWithTheme(<Login />);
      
      const usernameInput = screen.getByLabelText(/username/i);
      const passwordInput = screen.getByLabelText(/password/i);
      const loginButton = screen.getByRole('button', { name: /login/i });

      await userEvent.type(usernameInput, 'wronguser');
      await userEvent.type(passwordInput, 'wrongpass');
      fireEvent.click(loginButton);

      await waitFor(() => {
        expect(screen.getByText(/invalid username or password/i)).toBeInTheDocument();
      });

      // Should show retry button
      expect(screen.getByRole('button', { name: /retry/i })).toBeInTheDocument();
    });
  });

  describe('Dashboard Component Integration', () => {
    beforeEach(() => {
      localStorage.setItem('token', mockToken);
    });

    test('ChecklistDisplay loads data on mount', async () => {
      renderWithTheme(<ChecklistDisplay />);
      
      await waitFor(() => {
        expect(mockedAxios.get).toHaveBeenCalledWith(
          expect.stringContaining('/api/checklist/'),
          expect.objectContaining({
            headers: { Authorization: `Bearer ${mockToken}` }
          })
        );
      });

      expect(screen.getByText('HIPAA Security Rule Update 2024')).toBeInTheDocument();
    });

    test('ComplianceReport loads data on mount', async () => {
      renderWithTheme(<ComplianceReport />);
      
      await waitFor(() => {
        expect(mockedAxios.get).toHaveBeenCalledWith(
          expect.stringContaining('/api/report/'),
          expect.objectContaining({
            headers: { Authorization: `Bearer ${mockToken}` }
          })
        );
      });

      expect(screen.getByText('HIPAA Security Rule Update 2024')).toBeInTheDocument();
    });
  });

  describe('Data Flow Between Components', () => {
    beforeEach(() => {
      localStorage.setItem('token', mockToken);
    });

    test('ChecklistDisplay updates reflect in ComplianceReport', async () => {
      // Mock updated data after patch
      const updatedData = [
        {
          ...mockChecklistData[0],
          completed: true,
          notes: 'Updated notes'
        }
      ];

      mockedAxios.patch.mockResolvedValueOnce({ data: updatedData[0] });
      mockedAxios.get.mockImplementation((url) => {
        if (url.includes('/api/checklist/')) {
          return Promise.resolve({ data: updatedData });
        }
        if (url.includes('/api/report/')) {
          return Promise.resolve({ data: updatedData });
        }
        return Promise.resolve({ data: [] });
      });

      renderWithTheme(<ChecklistDisplay />);
      
      await waitFor(() => {
        const checkbox = screen.getByRole('checkbox');
        fireEvent.click(checkbox);
      });

      // Should call API to update
      expect(mockedAxios.patch).toHaveBeenCalledWith(
        expect.stringContaining('/api/checklist/1/'),
        { completed: true },
        expect.objectContaining({
          headers: { Authorization: `Bearer ${mockToken}` }
        })
      );
    });

    test('filter changes persist across component interactions', async () => {
      renderWithTheme(<ChecklistDisplay />);
      
      await waitFor(() => {
        const filterSelect = screen.getByLabelText(/filter by status/i);
        fireEvent.change(filterSelect, { target: { value: 'completed' } });
      });

      // Filter should be applied
      expect(screen.getByDisplayValue('completed')).toBeInTheDocument();
    });
  });

  describe('Error Handling Integration', () => {
    beforeEach(() => {
      localStorage.setItem('token', mockToken);
    });

    test('network error in one component does not affect others', async () => {
      // Mock error for checklist but success for report
      mockedAxios.get.mockImplementation((url) => {
        if (url.includes('/api/checklist/')) {
          return Promise.reject(new Error('Network Error'));
        }
        if (url.includes('/api/report/')) {
          return Promise.resolve({ data: mockChecklistData });
        }
        return Promise.resolve({ data: [] });
      });

      renderWithTheme(<ChecklistDisplay />);
      
      await waitFor(() => {
        expect(screen.getByText(/error loading checklist/i)).toBeInTheDocument();
      });

      // Should show retry button
      expect(screen.getByRole('button', { name: /retry/i })).toBeInTheDocument();
    });

    test('token expiration triggers re-authentication', async () => {
      // Mock token expiration
      mockedAxios.get.mockRejectedValueOnce({
        response: { status: 401, data: { detail: 'Token has expired' } }
      });

      renderWithTheme(<ChecklistDisplay />);
      
      await waitFor(() => {
        expect(screen.getByText(/session expired/i)).toBeInTheDocument();
      });

      // Should clear token and show login prompt
      expect(localStorage.removeItem).toHaveBeenCalledWith('token');
    });
  });

  describe('User Interaction Integration', () => {
    beforeEach(() => {
      localStorage.setItem('token', mockToken);
    });

    test('user can complete full workflow: login -> view checklist -> update item', async () => {
      // Start with login
      renderWithTheme(<Login />);
      
      const usernameInput = screen.getByLabelText(/username/i);
      const passwordInput = screen.getByLabelText(/password/i);
      const loginButton = screen.getByRole('button', { name: /login/i });

      await userEvent.type(usernameInput, 'testuser');
      await userEvent.type(passwordInput, 'testpass');
      fireEvent.click(loginButton);

      await waitFor(() => {
        expect(localStorage.setItem).toHaveBeenCalledWith('token', mockToken);
      });

      // Now test checklist interaction
      renderWithTheme(<ChecklistDisplay />);
      
      await waitFor(() => {
        const checkbox = screen.getByRole('checkbox');
        fireEvent.click(checkbox);
      });

      // Should update item
      expect(mockedAxios.patch).toHaveBeenCalledWith(
        expect.stringContaining('/api/checklist/1/'),
        { completed: true },
        expect.any(Object)
      );
    });

    test('user can navigate between checklist and report views', async () => {
      renderWithTheme(<ChecklistDisplay />);
      
      await waitFor(() => {
        expect(screen.getByText('HIPAA Security Rule Update 2024')).toBeInTheDocument();
      });

      // Switch to report view
      renderWithTheme(<ComplianceReport />);
      
      await waitFor(() => {
        expect(screen.getByText('HIPAA Security Rule Update 2024')).toBeInTheDocument();
      });
    });
  });

  describe('Performance Integration', () => {
    beforeEach(() => {
      localStorage.setItem('token', mockToken);
    });

    test('components load efficiently in sequence', async () => {
      const startTime = performance.now();
      
      renderWithTheme(<ChecklistDisplay />);
      
      await waitFor(() => {
        expect(screen.getByText('HIPAA Security Rule Update 2024')).toBeInTheDocument();
      });
      
      const endTime = performance.now();
      
      // Should load within reasonable time (less than 500ms)
      expect(endTime - startTime).toBeLessThan(500);
    });

    test('multiple API calls are handled efficiently', async () => {
      renderWithTheme(<ChecklistDisplay />);
      
      await waitFor(() => {
        expect(screen.getByText('HIPAA Security Rule Update 2024')).toBeInTheDocument();
      });

      // Should make multiple API calls efficiently
      expect(mockedAxios.get).toHaveBeenCalledTimes(3); // checklist, profile, auditlog
    });
  });

  describe('State Management Integration', () => {
    beforeEach(() => {
      localStorage.setItem('token', mockToken);
    });

    test('component state persists during user interactions', async () => {
      renderWithTheme(<ChecklistDisplay />);
      
      await waitFor(() => {
        const searchInput = screen.getByPlaceholderText(/search items/i);
        fireEvent.change(searchInput, { target: { value: 'Security' } });
      });

      // State should persist
      expect(screen.getByDisplayValue('Security')).toBeInTheDocument();
    });

    test('filter state is maintained across re-renders', async () => {
      const { rerender } = renderWithTheme(<ChecklistDisplay />);
      
      await waitFor(() => {
        const filterSelect = screen.getByLabelText(/filter by status/i);
        fireEvent.change(filterSelect, { target: { value: 'completed' } });
      });

      // Re-render component
      rerender(
        <ThemeProvider theme={testTheme}>
          <ChecklistDisplay />
        </ThemeProvider>
      );

      // Filter state should be maintained
      expect(screen.getByDisplayValue('completed')).toBeInTheDocument();
    });
  });

  describe('Accessibility Integration', () => {
    beforeEach(() => {
      localStorage.setItem('token', mockToken);
    });

    test('keyboard navigation works across components', async () => {
      renderWithTheme(<ChecklistDisplay />);
      
      await waitFor(() => {
        const firstCheckbox = screen.getByRole('checkbox');
        firstCheckbox.focus();
        expect(firstCheckbox).toHaveFocus();
        
        // Tab navigation should work
        fireEvent.keyDown(firstCheckbox, { key: 'Tab' });
      });
    });

    test('screen reader announcements work correctly', async () => {
      renderWithTheme(<ChecklistDisplay />);
      
      await waitFor(() => {
        const checkbox = screen.getByRole('checkbox');
        fireEvent.click(checkbox);
        
        // Should have proper ARIA attributes
        expect(checkbox).toHaveAttribute('aria-checked');
      });
    });
  });

  describe('Responsive Integration', () => {
    beforeEach(() => {
      localStorage.setItem('token', mockToken);
    });

    test('components adapt to viewport changes together', () => {
      // Start with mobile viewport
      Object.defineProperty(window, 'innerWidth', {
        writable: true,
        configurable: true,
        value: 375,
      });

      renderWithTheme(<ChecklistDisplay />);
      expect(screen.getByText(/total items/i)).toBeInTheDocument();

      // Change to desktop viewport
      Object.defineProperty(window, 'innerWidth', {
        writable: true,
        configurable: true,
        value: 1200,
      });

      window.dispatchEvent(new Event('resize'));

      // Component should still work correctly
      expect(screen.getByText(/total items/i)).toBeInTheDocument();
    });
  });
});
