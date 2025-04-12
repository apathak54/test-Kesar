import React, { useState } from 'react';
import './App.css';

const TestCase = ({ title, preCondition, steps, expectedResults }) => (
  <div className="test-case">
    <div className="test-case-title">{title}</div>
    
    <div className="test-case-section">
      <div className="test-case-section-title">Pre-condition:</div>
      <div className="test-case-content">
        {preCondition.split('\n').map((line, index) => (
          <div key={index}>{line}</div>
        ))}
      </div>
    </div>
    
    <div className="test-case-section">
      <div className="test-case-section-title">Steps:</div>
      <ul className="steps-list">
        {steps.map((step, index) => (
          <li key={index}>{step}</li>
        ))}
      </ul>
    </div>
    
    <div className="test-case-section">
      <div className="test-case-section-title">Expected Results:</div>
      <ul className="steps-list">
        {expectedResults.map((result, index) => (
          <li key={index}>{result}</li>
        ))}
      </ul>
    </div>
  </div>
);

const parseTestCases = (testCasesString) => {
  if (!testCasesString) return [];
  
  const lines = testCasesString.split('\n');
  const testCases = [];
  let currentTestCase = null;
  let currentSection = null;

  lines.forEach(line => {
    const trimmedLine = line.trim();
    
    if (trimmedLine.includes('Test Case')) {
      if (currentTestCase) {
        testCases.push(currentTestCase);
      }
      currentTestCase = {
        title: trimmedLine.replace(/#/g, '').trim(),
        preCondition: '',
        steps: [],
        expectedResults: []
      };
      currentSection = null;
    } else if (trimmedLine.includes('Pre-condition:')) {
      currentSection = 'preCondition';
    } else if (trimmedLine.includes('Steps:')) {
      currentSection = 'steps';
    } else if (trimmedLine.includes('Expected Results:')) {
      currentSection = 'expectedResults';
    } else if (trimmedLine && currentTestCase) {
      if (currentSection === 'preCondition') {
        // Split the line by dashes and handle each part
        const parts = trimmedLine.split('-').filter(part => part.trim());
        if (parts.length > 0) {
          if (currentTestCase.preCondition) {
            currentTestCase.preCondition += '\n' + parts.map(part => part.trim()).join('\n');
          } else {
            currentTestCase.preCondition = parts.map(part => part.trim()).join('\n');
          }
        } else {
          // Handle non-dash lines
          if (currentTestCase.preCondition) {
            currentTestCase.preCondition += ' ' + trimmedLine.replace(/\*/g, '');
          } else {
            currentTestCase.preCondition = trimmedLine.replace(/\*/g, '');
          }
        }
      } else if (currentSection === 'steps' && trimmedLine.match(/^\d+\./)) {
        currentTestCase.steps.push(trimmedLine.replace(/^\d+\./, '').trim());
      } else if (currentSection === 'expectedResults' && trimmedLine.startsWith('-')) {
        currentTestCase.expectedResults.push(trimmedLine.replace('-', '').trim());
      }
    }
  });

  if (currentTestCase) {
    testCases.push(currentTestCase);
  }

  return testCases;
};

function App() {
  const [pbi, setPbi] = useState('');
  const [additionalDetails, setAdditionalDetails] = useState('');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    setResult(null);

    try {
      const response = await fetch('http://localhost:5000/api/generate-test-cases', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          pbi,
          additional_details: additionalDetails,
        }),
      });

      const data = await response.json();

      if (!data.success) {
        throw new Error(data.error);
      }

      setResult(data.data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>Test Kesar</h1>
      </header>
      <main>
        <form onSubmit={handleSubmit} className="input-form">
          <div className="form-group">
            <label htmlFor="pbi">PBI:</label>
            <textarea
              id="pbi"
              value={pbi}
              onChange={(e) => setPbi(e.target.value)}
              placeholder="Enter your PBI here..."
              required
            />
          </div>
          <div className="form-group">
            <label htmlFor="additionalDetails">Additional Details:</label>
            <textarea
              id="additionalDetails"
              value={additionalDetails}
              onChange={(e) => setAdditionalDetails(e.target.value)}
              placeholder="Enter any additional details..."
            />
          </div>
          <button type="submit" disabled={loading}>
            {loading ? 'Generating...' : 'Generate Test Cases'}
          </button>
        </form>

        {error && (
          <div className="error">
            <h3>Error</h3>
            <p>{error}</p>
          </div>
        )}

        {result && (
          <div className="results">
            <div className="result-section">
              <h3>Positive Test Cases</h3>
              <div className="test-cases-container">
                {parseTestCases(result.positive_test_cases).map((testCase, index) => (
                  <TestCase key={index} {...testCase} />
                ))}
              </div>
            </div>
            <div className="result-section">
              <h3>Negative Test Cases</h3>
              <div className="test-cases-container">
                {parseTestCases(result.negative_test_cases).map((testCase, index) => (
                  <TestCase key={index} {...testCase} />
                ))}
              </div>
            </div>
          </div>
        )}
      </main>
    </div>
  );
}

export default App; 