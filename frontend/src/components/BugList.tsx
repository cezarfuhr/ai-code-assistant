/**
 * Component to display detected bugs.
 */
import React from 'react';
import { Bug } from '../services/api';

interface BugListProps {
  bugs: Bug[];
}

const severityColors: Record<string, string> = {
  critical: '#dc2626',
  high: '#ea580c',
  medium: '#f59e0b',
  low: '#84cc16',
  info: '#3b82f6',
};

export const BugList: React.FC<BugListProps> = ({ bugs }) => {
  if (bugs.length === 0) {
    return <div className="no-bugs">No issues detected! Your code looks clean.</div>;
  }

  return (
    <div className="bug-list">
      <h3>Detected Issues ({bugs.length})</h3>
      {bugs.map((bug, index) => (
        <div key={index} className="bug-item">
          <div className="bug-header">
            <span
              className="bug-severity"
              style={{ backgroundColor: severityColors[bug.severity.toLowerCase()] || '#6b7280' }}
            >
              {bug.severity}
            </span>
            {bug.line && <span className="bug-line">Line {bug.line}</span>}
          </div>
          <div className="bug-description">{bug.description}</div>
          <div className="bug-suggestion">
            <strong>Suggestion:</strong> {bug.suggestion}
          </div>
        </div>
      ))}
    </div>
  );
};
