/**
 * Advanced code editor using Monaco Editor (VSCode engine).
 */
import React from 'react';
import Editor from '@monaco-editor/react';

interface MonacoCodeEditorProps {
  value: string;
  onChange: (value: string) => void;
  language?: string;
  readOnly?: boolean;
  theme?: 'vs-dark' | 'vs-light' | 'hc-black';
  height?: string;
  minimap?: boolean;
}

export const MonacoCodeEditor: React.FC<MonacoCodeEditorProps> = ({
  value,
  onChange,
  language = 'python',
  readOnly = false,
  theme = 'vs-dark',
  height = '400px',
  minimap = true,
}) => {
  const handleEditorChange = (value: string | undefined) => {
    onChange(value || '');
  };

  // Map language names to Monaco language IDs
  const getMonacoLanguage = (lang: string): string => {
    const languageMap: Record<string, string> = {
      python: 'python',
      javascript: 'javascript',
      typescript: 'typescript',
      java: 'java',
      go: 'go',
      rust: 'rust',
      cpp: 'cpp',
      'c++': 'cpp',
      csharp: 'csharp',
      'c#': 'csharp',
      ruby: 'ruby',
      php: 'php',
      swift: 'swift',
      kotlin: 'kotlin',
      html: 'html',
      css: 'css',
      sql: 'sql',
      shell: 'shell',
      bash: 'shell',
    };

    return languageMap[lang.toLowerCase()] || 'plaintext';
  };

  return (
    <div className="monaco-editor-container">
      <Editor
        height={height}
        language={getMonacoLanguage(language)}
        value={value}
        onChange={handleEditorChange}
        theme={theme}
        options={{
          readOnly,
          minimap: { enabled: minimap },
          fontSize: 14,
          lineNumbers: 'on',
          roundedSelection: true,
          scrollBeyondLastLine: false,
          automaticLayout: true,
          tabSize: 4,
          wordWrap: 'on',
          formatOnPaste: true,
          formatOnType: true,
          suggest: {
            showKeywords: true,
            showSnippets: true,
          },
          quickSuggestions: !readOnly,
          suggestOnTriggerCharacters: !readOnly,
          acceptSuggestionOnEnter: readOnly ? 'off' : 'on',
          padding: { top: 10, bottom: 10 },
        }}
        loading={<div className="editor-loading">Loading editor...</div>}
      />
    </div>
  );
};
