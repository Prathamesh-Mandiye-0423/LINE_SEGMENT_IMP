from flask import Flask, request, jsonify
from flask_cors import CORS
import time
import random
# import algorithms.data_structures as ds
from algorithms.data_structures import LineSegment, Point
from algorithms.rectangles import compute_two_rectangles
from algorithms.squares import compute_two_squares
# print("Testing imports")

app=Flask(__name__)
CORS(app)

def parse_segments(segments_data):
    segments=[]
    for i,seg_data in enumerate(segments_data):
        p1=Point(seg_data['p1']['x'], seg_data['p1']['y'])
        p2=Point(seg_data['p2']['x'], seg_data['p2']['y'])
        color=seg_data.get('color', 'red')
        segments.append(LineSegment(p1, p2,i, color))
    return segments

@app.route('/api/health',methods=['GET'])
def health_check():
    return jsonify(
        {
            "status": "healthy",
            "message": "Line Segment Seperator API is running"

        }
    )

@app.route('/api/compute/rectangles',methods=['POST'])
def compute_rectangles():
    try:
        data=request.get_json()
        if not data:
            return jsonify({'error':'No data provided'}), 400

        red_segments = parse_segments(data.get('red_segments', []))
        blue_segments = parse_segments(data.get('blue_segments', []))

        if len(red_segments)<2:
            return jsonify(
                {
                    'error':'At least 2 red segments are required'
                }
            ),400

        start_time=time.time()

        result = compute_two_rectangles(red_segments, blue_segments)
        execution_time=time.time()-start_time
        result['execution_time_ms'] = round(execution_time * 1000,2)

        if result.get('success'):
            return jsonify(result), 200
        else:
            return jsonify(result), 400

    except Exception as e:
        return jsonify({'error': f' Server Error: {str(e)}'
        }), 500
@app.route('/api/compute/squares',methods=['POST'])
def compute_squares():
    try:
        data=request.get_json()

        if not data:
            return jsonify(
                {
                    'error':'No data provided'
                }), 400

        red_segments=parse_segments(data.get('red_segments',[]))
        blue_segments=parse_segments(data.get('blue_segments',[]))
        use_pst=data.get('use_pst', True)
        if len(red_segments)<2:
            return jsonify(
                {
                    'error':'At least 2 red segments are required'
                }
            ), 400

        start_time=time.time()

        result=compute_two_squares(red_segments, blue_segments, use_pst)
        execution_time=time.time()-start_time
        result['execution_time_ms'] = round(execution_time * 1000,2)

        if result.get('success'):
            return jsonify(result), 200
        else:
            return jsonify(result), 400

    except Exception as e:
        return jsonify(
            {
                'error': f' Server Error: {str(e)}'
        }), 500


@app.route('/api/generate/random', methods=['POST'])
def generate_random_segments():
    try:
        data=request.get_json()
        num_red=data.get('num_red',10)
        num_blue=data.get('num_blue',20)
        width= data.get('width',800)
        height=data.get('height',600)
        max_length=data.get('max_segment_length', 100)

        red_segments=[]
        blue_segments=[]

        for i in range(num_red):
            x1=random.uniform(0,width)
            y1=random.uniform(0,height)
            angle=random.uniform(0, 2*3.14159)
            length=random.uniform(10, max_length)
            x2=x1 + length * random.uniform(0.5,1) * random.choice([-1,1])
            y2=y1 + length * random.uniform(0.5,1) * random.choice([-1,1])
            p1=Point(x1,y1)
            p2=Point(x2,y2)
            red_segments.append(
                {
                    'p1': {'x': p1.x, 'y': p1.y},
                    'p2': {'x': p2.x, 'y': p2.y},
                    'color': 'red'
                }
            )

        for i in range(num_blue):
            x1=random.uniform(0,width)
            y1=random.uniform(0,height)
            angle=random.uniform(0, 2*3.14159)
            length=random.uniform(10, max_length)
            x2=x1 + length * random.uniform(0.5,1) * random.choice([-1,1])
            y2=y1 + length * random.uniform(0.5,1) * random.choice([-1,1])
            p1=Point(x1,y1)
            p2=Point(x2,y2)
            blue_segments.append(
                {
                    'p1': {'x': p1.x, 'y': p1.y},
                    'p2': {'x': p2.x, 'y': p2.y},
                    'color': 'blue'
                }
            )

        return jsonify(
            {
                'red_segments': red_segments,
                'blue_segments': blue_segments
            }), 200

    except Exception as e:
        return jsonify(
            {
                'error': f' Server Error: {str(e)}'
            }), 500


if __name__=='__main__':
    print("Starting Line Segment Separator API...")
    print("API available at http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)
