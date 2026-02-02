# Line Segment Separator - Research Algorithm Implementation

Implementation of algorithms for computing two disjoint axis-parallel rectangles/squares that separate bichromatic line segments, based on the asymmetric separation problem from computational geometry.

## 📚 Research Background

<!-- This project implements algorithms from Section 6.5.3 and 6.5.4 of computational geometry research on asymmetric separation problems for bichromatic point and line segment sets. -->

### Problem Statement

Given:
- **Red line segments (R)**: Must be covered by the separators
- **Blue line segments (B)**: Should be minimized in coverage

Find: Two disjoint axis-parallel rectangles/squares whose union covers all red segments while minimizing the number of blue segments covered.

### Algorithms Implemented

1. **Two Disjoint Rectangles**
   - Time Complexity: **O(nm)**
   - Space Complexity: O(m log m + n)
   - Uses sweep line technique with valid position computation

2. **Two Disjoint Squares (Optimized)**
   - Time Complexity: **O(nm log m)** with Priority Search Trees
   - Time Complexity: **O(nm²)** with naive approach
   - Space Complexity: O(m log m + n)
   - Uses Priority Search Trees for efficient range minimum queries

## 🏗️ Architecture

```
line-segment-separator/
├── backend/           # Python Flask API
│   ├── algorithms/
│   │   ├── data_structures.py    # Geometric data structures
│   │   ├── rectangles.py         # Rectangle algorithm
│   │   └── squares.py            # Square algorithm with PST
│   ├── app.py        # Flask server
│   └── requirements.txt
├── frontend/         # React application
│   ├── src/
│   │   ├── components/
│   │   │   ├── Canvas.jsx        # Drawing interface
│   │   │   ├── Controls.jsx      # Algorithm controls
│   │   │   └── Results.jsx       # Result visualization
│   │   ├── utils/
│   │   │   └── api.js           # API client
│   │   └── App.jsx
│   └── package.json
└── README.md
```

## 🚀 Getting Started

### Prerequisites

- Python 3.8+
- Node.js 16+
- npm or yarn

### Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the server
python app.py
```

Backend will run on `http://localhost:5000`

### Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Run development server
npm run dev
```

Frontend will run on `http://localhost:3000`

## 📖 Usage

### Drawing Segments

1. **Select Color**: Choose "Red" or "Blue" from the controls
2. **Draw**: Click and drag on the canvas to create line segments
3. **Requirements**: Add at least 2 red segments before computing

### Computing Separators

1. **Choose Algorithm**: 
   - Two Rectangles: O(nm) complexity
   - Two Squares: O(nm log m) with PST, O(nm²) naive

2. **Options** (for Squares):
   - Toggle "Use Priority Search Tree" for optimized algorithm

3. **Compute**: Click "Compute Separators" button

4. **View Results**: 
   - Red-bordered shape: First separator
   - Green-bordered shape: Second separator
   - Statistics panel shows execution time and blue coverage

### Additional Features

- **Generate Random**: Create random test data
- **Clear Color**: Remove all segments of selected color
- **Clear All**: Reset the entire canvas

## 🔬 Algorithm Details

### Valid Separator Positions

Both algorithms compute "valid positions" where the sweep line doesn't intersect any red segment's interior:

```python
def compute_valid_y_positions(red_segments):
    # Create events for segment y-intervals
    events = [(y_min, 'START'), (y_max, 'END')]
    # Valid positions are where no segments are "active"
    return positions where active_count == 0
```

### Priority Search Tree (PST)

For the squares algorithm, PST enables O(log m) range minimum queries:

- **Structure**: Binary search tree on x-coordinates with heap on y-coordinates
- **Query**: Find minimum blue_count in range [x_min, ∞) × [y_min, ∞)
- **Usage**: Quickly find optimal disjoint square pairs

### 2D Range Trees

Used for efficient segment counting:

- **Interval-to-Point Transform**: Map segment (x_min, x_max, y_min, y_max) to 2D points
- **Query**: Count segments fully contained in a rectangle
- **Time**: O(log² m) per query

## 📊 Performance

### Complexity Comparison

| Algorithm | Time Complexity | Space Complexity | Best For |
|-----------|----------------|------------------|----------|
| Rectangles | O(nm) | O(m log m + n) | General use |
| Squares (PST) | O(nm log m) | O(m log m + n) | Large m (>100) |
| Squares (Naive) | O(nm²) | O(m + n) | Small m (<50) |

### Measured Performance (Example)

- **n = 10, m = 20**: ~5-10ms
- **n = 50, m = 100**: ~50-100ms
- **n = 100, m = 200**: ~200-500ms

## 🧪 API Endpoints

### POST /api/compute/rectangles
```json
{
  "red_segments": [{"p1": {"x": 0, "y": 0}, "p2": {"x": 1, "y": 1}}],
  "blue_segments": [...]
}
```

### POST /api/compute/squares
```json
{
  "red_segments": [...],
  "blue_segments": [...],
  "use_pst": true
}
```

### POST /api/generate/random
```json
{
  "num_red": 10,
  "num_blue": 20,
  "width": 800,
  "height": 600,
  "max_segment_length": 100
}
```

## 🎓 Research References

This implementation is based on research in computational geometry, specifically:

- **Asymmetric Separation Problems**: Covering one set while minimizing coverage of another
- **Sweep Line Algorithms**: For efficiently processing geometric events
- **Priority Search Trees**: For 3-sided range queries (McCreight, 1985)
- **2D Range Trees**: For orthogonal range searching

## 🐛 Troubleshooting

### Backend won't start
- Ensure Python 3.8+ is installed
- Check if port 5000 is available
- Verify all dependencies are installed

### Frontend won't start
- Ensure Node.js 16+ is installed
- Delete `node_modules` and run `npm install` again
- Check if port 3000 is available

### CORS errors
- Ensure backend is running before frontend
- Check proxy configuration in `vite.config.js`

## 🤝 Contributing

Contributions are welcome! Areas for improvement:

- Additional geometric separators (circles, polygons)
- 3D extension
- Approximation algorithms
- Visualization enhancements
- Performance optimizations

## 📄 License

MIT License - Feel free to use for research and educational purposes.

## 🙏 Acknowledgments

Based on research in asymmetric separation problems for bichromatic geometric objects.