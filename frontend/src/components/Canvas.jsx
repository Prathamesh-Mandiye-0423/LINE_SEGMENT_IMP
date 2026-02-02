import React, { useRef, useEffect, useState } from 'react';
import './Canvas.css';

const Canvas = ({ 
  redSegments, 
  blueSegments, 
  onAddSegment, 
  currentColor,
  result,
  algorithmType 
}) => {
  const canvasRef = useRef(null);
  const [drawing, setDrawing] = useState(false);
  const [startPoint, setStartPoint] = useState(null);
  const [currentPoint, setCurrentPoint] = useState(null);

  const CANVAS_WIDTH = 800;
  const CANVAS_HEIGHT = 600;

  useEffect(() => {
    drawCanvas();
  }, [redSegments, blueSegments, currentPoint, result]);

  const drawCanvas = () => {
    const canvas = canvasRef.current;
    if (!canvas) return;

    const ctx = canvas.getContext('2d');
    
    // Clear canvas
    ctx.fillStyle = '#f8f9fa';
    ctx.fillRect(0, 0, CANVAS_WIDTH, CANVAS_HEIGHT);
    
    // Draw grid
    ctx.strokeStyle = '#e0e0e0';
    ctx.lineWidth = 1;
    for (let x = 0; x <= CANVAS_WIDTH; x += 50) {
      ctx.beginPath();
      ctx.moveTo(x, 0);
      ctx.lineTo(x, CANVAS_HEIGHT);
      ctx.stroke();
    }
    for (let y = 0; y <= CANVAS_HEIGHT; y += 50) {
      ctx.beginPath();
      ctx.moveTo(0, y);
      ctx.lineTo(CANVAS_WIDTH, y);
      ctx.stroke();
    }

    // Draw result shapes first (so segments appear on top)
    if (result && result.success) {
      drawResultShapes(ctx, result);
    }

    // Draw segments
    [...redSegments, ...blueSegments].forEach(segment => {
      drawSegment(ctx, segment);
    });

    // Draw current drawing segment
    if (drawing && startPoint && currentPoint) {
      ctx.strokeStyle = currentColor === 'red' ? '#ff4444' : '#4444ff';
      ctx.lineWidth = 3;
      ctx.setLineDash([5, 5]);
      ctx.beginPath();
      ctx.moveTo(startPoint.x, startPoint.y);
      ctx.lineTo(currentPoint.x, currentPoint.y);
      ctx.stroke();
      ctx.setLineDash([]);
      
      // Draw endpoints
      ctx.fillStyle = currentColor === 'red' ? '#ff4444' : '#4444ff';
      ctx.beginPath();
      ctx.arc(startPoint.x, startPoint.y, 5, 0, 2 * Math.PI);
      ctx.fill();
      ctx.beginPath();
      ctx.arc(currentPoint.x, currentPoint.y, 5, 0, 2 * Math.PI);
      ctx.fill();
    }
  };

  const drawSegment = (ctx, segment) => {
    const color = segment.color === 'red' ? '#ff4444' : '#4444ff';
    
    // Draw line
    ctx.strokeStyle = color;
    ctx.lineWidth = 3;
    ctx.beginPath();
    ctx.moveTo(segment.p1.x, segment.p1.y);
    ctx.lineTo(segment.p2.x, segment.p2.y);
    ctx.stroke();

    // Draw endpoints
    ctx.fillStyle = color;
    ctx.beginPath();
    ctx.arc(segment.p1.x, segment.p1.y, 4, 0, 2 * Math.PI);
    ctx.fill();
    ctx.beginPath();
    ctx.arc(segment.p2.x, segment.p2.y, 4, 0, 2 * Math.PI);
    ctx.fill();
  };

  const drawResultShapes = (ctx, result) => {
    if (algorithmType === 'rectangles') {
      drawRectangle(ctx, result.rectangle1, '#ff000033', '#ff0000');
      drawRectangle(ctx, result.rectangle2, '#00ff0033', '#00ff00');
    } else {
      drawSquare(ctx, result.square1, '#ff000033', '#ff0000');
      drawSquare(ctx, result.square2, '#00ff0033', '#00ff00');
    }
  };

  const drawRectangle = (ctx, rect, fillColor, strokeColor) => {
    if (!rect) return;
    
    const { x_min, y_min, x_max, y_max } = rect;
    const width = x_max - x_min;
    const height = y_max - y_min;

    // Fill
    ctx.fillStyle = fillColor;
    ctx.fillRect(x_min, y_min, width, height);

    // Stroke
    ctx.strokeStyle = strokeColor;
    ctx.lineWidth = 2;
    ctx.strokeRect(x_min, y_min, width, height);

    // Label
    ctx.fillStyle = strokeColor;
    ctx.font = 'bold 14px Arial';
    ctx.fillText('R', x_min + 5, y_min + 20);
  };

  const drawSquare = (ctx, square, fillColor, strokeColor) => {
    if (!square) return;
    
    const { x_min, y_min, side_length } = square;

    // Fill
    ctx.fillStyle = fillColor;
    ctx.fillRect(x_min, y_min, side_length, side_length);

    // Stroke
    ctx.strokeStyle = strokeColor;
    ctx.lineWidth = 2;
    ctx.strokeRect(x_min, y_min, side_length, side_length);

    // Label
    ctx.fillStyle = strokeColor;
    ctx.font = 'bold 14px Arial';
    ctx.fillText('S', x_min + 5, y_min + 20);
  };

  const getCanvasCoordinates = (e) => {
    const canvas = canvasRef.current;
    const rect = canvas.getBoundingClientRect();
    return {
      x: e.clientX - rect.left,
      y: e.clientY - rect.top
    };
  };

  const handleMouseDown = (e) => {
    const point = getCanvasCoordinates(e);
    setDrawing(true);
    setStartPoint(point);
    setCurrentPoint(point);
  };

  const handleMouseMove = (e) => {
    if (!drawing) return;
    const point = getCanvasCoordinates(e);
    setCurrentPoint(point);
  };

  const handleMouseUp = (e) => {
    if (!drawing || !startPoint) return;

    const endPoint = getCanvasCoordinates(e);
    
    // Only add if segment has some length
    const dx = endPoint.x - startPoint.x;
    const dy = endPoint.y - startPoint.y;
    const length = Math.sqrt(dx * dx + dy * dy);
    
    if (length > 5) {
      onAddSegment({
        p1: { x: startPoint.x, y: startPoint.y },
        p2: { x: endPoint.x, y: endPoint.y }
      });
    }

    setDrawing(false);
    setStartPoint(null);
    setCurrentPoint(null);
  };

  const handleMouseLeave = () => {
    setDrawing(false);
    setStartPoint(null);
    setCurrentPoint(null);
  };

  return (
    <div className="canvas-container">
      <div className="canvas-info">
        <span>Drawing: <strong>{currentColor.toUpperCase()}</strong> segments</span>
        <span>Click and drag to draw a segment</span>
      </div>
      <canvas
        ref={canvasRef}
        width={CANVAS_WIDTH}
        height={CANVAS_HEIGHT}
        onMouseDown={handleMouseDown}
        onMouseMove={handleMouseMove}
        onMouseUp={handleMouseUp}
        onMouseLeave={handleMouseLeave}
        className="drawing-canvas"
      />
    </div>
  );
};

export default Canvas;