/**
 * Main application component.
 */
import React, { useState } from 'react';
import { CodeEditor } from './components/CodeEditor';
import { BugList } from './components/BugList';
import { apiService, Bug } from './services/api';
import './styles/App.css';

type Feature = 'generate' | 'explain' | 'bugs' | 'refactor' | 'document';

function App() {
  const [activeFeature, setActiveFeature] = useState<Feature>('generate');
  const [code, setCode] = useState('');
  const [prompt, setPrompt] = useState('');
  const [language, setLanguage] = useState('python');
  const [output, setOutput] = useState('');
  const [bugs, setBugs] = useState<Bug[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleGenerate = async () => {
    if (!prompt.trim()) {
      setError('Please enter a prompt');
      return;
    }

    setLoading(true);
    setError('');
    try {
      const response = await apiService.generateCode({
        prompt,
        language,
      });
      setCode(response.code || '');
      setOutput(response.explanation || '');
    } catch (err) {
      setError('Failed to generate code. Please check your API key and try again.');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleExplain = async () => {
    if (!code.trim()) {
      setError('Please enter code to explain');
      return;
    }

    setLoading(true);
    setError('');
    try {
      const response = await apiService.explainCode({ code, language });
      setOutput(response.explanation || '');
    } catch (err) {
      setError('Failed to explain code.');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleDetectBugs = async () => {
    if (!code.trim()) {
      setError('Please enter code to analyze');
      return;
    }

    setLoading(true);
    setError('');
    try {
      const response = await apiService.detectBugs({ code, language });
      setBugs(response.bugs || []);
      setOutput(response.explanation || '');
    } catch (err) {
      setError('Failed to detect bugs.');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleRefactor = async () => {
    if (!code.trim()) {
      setError('Please enter code to refactor');
      return;
    }

    setLoading(true);
    setError('');
    try {
      const response = await apiService.refactorCode({ code, language });
      setCode(response.code || '');
      setOutput(response.explanation || '');
    } catch (err) {
      setError('Failed to refactor code.');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleDocument = async () => {
    if (!code.trim()) {
      setError('Please enter code to document');
      return;
    }

    setLoading(true);
    setError('');
    try {
      const response = await apiService.generateDocumentation({
        code,
        language,
        style: 'google',
      });
      setCode(response.code || '');
      setOutput(response.explanation || '');
    } catch (err) {
      setError('Failed to generate documentation.');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleAction = () => {
    switch (activeFeature) {
      case 'generate':
        handleGenerate();
        break;
      case 'explain':
        handleExplain();
        break;
      case 'bugs':
        handleDetectBugs();
        break;
      case 'refactor':
        handleRefactor();
        break;
      case 'document':
        handleDocument();
        break;
    }
  };

  return (
    <div className="app">
      <header className="app-header">
        <h1>AI Code Assistant</h1>
        <p>AI-powered code generation, explanation, and debugging</p>
      </header>

      <div className="features">
        <button
          className={activeFeature === 'generate' ? 'active' : ''}
          onClick={() => setActiveFeature('generate')}
        >
          Generate Code
        </button>
        <button
          className={activeFeature === 'explain' ? 'active' : ''}
          onClick={() => setActiveFeature('explain')}
        >
          Explain Code
        </button>
        <button
          className={activeFeature === 'bugs' ? 'active' : ''}
          onClick={() => setActiveFeature('bugs')}
        >
          Detect Bugs
        </button>
        <button
          className={activeFeature === 'refactor' ? 'active' : ''}
          onClick={() => setActiveFeature('refactor')}
        >
          Refactor
        </button>
        <button
          className={activeFeature === 'document' ? 'active' : ''}
          onClick={() => setActiveFeature('document')}
        >
          Document
        </button>
      </div>

      <div className="controls">
        <select value={language} onChange={(e) => setLanguage(e.target.value)}>
          <option value="python">Python</option>
          <option value="javascript">JavaScript</option>
          <option value="typescript">TypeScript</option>
          <option value="java">Java</option>
          <option value="go">Go</option>
          <option value="rust">Rust</option>
          <option value="cpp">C++</option>
        </select>
      </div>

      <div className="workspace">
        <div className="input-section">
          {activeFeature === 'generate' ? (
            <div className="prompt-input">
              <label>Describe the code you want to generate:</label>
              <textarea
                value={prompt}
                onChange={(e) => setPrompt(e.target.value)}
                placeholder="e.g., Create a function to calculate fibonacci numbers"
                rows={5}
              />
            </div>
          ) : (
            <>
              <label>Your Code:</label>
              <CodeEditor value={code} onChange={setCode} language={language} />
            </>
          )}
        </div>

        <div className="action-section">
          <button
            className="action-button"
            onClick={handleAction}
            disabled={loading}
          >
            {loading ? 'Processing...' : getActionLabel(activeFeature)}
          </button>
          {error && <div className="error">{error}</div>}
        </div>

        <div className="output-section">
          <label>Result:</label>
          {activeFeature === 'bugs' && bugs.length > 0 ? (
            <BugList bugs={bugs} />
          ) : (
            <>
              {(activeFeature === 'generate' || activeFeature === 'refactor' || activeFeature === 'document') && code && (
                <CodeEditor value={code} onChange={setCode} language={language} readOnly />
              )}
              {output && (
                <div className="explanation">
                  <h3>Explanation:</h3>
                  <p>{output}</p>
                </div>
              )}
            </>
          )}
        </div>
      </div>
    </div>
  );
}

function getActionLabel(feature: Feature): string {
  switch (feature) {
    case 'generate':
      return 'Generate Code';
    case 'explain':
      return 'Explain Code';
    case 'bugs':
      return 'Detect Bugs';
    case 'refactor':
      return 'Refactor Code';
    case 'document':
      return 'Add Documentation';
  }
}

export default App;
