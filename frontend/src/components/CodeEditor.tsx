/**
 * Code editor component with syntax highlighting.
 */
import React from 'react';

interface CodeEditorProps {
  value: string;
  onChange: (value: string) => void;
  placeholder?: string;
  language?: string;
  readOnly?: boolean;
}

export const CodeEditor: React.FC<CodeEditorProps> = ({
  value,
  onChange,
  placeholder = 'Enter your code here...',
  language = 'python',
  readOnly = false,
}) => {
  return (
    <div className="code-editor">
      <textarea
        value={value}
        onChange={(e) => onChange(e.target.value)}
        placeholder={placeholder}
        className="code-textarea"
        spellCheck={false}
        readOnly={readOnly}
        data-language={language}
      />
    </div>
  );
};
