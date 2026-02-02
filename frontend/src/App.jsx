import React, { useState, useRef, useEffect } from 'react';
import Canvas from './components/Canvas';
import Controls from './components/Controls';
import Results from './components/Results';
import { computeRectangles, computeSquares, generateRandomData } from './utils/api';
import './App.css';

function App() {
  const [redSegments, setRedSegments] = useState([]);
  const [blueSegments, setBlueSegments] = useState([]);
  const [currentColor, setCurrentColor] = useState('red');
  const [algorithmType, setAlgorithmType] = useState('rectangles');
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [usePST, setUsePST] = useState(true);

  const handleAddSegment = (segment) => {
    if (currentColor === 'red') {
      setRedSegments([...redSegments, { ...segment, color: 'red' }]);
    } else {
      setBlueSegments([...blueSegments, { ...segment, color: 'blue' }]);
    }
    setResult(null); // Clear previous results
  };

  const handleClear = () => {
    setRedSegments([]);
    setBlueSegments([]);
    setResult(null);
    setError(null);
  };

  const handleClearColor = () => {
    if (currentColor === 'red') {
      setRedSegments([]);
    } else {
      setBlueSegments([]);
    }
    setResult(null);
  };

  const handleCompute = async () => {
    if (redSegments.length < 2) {
      setError('Please add at least 2 red segments');
      return;
    }

    setLoading(true);
    setError(null);

    try {
      let response;
      if (algorithmType === 'rectangles') {
        response = await computeRectangles(redSegments, blueSegments);
      } else {
        response = await computeSquares(redSegments, blueSegments, usePST);
      }

      if (response.success) {
        setResult(response);
        setError(null);
      } else {
        setError(response.error || 'Computation failed');
        setResult(null);
      }
    } catch (err) {
      setError(err.message || 'Failed to compute separators');
      setResult(null);
    } finally {
      setLoading(false);
    }
  };

  const handleGenerateRandom = async () => {
    setLoading(true);
    setError(null);

    try {
      const data = await generateRandomData({
        num_red: 10,
        num_blue: 15,
        width: 800,
        height: 600,
        max_segment_length: 80
      });

      setRedSegments(data.red_segments);
      setBlueSegments(data.blue_segments);
      setResult(null);
    } catch (err) {
      setError(err.message || 'Failed to generate random data');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="app">
      <header className="app-header">
        <h1>Line Segment Separator</h1>
        <p>Two Disjoint Rectangles/Squares Algorithm Implementation</p>
      </header>

      <div className="app-container">
        <div className="left-panel">
          <Controls
            currentColor={currentColor}
            setCurrentColor={setCurrentColor}
            algorithmType={algorithmType}
            setAlgorithmType={setAlgorithmType}
            usePST={usePST}
            setUsePST={setUsePST}
            onCompute={handleCompute}
            onClear={handleClear}
            onClearColor={handleClearColor}
            onGenerateRandom={handleGenerateRandom}
            loading={loading}
            redCount={redSegments.length}
            blueCount={blueSegments.length}
          />

          {error && (
            <div className="error-message">
              <strong>Error:</strong> {error}
            </div>
          )}

          {result && <Results result={result} algorithmType={algorithmType} />}
        </div>

        <div className="right-panel">
          <Canvas
            redSegments={redSegments}
            blueSegments={blueSegments}
            onAddSegment={handleAddSegment}
            currentColor={currentColor}
            result={result}
            algorithmType={algorithmType}
          />
        </div>
      </div>
    </div>
  );
}

export default App;