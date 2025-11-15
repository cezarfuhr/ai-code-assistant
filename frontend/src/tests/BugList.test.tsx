/**
 * Tests for BugList component.
 */
import { describe, it, expect } from 'vitest';
import { render, screen } from '@testing-library/react';
import { BugList } from '../components/BugList';
import { Bug } from '../services/api';

describe('BugList Component', () => {
  it('shows message when no bugs are found', () => {
    render(<BugList bugs={[]} />);
    expect(screen.getByText(/No issues detected/i)).toBeInTheDocument();
  });

  it('displays bug count', () => {
    const bugs: Bug[] = [
      {
        line: 10,
        severity: 'high',
        description: 'Null pointer exception',
        suggestion: 'Add null check',
      },
      {
        line: 20,
        severity: 'medium',
        description: 'Unused variable',
        suggestion: 'Remove unused variable',
      },
    ];

    render(<BugList bugs={bugs} />);
    expect(screen.getByText('Detected Issues (2)')).toBeInTheDocument();
  });

  it('displays bug details', () => {
    const bugs: Bug[] = [
      {
        line: 10,
        severity: 'critical',
        description: 'Security vulnerability',
        suggestion: 'Sanitize user input',
      },
    ];

    render(<BugList bugs={bugs} />);

    expect(screen.getByText('critical')).toBeInTheDocument();
    expect(screen.getByText('Line 10')).toBeInTheDocument();
    expect(screen.getByText('Security vulnerability')).toBeInTheDocument();
    expect(screen.getByText(/Sanitize user input/i)).toBeInTheDocument();
  });

  it('displays bugs without line numbers', () => {
    const bugs: Bug[] = [
      {
        line: null,
        severity: 'low',
        description: 'Code style issue',
        suggestion: 'Follow PEP 8',
      },
    ];

    render(<BugList bugs={bugs} />);

    expect(screen.getByText('Code style issue')).toBeInTheDocument();
    expect(screen.queryByText(/Line/i)).not.toBeInTheDocument();
  });

  it('displays multiple bugs', () => {
    const bugs: Bug[] = [
      {
        line: 1,
        severity: 'high',
        description: 'Bug 1',
        suggestion: 'Fix 1',
      },
      {
        line: 2,
        severity: 'medium',
        description: 'Bug 2',
        suggestion: 'Fix 2',
      },
      {
        line: 3,
        severity: 'low',
        description: 'Bug 3',
        suggestion: 'Fix 3',
      },
    ];

    render(<BugList bugs={bugs} />);

    expect(screen.getByText('Bug 1')).toBeInTheDocument();
    expect(screen.getByText('Bug 2')).toBeInTheDocument();
    expect(screen.getByText('Bug 3')).toBeInTheDocument();
  });
});
