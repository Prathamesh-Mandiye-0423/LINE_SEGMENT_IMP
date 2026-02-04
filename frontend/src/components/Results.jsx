import React from 'react';
import './Results.css';

const Results = ({ result, algorithmType }) => {
  if (!result || !result.success) return null;

  const shape1 = algorithmType === 'rectangles' ? result.rectangle1 : result.square1;
  const shape2 = algorithmType === 'rectangles' ? result.rectangle2 : result.square2;
  const shapeName = algorithmType === 'rectangles' ? 'Rectangle' : 'Square';

  return (
    <div className="results">
      <h3>Results</h3>
      
      <div className="result-summary">
        <div className="stat">
          <label>Blue Segments Covered:</label>
          <span className="value">{result.blue_count}</span>
        </div>
        <div className="stat">
          <label>Execution Time:</label>
          <span className="value">{result.execution_time_ms} ms</span>
        </div>
        <div className="stat">
          <label>Separator Type:</label>
          <span className="value">{result.separator_type}</span>
        </div>
        {result.algorithm && (
          <div className="stat">
            <label>Algorithm:</label>
            <span className="value">{result.algorithm}</span>
          </div>
        )}
      </div>

      <div className="shapes-info">
        <div className="shape-details">
          <h4>{shapeName} 1 (Red Border)</h4>
          <table>
            <tbody>
              <tr>
                <td>X Range:</td>
                <td>[{shape1.x_min.toFixed(1)}, {shape1.x_max.toFixed(1)}]</td>
              </tr>
              <tr>
                <td>Y Range:</td>
                <td>[{shape1.y_min.toFixed(1)}, {shape1.y_max.toFixed(1)}]</td>
              </tr>
              {algorithmType === 'rectangles' ? (
                <>
                  <tr>
                    <td>Width:</td>
                    <td>{shape1.width.toFixed(1)}</td>
                  </tr>
                  <tr>
                    <td>Height:</td>
                    <td>{shape1.height.toFixed(1)}</td>
                  </tr>
                </>
              ) : (
                <tr>
                  <td>Side Length:</td>
                  <td>{shape1.side_length.toFixed(1)}</td>
                </tr>
              )}
            </tbody>
          </table>
        </div>

        <div className="shape-details">
          <h4>{shapeName} 2 (Green Border)</h4>
          <table>
            <tbody>
              <tr>
                <td>X Range:</td>
                <td>[{shape2.x_min.toFixed(1)}, {shape2.x_max.toFixed(1)}]</td>
              </tr>
              <tr>
                <td>Y Range:</td>
                <td>[{shape2.y_min.toFixed(1)}, {shape2.y_max.toFixed(1)}]</td>
              </tr>
              {algorithmType === 'rectangles' ? (
                <>
                  <tr>
                    <td>Width:</td>
                    <td>{shape2.width.toFixed(1)}</td>
                  </tr>
                  <tr>
                    <td>Height:</td>
                    <td>{shape2.height.toFixed(1)}</td>
                  </tr>
                </>
              ) : (
                <tr>
                  <td>Side Length:</td>
                  <td>{shape2.side_length.toFixed(1)}</td>
                </tr>
              )}
            </tbody>
          </table>
        </div>
      </div>

      <div className="complexity-info">
        <h4>Complexity Analysis</h4>
        <p>
          <strong>Red segments (n):</strong> {result.total_red_segments}<br/>
          <strong>Blue segments (m):</strong> {result.total_blue_segments}
        </p>
        {/* {algorithmType === 'rectangles' ? (
          <p className="complexity">
            Time Complexity: <code>O(nm) = O({result.total_red_segments} × {result.total_blue_segments})</code>
          </p>
        ) : (
          <p className="complexity">
            Time Complexity: <code>O(nm log m) = O({result.total_red_segments} × {result.total_blue_segments} × log {result.total_blue_segments})</code>
          </p>
        )} */}
      </div>
    </div>
  );
};

export default Results;