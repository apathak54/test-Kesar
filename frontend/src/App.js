import React, { useState } from 'react';
import './App.css';

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
        <h1>Test Case Generator</h1>
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
              <pre>{result.positive_test_cases}</pre>
            </div>
            <div className="result-section">
              <h3>Negative Test Cases</h3>
              <pre>{result.negative_test_cases}</pre>
            </div>
          </div>
        )}
      </main>
    </div>
  );
}

export default App; 