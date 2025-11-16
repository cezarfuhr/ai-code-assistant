/**
 * Tests for the main App component.
 */
import { describe, it, expect, vi } from 'vitest';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import App from '../App';
import * as api from '../services/api';

// Mock the API service
vi.mock('../services/api', () => ({
  apiService: {
    generateCode: vi.fn(),
    explainCode: vi.fn(),
    detectBugs: vi.fn(),
    refactorCode: vi.fn(),
    generateDocumentation: vi.fn(),
  },
}));

describe('App Component', () => {
  it('renders the app header', () => {
    render(<App />);
    expect(screen.getByText('AI Code Assistant')).toBeInTheDocument();
    expect(
      screen.getByText('AI-powered code generation, explanation, and debugging')
    ).toBeInTheDocument();
  });

  it('renders all feature buttons', () => {
    render(<App />);
    expect(screen.getByText('Generate Code')).toBeInTheDocument();
    expect(screen.getByText('Explain Code')).toBeInTheDocument();
    expect(screen.getByText('Detect Bugs')).toBeInTheDocument();
    expect(screen.getByText('Refactor')).toBeInTheDocument();
    expect(screen.getByText('Document')).toBeInTheDocument();
  });

  it('switches between features', () => {
    render(<App />);
    const explainButton = screen.getByText('Explain Code');

    fireEvent.click(explainButton);

    // Check if the UI changed to show code input instead of prompt
    expect(screen.getByText('Your Code:')).toBeInTheDocument();
  });

  it('shows error when generating code without prompt', async () => {
    render(<App />);

    const generateButton = screen.getByRole('button', { name: /Generate Code/i });
    fireEvent.click(generateButton);

    await waitFor(() => {
      expect(screen.getByText('Please enter a prompt')).toBeInTheDocument();
    });
  });

  it('generates code successfully', async () => {
    const mockResponse = {
      success: true,
      code: 'def hello():\n    print("Hello")',
      explanation: 'A simple hello function',
      language: 'python',
    };

    vi.spyOn(api.apiService, 'generateCode').mockResolvedValue(mockResponse);

    render(<App />);

    const promptInput = screen.getByPlaceholderText(/e.g., Create a function/i);
    fireEvent.change(promptInput, { target: { value: 'Create a hello function' } });

    const generateButton = screen.getByRole('button', { name: /Generate Code/i });
    fireEvent.click(generateButton);

    await waitFor(() => {
      expect(api.apiService.generateCode).toHaveBeenCalledWith({
        prompt: 'Create a hello function',
        language: 'python',
      });
    });
  });

  it('changes programming language', () => {
    render(<App />);

    const languageSelect = screen.getByRole('combobox');
    fireEvent.change(languageSelect, { target: { value: 'javascript' } });

    expect(languageSelect).toHaveValue('javascript');
  });
});
