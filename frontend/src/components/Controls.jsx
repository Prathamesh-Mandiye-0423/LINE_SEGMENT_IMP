import React from 'react';
import './Controls.css';

const Controls = ({
  currentColor,
  setCurrentColor,
  algorithmType,
  setAlgorithmType,
  usePST,
  setUsePST,
  onCompute,
  onClear,
  onClearColor,
  onGenerateRandom,
  loading,
  redCount,
  blueCount
}) => {
  return (
    <div className="controls">
      <div className="control-section">
        <h3>Segment Type</h3>
        <div className="button-group">
          <button
            className={`btn ${currentColor === 'red' ? 'btn-red active' : 'btn-red'}`}
            onClick={() => setCurrentColor('red')}
          >
            Red ({redCount})
          </button>
          <button
            className={`btn ${currentColor === 'blue' ? 'btn-blue active' : 'btn-blue'}`}
            onClick={() => setCurrentColor('blue')}
          >
            Blue ({blueCount})
          </button>
        </div>
      </div>

      <div className="control-section">
        <h3>Algorithm Type</h3>
        <div className="radio-group">
          <label>
            <input
              type="radio"
              value="rectangles"
              checked={algorithmType === 'rectangles'}
              onChange={(e) => setAlgorithmType(e.target.value)}
            />
            <span>Two Rectangles</span>
            <small>O(n^2+nm) time</small>
          </label>
          <label>
            <input
              type="radio"
              value="squares"
              checked={algorithmType === 'squares'}
              onChange={(e) => setAlgorithmType(e.target.value)}
            />
            <span>Two Squares</span>
            <small>O(nm^2 + n^2) time</small>
          </label>
        </div>
      </div>

      {algorithmType === 'squares' && (
        <div className="control-section">
          <h3>Square Algorithm</h3>
          <div className="checkbox-group">
            <label>
              <input
                type="checkbox"
                checked={usePST}
                onChange={(e) => setUsePST(e.target.checked)}
              />
              <span>Use Priority Search Tree</span>
              <small>{'O(nm^2 + n^2)'}</small>
            </label>
          </div>
        </div>
      )}

      <div className="control-section">
        <h3>Actions</h3>
        <div className="action-buttons">
          <button
            className="btn btn-primary"
            onClick={onCompute}
            disabled={loading || redCount < 2}
          >
            {loading ? 'Computing...' : 'Compute Separators'}
          </button>
          <button
            className="btn btn-secondary"
            onClick={onGenerateRandom}
            disabled={loading}
          >
            Generate Random
          </button>
          <button
            className="btn btn-warning"
            onClick={onClearColor}
            disabled={loading}
          >
            Clear {currentColor.charAt(0).toUpperCase() + currentColor.slice(1)}
          </button>
          <button
            className="btn btn-danger"
            onClick={onClear}
            disabled={loading}
          >
            Clear All
          </button>
        </div>
      </div>

      <div className="info-section">
        <h3>Instructions</h3>
        <ol>
          <li>Select segment color (Red or Blue)</li>
          <li>Click and drag on canvas to draw segments</li>
          <li>Add at least 2 red segments</li>
          <li>Choose algorithm type</li>
          <li>Click "Compute Separators"</li>
        </ol>
        <p className="note">
          <strong>Red segments</strong> must be covered.<br/>
          <strong>Blue segments</strong> should be minimized.
        </p>
      </div>
    </div>
  );
};

export default Controls;