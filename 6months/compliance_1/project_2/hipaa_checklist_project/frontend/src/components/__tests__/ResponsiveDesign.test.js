import React from 'react';
import { render, screen } from '@testing-library/react';
import { ThemeProvider, createTheme } from '@mui/material/styles';
import Login from '../Login';
import ChecklistDisplay from '../ChecklistDisplay';
import ComplianceReport from '../ComplianceReport';

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

// Mock API responses
jest.mock('axios', () => ({
  get: jest.fn(() => Promise.resolve({ data: [] })),
  post: jest.fn(() => Promise.resolve({ data: { access: 'token', refresh: 'refresh' } })),
  patch: jest.fn(() => Promise.resolve({ data: {} })),
}));

// Mock localStorage
const localStorageMock = {
  getItem: jest.fn(() => 'mock-token'),
  setItem: jest.fn(),
  removeItem: jest.fn(),
  clear: jest.fn(),
};
global.localStorage = localStorageMock;

describe('Responsive Design Tests', () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  describe('Mobile Viewport (375px)', () => {
    beforeEach(() => {
      // Mock mobile viewport
      Object.defineProperty(window, 'innerWidth', {
        writable: true,
        configurable: true,
        value: 375,
      });
      Object.defineProperty(window, 'innerHeight', {
        writable: true,
        configurable: true,
        value: 667,
      });
    });

    test('Login component renders correctly on mobile', () => {
      renderWithTheme(<Login />);
      
      // Should render without errors
      expect(screen.getByLabelText(/username/i)).toBeInTheDocument();
      expect(screen.getByLabelText(/password/i)).toBeInTheDocument();
      expect(screen.getByRole('button', { name: /login/i })).toBeInTheDocument();
    });

    test('ChecklistDisplay component renders correctly on mobile', () => {
      renderWithTheme(<ChecklistDisplay />);
      
      // Should render without errors
      expect(screen.getByText(/total items/i)).toBeInTheDocument();
    });

    test('ComplianceReport component renders correctly on mobile', () => {
      renderWithTheme(<ComplianceReport />);
      
      // Should render without errors
      expect(screen.getByText(/compliance report/i)).toBeInTheDocument();
    });
  });

  describe('Mobile Landscape Viewport (667px)', () => {
    beforeEach(() => {
      // Mock mobile landscape viewport
      Object.defineProperty(window, 'innerWidth', {
        writable: true,
        configurable: true,
        value: 667,
      });
      Object.defineProperty(window, 'innerHeight', {
        writable: true,
        configurable: true,
        value: 375,
      });
    });

    test('Login component renders correctly on mobile landscape', () => {
      renderWithTheme(<Login />);
      
      // Should render without errors
      expect(screen.getByLabelText(/username/i)).toBeInTheDocument();
      expect(screen.getByLabelText(/password/i)).toBeInTheDocument();
      expect(screen.getByRole('button', { name: /login/i })).toBeInTheDocument();
    });

    test('ChecklistDisplay component renders correctly on mobile landscape', () => {
      renderWithTheme(<ChecklistDisplay />);
      
      // Should render without errors
      expect(screen.getByText(/total items/i)).toBeInTheDocument();
    });

    test('ComplianceReport component renders correctly on mobile landscape', () => {
      renderWithTheme(<ComplianceReport />);
      
      // Should render without errors
      expect(screen.getByText(/compliance report/i)).toBeInTheDocument();
    });
  });

  describe('Tablet Viewport (768px)', () => {
    beforeEach(() => {
      // Mock tablet viewport
      Object.defineProperty(window, 'innerWidth', {
        writable: true,
        configurable: true,
        value: 768,
      });
      Object.defineProperty(window, 'innerHeight', {
        writable: true,
        configurable: true,
        value: 1024,
      });
    });

    test('Login component renders correctly on tablet', () => {
      renderWithTheme(<Login />);
      
      // Should render without errors
      expect(screen.getByLabelText(/username/i)).toBeInTheDocument();
      expect(screen.getByLabelText(/password/i)).toBeInTheDocument();
      expect(screen.getByRole('button', { name: /login/i })).toBeInTheDocument();
    });

    test('ChecklistDisplay component renders correctly on tablet', () => {
      renderWithTheme(<ChecklistDisplay />);
      
      // Should render without errors
      expect(screen.getByText(/total items/i)).toBeInTheDocument();
    });

    test('ComplianceReport component renders correctly on tablet', () => {
      renderWithTheme(<ComplianceReport />);
      
      // Should render without errors
      expect(screen.getByText(/compliance report/i)).toBeInTheDocument();
    });
  });

  describe('Tablet Landscape Viewport (1024px)', () => {
    beforeEach(() => {
      // Mock tablet landscape viewport
      Object.defineProperty(window, 'innerWidth', {
        writable: true,
        configurable: true,
        value: 1024,
      });
      Object.defineProperty(window, 'innerHeight', {
        writable: true,
        configurable: true,
        value: 768,
      });
    });

    test('Login component renders correctly on tablet landscape', () => {
      renderWithTheme(<Login />);
      
      // Should render without errors
      expect(screen.getByLabelText(/username/i)).toBeInTheDocument();
      expect(screen.getByLabelText(/password/i)).toBeInTheDocument();
      expect(screen.getByRole('button', { name: /login/i })).toBeInTheDocument();
    });

    test('ChecklistDisplay component renders correctly on tablet landscape', () => {
      renderWithTheme(<ChecklistDisplay />);
      
      // Should render without errors
      expect(screen.getByText(/total items/i)).toBeInTheDocument();
    });

    test('ComplianceReport component renders correctly on tablet landscape', () => {
      renderWithTheme(<ComplianceReport />);
      
      // Should render without errors
      expect(screen.getByText(/compliance report/i)).toBeInTheDocument();
    });
  });

  describe('Desktop Viewport (1200px)', () => {
    beforeEach(() => {
      // Mock desktop viewport
      Object.defineProperty(window, 'innerWidth', {
        writable: true,
        configurable: true,
        value: 1200,
      });
      Object.defineProperty(window, 'innerHeight', {
        writable: true,
        configurable: true,
        value: 800,
      });
    });

    test('Login component renders correctly on desktop', () => {
      renderWithTheme(<Login />);
      
      // Should render without errors
      expect(screen.getByLabelText(/username/i)).toBeInTheDocument();
      expect(screen.getByLabelText(/password/i)).toBeInTheDocument();
      expect(screen.getByRole('button', { name: /login/i })).toBeInTheDocument();
    });

    test('ChecklistDisplay component renders correctly on desktop', () => {
      renderWithTheme(<ChecklistDisplay />);
      
      // Should render without errors
      expect(screen.getByText(/total items/i)).toBeInTheDocument();
    });

    test('ComplianceReport component renders correctly on desktop', () => {
      renderWithTheme(<ComplianceReport />);
      
      // Should render without errors
      expect(screen.getByText(/compliance report/i)).toBeInTheDocument();
    });
  });

  describe('Large Desktop Viewport (1920px)', () => {
    beforeEach(() => {
      // Mock large desktop viewport
      Object.defineProperty(window, 'innerWidth', {
        writable: true,
        configurable: true,
        value: 1920,
      });
      Object.defineProperty(window, 'innerHeight', {
        writable: true,
        configurable: true,
        value: 1080,
      });
    });

    test('Login component renders correctly on large desktop', () => {
      renderWithTheme(<Login />);
      
      // Should render without errors
      expect(screen.getByLabelText(/username/i)).toBeInTheDocument();
      expect(screen.getByLabelText(/password/i)).toBeInTheDocument();
      expect(screen.getByRole('button', { name: /login/i })).toBeInTheDocument();
    });

    test('ChecklistDisplay component renders correctly on large desktop', () => {
      renderWithTheme(<ChecklistDisplay />);
      
      // Should render without errors
      expect(screen.getByText(/total items/i)).toBeInTheDocument();
    });

    test('ComplianceReport component renders correctly on large desktop', () => {
      renderWithTheme(<ComplianceReport />);
      
      // Should render without errors
      expect(screen.getByText(/compliance report/i)).toBeInTheDocument();
    });
  });

  describe('Viewport Change Handling', () => {
    test('components handle viewport changes gracefully', () => {
      // Start with mobile viewport
      Object.defineProperty(window, 'innerWidth', {
        writable: true,
        configurable: true,
        value: 375,
      });

      const { rerender } = renderWithTheme(<Login />);
      expect(screen.getByLabelText(/username/i)).toBeInTheDocument();

      // Change to desktop viewport
      Object.defineProperty(window, 'innerWidth', {
        writable: true,
        configurable: true,
        value: 1200,
      });

      // Trigger resize event
      window.dispatchEvent(new Event('resize'));

      // Component should still render correctly
      expect(screen.getByLabelText(/username/i)).toBeInTheDocument();
    });

    test('components handle orientation changes', () => {
      // Start with portrait orientation
      Object.defineProperty(window, 'innerWidth', {
        writable: true,
        configurable: true,
        value: 375,
      });
      Object.defineProperty(window, 'innerHeight', {
        writable: true,
        configurable: true,
        value: 667,
      });

      renderWithTheme(<ChecklistDisplay />);
      expect(screen.getByText(/total items/i)).toBeInTheDocument();

      // Change to landscape orientation
      Object.defineProperty(window, 'innerWidth', {
        writable: true,
        configurable: true,
        value: 667,
      });
      Object.defineProperty(window, 'innerHeight', {
        writable: true,
        configurable: true,
        value: 375,
      });

      // Trigger orientation change event
      window.dispatchEvent(new Event('orientationchange'));

      // Component should still render correctly
      expect(screen.getByText(/total items/i)).toBeInTheDocument();
    });
  });

  describe('Touch Device Support', () => {
    test('components support touch interactions', () => {
      // Mock touch device
      Object.defineProperty(window, 'ontouchstart', {
        writable: true,
        configurable: true,
        value: true,
      });

      renderWithTheme(<Login />);
      
      // Should render without errors on touch device
      expect(screen.getByLabelText(/username/i)).toBeInTheDocument();
      expect(screen.getByLabelText(/password/i)).toBeInTheDocument();
      expect(screen.getByRole('button', { name: /login/i })).toBeInTheDocument();
    });

    test('components handle touch events', () => {
      renderWithTheme(<ChecklistDisplay />);
      
      // Should render without errors
      expect(screen.getByText(/total items/i)).toBeInTheDocument();
      
      // Touch events should be handled gracefully
      const button = screen.getByRole('button', { name: /export csv/i });
      fireEvent.touchStart(button);
      fireEvent.touchEnd(button);
    });
  });

  describe('High DPI Display Support', () => {
    test('components render correctly on high DPI displays', () => {
      // Mock high DPI display
      Object.defineProperty(window, 'devicePixelRatio', {
        writable: true,
        configurable: true,
        value: 2,
      });

      renderWithTheme(<ComplianceReport />);
      
      // Should render without errors on high DPI display
      expect(screen.getByText(/compliance report/i)).toBeInTheDocument();
    });

    test('components handle different pixel ratios', () => {
      // Test various pixel ratios
      const pixelRatios = [1, 1.5, 2, 3];
      
      pixelRatios.forEach(ratio => {
        Object.defineProperty(window, 'devicePixelRatio', {
          writable: true,
          configurable: true,
          value: ratio,
        });

        renderWithTheme(<Login />);
        expect(screen.getByLabelText(/username/i)).toBeInTheDocument();
      });
    });
  });

  describe('Accessibility on Different Viewports', () => {
    test('maintains accessibility on mobile', () => {
      Object.defineProperty(window, 'innerWidth', {
        writable: true,
        configurable: true,
        value: 375,
      });

      renderWithTheme(<Login />);
      
      // Should maintain proper ARIA labels
      expect(screen.getByLabelText(/username/i)).toBeInTheDocument();
      expect(screen.getByLabelText(/password/i)).toBeInTheDocument();
      expect(screen.getByRole('button', { name: /login/i })).toBeInTheDocument();
    });

    test('maintains accessibility on tablet', () => {
      Object.defineProperty(window, 'innerWidth', {
        writable: true,
        configurable: true,
        value: 768,
      });

      renderWithTheme(<ChecklistDisplay />);
      
      // Should maintain proper ARIA labels
      expect(screen.getByText(/total items/i)).toBeInTheDocument();
    });

    test('maintains accessibility on desktop', () => {
      Object.defineProperty(window, 'innerWidth', {
        writable: true,
        configurable: true,
        value: 1200,
      });

      renderWithTheme(<ComplianceReport />);
      
      // Should maintain proper ARIA labels
      expect(screen.getByText(/compliance report/i)).toBeInTheDocument();
    });
  });

  describe('Performance on Different Viewports', () => {
    test('components load efficiently on mobile', () => {
      Object.defineProperty(window, 'innerWidth', {
        writable: true,
        configurable: true,
        value: 375,
      });

      const startTime = performance.now();
      renderWithTheme(<Login />);
      const endTime = performance.now();
      
      // Should render quickly (less than 100ms)
      expect(endTime - startTime).toBeLessThan(100);
      expect(screen.getByLabelText(/username/i)).toBeInTheDocument();
    });

    test('components load efficiently on desktop', () => {
      Object.defineProperty(window, 'innerWidth', {
        writable: true,
        configurable: true,
        value: 1200,
      });

      const startTime = performance.now();
      renderWithTheme(<ChecklistDisplay />);
      const endTime = performance.now();
      
      // Should render quickly (less than 100ms)
      expect(endTime - startTime).toBeLessThan(100);
      expect(screen.getByText(/total items/i)).toBeInTheDocument();
    });
  });
});
