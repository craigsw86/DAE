import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { ThemeProvider, createTheme } from '@mui/material/styles';
import axios from 'axios';
import Login from '../Login';

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

describe('Login Component', () => {
  beforeEach(() => {
    // Clear all mocks before each test
    jest.clearAllMocks();
    localStorage.clear();
  });

  describe('Rendering', () => {
    test('renders login form with all required elements', () => {
      renderWithTheme(<Login />);
      
      // Check for form elements
      expect(screen.getByLabelText(/username/i)).toBeInTheDocument();
      expect(screen.getByLabelText(/password/i)).toBeInTheDocument();
      expect(screen.getByRole('button', { name: /login/i })).toBeInTheDocument();
      expect(screen.getByText(/hipaa compliance checklist/i)).toBeInTheDocument();
    });

    test('renders with correct initial state', () => {
      renderWithTheme(<Login />);
      
      // Check initial form state
      expect(screen.getByLabelText(/username/i)).toHaveValue('');
      expect(screen.getByLabelText(/password/i)).toHaveValue('');
      expect(screen.getByRole('button', { name: /login/i })).not.toBeDisabled();
    });

    test('displays loading state when logging in', async () => {
      // Mock a delayed response
      mockedAxios.post.mockImplementation(() => 
        new Promise(resolve => setTimeout(() => resolve({
          data: { access: 'mock-token', refresh: 'mock-refresh' }
        }), 100))
      );

      renderWithTheme(<Login />);
      
      const usernameInput = screen.getByLabelText(/username/i);
      const passwordInput = screen.getByLabelText(/password/i);
      const loginButton = screen.getByRole('button', { name: /login/i });

      // Fill form and submit
      await userEvent.type(usernameInput, 'testuser');
      await userEvent.type(passwordInput, 'testpass');
      fireEvent.click(loginButton);

      // Check loading state
      expect(loginButton).toBeDisabled();
      expect(screen.getByText(/logging in/i)).toBeInTheDocument();
    });
  });

  describe('Form Validation', () => {
    test('shows error for empty username', async () => {
      renderWithTheme(<Login />);
      
      const loginButton = screen.getByRole('button', { name: /login/i });
      fireEvent.click(loginButton);

      await waitFor(() => {
        expect(screen.getByText(/username is required/i)).toBeInTheDocument();
      });
    });

    test('shows error for empty password', async () => {
      renderWithTheme(<Login />);
      
      const usernameInput = screen.getByLabelText(/username/i);
      const loginButton = screen.getByRole('button', { name: /login/i });

      await userEvent.type(usernameInput, 'testuser');
      fireEvent.click(loginButton);

      await waitFor(() => {
        expect(screen.getByText(/password is required/i)).toBeInTheDocument();
      });
    });

    test('shows error for both empty fields', async () => {
      renderWithTheme(<Login />);
      
      const loginButton = screen.getByRole('button', { name: /login/i });
      fireEvent.click(loginButton);

      await waitFor(() => {
        expect(screen.getByText(/username is required/i)).toBeInTheDocument();
        expect(screen.getByText(/password is required/i)).toBeInTheDocument();
      });
    });

    test('clears errors when user starts typing', async () => {
      renderWithTheme(<Login />);
      
      const usernameInput = screen.getByLabelText(/username/i);
      const loginButton = screen.getByRole('button', { name: /login/i });

      // Trigger validation error
      fireEvent.click(loginButton);
      await waitFor(() => {
        expect(screen.getByText(/username is required/i)).toBeInTheDocument();
      });

      // Start typing to clear error
      await userEvent.type(usernameInput, 'test');
      await waitFor(() => {
        expect(screen.queryByText(/username is required/i)).not.toBeInTheDocument();
      });
    });
  });

  describe('API Integration', () => {
    test('successful login saves token and redirects', async () => {
      const mockToken = 'mock-access-token';
      const mockRefreshToken = 'mock-refresh-token';
      
      mockedAxios.post.mockResolvedValueOnce({
        data: {
          access: mockToken,
          refresh: mockRefreshToken
        }
      });

      renderWithTheme(<Login />);
      
      const usernameInput = screen.getByLabelText(/username/i);
      const passwordInput = screen.getByLabelText(/password/i);
      const loginButton = screen.getByRole('button', { name: /login/i });

      // Fill form and submit
      await userEvent.type(usernameInput, 'testuser');
      await userEvent.type(passwordInput, 'testpass');
      fireEvent.click(loginButton);

      // Wait for API call
      await waitFor(() => {
        expect(mockedAxios.post).toHaveBeenCalledWith(
          'http://localhost:8000/api/token/',
          {
            username: 'testuser',
            password: 'testpass'
          }
        );
      });

      // Check token storage
      expect(localStorage.setItem).toHaveBeenCalledWith('token', mockToken);
      expect(localStorage.setItem).toHaveBeenCalledWith('refreshToken', mockRefreshToken);
    });

    test('handles login failure with 401 error', async () => {
      mockedAxios.post.mockRejectedValueOnce({
        response: {
          status: 401,
          data: { detail: 'Invalid credentials' }
        }
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
    });

    test('handles network error', async () => {
      mockedAxios.post.mockRejectedValueOnce(new Error('Network Error'));

      renderWithTheme(<Login />);
      
      const usernameInput = screen.getByLabelText(/username/i);
      const passwordInput = screen.getByLabelText(/password/i);
      const loginButton = screen.getByRole('button', { name: /login/i });

      await userEvent.type(usernameInput, 'testuser');
      await userEvent.type(passwordInput, 'testpass');
      fireEvent.click(loginButton);

      await waitFor(() => {
        expect(screen.getByText(/network error. please try again/i)).toBeInTheDocument();
      });
    });

    test('handles server error (500)', async () => {
      mockedAxios.post.mockRejectedValueOnce({
        response: {
          status: 500,
          data: { detail: 'Internal server error' }
        }
      });

      renderWithTheme(<Login />);
      
      const usernameInput = screen.getByLabelText(/username/i);
      const passwordInput = screen.getByLabelText(/password/i);
      const loginButton = screen.getByRole('button', { name: /login/i });

      await userEvent.type(usernameInput, 'testuser');
      await userEvent.type(passwordInput, 'testpass');
      fireEvent.click(loginButton);

      await waitFor(() => {
        expect(screen.getByText(/server error. please try again later/i)).toBeInTheDocument();
      });
    });
  });

  describe('User Interactions', () => {
    test('allows user to type in username field', async () => {
      renderWithTheme(<Login />);
      
      const usernameInput = screen.getByLabelText(/username/i);
      await userEvent.type(usernameInput, 'testuser');
      
      expect(usernameInput).toHaveValue('testuser');
    });

    test('allows user to type in password field', async () => {
      renderWithTheme(<Login />);
      
      const passwordInput = screen.getByLabelText(/password/i);
      await userEvent.type(passwordInput, 'testpass');
      
      expect(passwordInput).toHaveValue('testpass');
    });

    test('submits form on Enter key press', async () => {
      mockedAxios.post.mockResolvedValueOnce({
        data: { access: 'mock-token', refresh: 'mock-refresh' }
      });

      renderWithTheme(<Login />);
      
      const usernameInput = screen.getByLabelText(/username/i);
      const passwordInput = screen.getByLabelText(/password/i);

      await userEvent.type(usernameInput, 'testuser');
      await userEvent.type(passwordInput, 'testpass');
      
      // Press Enter in password field
      fireEvent.keyDown(passwordInput, { key: 'Enter', code: 'Enter' });

      await waitFor(() => {
        expect(mockedAxios.post).toHaveBeenCalled();
      });
    });

    test('retry button works after error', async () => {
      // First attempt fails
      mockedAxios.post
        .mockRejectedValueOnce({
          response: { status: 401, data: { detail: 'Invalid credentials' } }
        })
        .mockResolvedValueOnce({
          data: { access: 'mock-token', refresh: 'mock-refresh' }
        });

      renderWithTheme(<Login />);
      
      const usernameInput = screen.getByLabelText(/username/i);
      const passwordInput = screen.getByLabelText(/password/i);
      const loginButton = screen.getByRole('button', { name: /login/i });

      // First login attempt
      await userEvent.type(usernameInput, 'wronguser');
      await userEvent.type(passwordInput, 'wrongpass');
      fireEvent.click(loginButton);

      await waitFor(() => {
        expect(screen.getByText(/invalid username or password/i)).toBeInTheDocument();
      });

      // Click retry button
      const retryButton = screen.getByRole('button', { name: /retry/i });
      fireEvent.click(retryButton);

      // Check that form is cleared and ready for retry
      expect(usernameInput).toHaveValue('');
      expect(passwordInput).toHaveValue('');
    });
  });

  describe('Accessibility', () => {
    test('has proper ARIA labels', () => {
      renderWithTheme(<Login />);
      
      expect(screen.getByLabelText(/username/i)).toBeInTheDocument();
      expect(screen.getByLabelText(/password/i)).toBeInTheDocument();
      expect(screen.getByRole('button', { name: /login/i })).toBeInTheDocument();
    });

    test('supports keyboard navigation', async () => {
      renderWithTheme(<Login />);
      
      const usernameInput = screen.getByLabelText(/username/i);
      const passwordInput = screen.getByLabelText(/password/i);
      const loginButton = screen.getByRole('button', { name: /login/i });

      // Tab navigation
      usernameInput.focus();
      expect(usernameInput).toHaveFocus();
      
      fireEvent.keyDown(usernameInput, { key: 'Tab' });
      expect(passwordInput).toHaveFocus();
      
      fireEvent.keyDown(passwordInput, { key: 'Tab' });
      expect(loginButton).toHaveFocus();
    });

    test('announces errors to screen readers', async () => {
      renderWithTheme(<Login />);
      
      const loginButton = screen.getByRole('button', { name: /login/i });
      fireEvent.click(loginButton);

      await waitFor(() => {
        const errorMessage = screen.getByText(/username is required/i);
        expect(errorMessage).toHaveAttribute('role', 'alert');
      });
    });
  });

  describe('Responsive Design', () => {
    test('adapts to mobile viewport', () => {
      // Mock mobile viewport
      Object.defineProperty(window, 'innerWidth', {
        writable: true,
        configurable: true,
        value: 375,
      });

      renderWithTheme(<Login />);
      
      // Check that component renders without errors on mobile
      expect(screen.getByLabelText(/username/i)).toBeInTheDocument();
      expect(screen.getByLabelText(/password/i)).toBeInTheDocument();
    });

    test('adapts to tablet viewport', () => {
      // Mock tablet viewport
      Object.defineProperty(window, 'innerWidth', {
        writable: true,
        configurable: true,
        value: 768,
      });

      renderWithTheme(<Login />);
      
      // Check that component renders without errors on tablet
      expect(screen.getByLabelText(/username/i)).toBeInTheDocument();
      expect(screen.getByLabelText(/password/i)).toBeInTheDocument();
    });

    test('adapts to desktop viewport', () => {
      // Mock desktop viewport
      Object.defineProperty(window, 'innerWidth', {
        writable: true,
        configurable: true,
        value: 1200,
      });

      renderWithTheme(<Login />);
      
      // Check that component renders without errors on desktop
      expect(screen.getByLabelText(/username/i)).toBeInTheDocument();
      expect(screen.getByLabelText(/password/i)).toBeInTheDocument();
    });
  });
});
