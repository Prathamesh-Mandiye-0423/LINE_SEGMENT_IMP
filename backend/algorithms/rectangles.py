# Time complexity of O(nm)

from typing import List, Tuple, Optional
from algorithms.data_structures import(
    LineSegment,
    Rectangle,
    Point, RangeTree2D, count_segments_in_rectangle
)
# When making relative imports no need to use leading dots
# print("Testing relative imports")

def compute_valid_y_positions(red_segments: List[LineSegment])->float:
    events=[]
    for seg in red_segments:
        y_min=seg.y_min()
        y_max=seg.y_max()
        events.append((y_min, 1))
        events.append((y_max, -1))
    events.sort(key=lambda e:e[0])
    active_segments=0
    valid_y_pos=[]
    prev_y=None
    for y,event_type in events:
        if active_segments==0 and prev_y!=y:
            valid_y_pos.append((y))

        if event_type=="START":
            # try with number instead
            active_segments+=1
        elif event_type=="END":
            active_segments-=1
        prev_y=y
    # return valid_y_pos
    if active_segments==0 and events:
        valid_y_pos.append((events[-1][0]))
    return sorted(set(valid_y_pos))

def compute_valid_x_positions(red_segments: List[LineSegment])->List[float]:
    events=[]
    for seg in red_segments:
        x_min=seg.x_min()
        x_max=seg.x_max()
        events.append((x_min, 1))
        events.append((x_max, -1))
    events.sort(key=lambda e:e[0])
    active_segments=0
    valid_x_pos=[]
    prev_x=None
    for x,event_type in events:
        if active_segments==0 and prev_x!=x:
            valid_x_pos.append((x))

        if event_type=="START":
            # try with number instead
            active_segments+=1
        elif event_type=="END":
            active_segments-=1
        prev_x=x
    # return valid_x_pos
    if active_segments==0 and events:
        valid_x_pos.append((events[-1][0]))
    return sorted(set(valid_x_pos))


def compute_bounding_rectangle(segments: List[LineSegment])->Optional[Rectangle]:
    if not segments:
        return None
    
    endpoints=[]
    for seg in segments:
        endpoints.extend(seg.endpoints())

    if not endpoints:
        return None

    x_coords = [p.x for p in endpoints]
    y_coords = [p.y for p in endpoints]

    return Rectangle(
        min(x_coords),
        min(y_coords),
        max(x_coords),
        max(y_coords)
    )

#Returns (R1,R2,blue_count)
def horizontal_sweep(red_segments: List[LineSegment],
                     blue_segments: List[LineSegment],
                     valid_y_positions: List[float]) ->Tuple[Rectangle,Rectangle, int]:
    min_blue_count=float('inf')
    best_r1=None
    best_r2=None
    for y in valid_y_positions:
        Q1=[seg for seg in red_segments if seg.y_max()<=y]
        Q2=[seg for seg in red_segments if seg.y_min()>=y]
        if not Q1 or not Q2:
            continue
        R1=compute_bounding_rectangle(Q1)
        R2=compute_bounding_rectangle(Q2)

        if R1 is None or R2 is None:
            continue
    
        if not R1.disjointCheck(R2):
            continue

        blue_count_r1=count_segments_in_rectangle(blue_segments,R1)
        blue_count_r2=count_segments_in_rectangle(blue_segments,R2)
        total_blue=blue_count_r1+blue_count_r2

        if total_blue<min_blue_count:
            min_blue_count=total_blue
            best_r1=R1
            best_r2=R2
    return best_r1,best_r2,min_blue_count


def vertical_sweep(red_segments: List[LineSegment],
                    blue_segments: List[LineSegment],
                    valid_x_positions: List[float]) ->Tuple[Rectangle,Rectangle, int]:
    min_blue_count=float('inf')
    best_r1=None
    best_r2=None
    for x in valid_x_positions:
        Q1=[seg for seg in red_segments if seg.x_max()<=x]
        Q2=[seg for seg in red_segments if seg.x_min()>=x]
        if not Q1 or not Q2:
            continue
        R1=compute_bounding_rectangle(Q1)
        R2=compute_bounding_rectangle(Q2)

        if R1 is None or R2 is None:
            continue

        if not R1.disjointCheck(R2):
            continue

        blue_count_r1=count_segments_in_rectangle(blue_segments,R1)
        blue_count_r2=count_segments_in_rectangle(blue_segments,R2)
        total_blue=blue_count_r1+blue_count_r2

        if total_blue<min_blue_count:
            min_blue_count=total_blue
            best_r1=R1
            best_r2=R2
    return best_r1,best_r2,min_blue_count

def compute_two_rectangles(red_segments: List[LineSegment],
                           blue_segments: List[LineSegment]) ->dict:
    if(len(red_segments)<2):
        return {
            'success': False,
            'error': 'Need at least 2 red segments'
        }
    valid_y=compute_valid_y_positions(red_segments)
    valid_x=compute_valid_x_positions(red_segments)

    if not valid_y or not valid_x:
        return {
            'success': False,
            'error': 'No valid positions found'
        }

    #Horizontal sweep first
    r1_h,r2_h,blue_h=None, None, float('inf')
    if valid_y:
        r1_h, r2_h, blue_h=horizontal_sweep(red_segments,blue_segments,valid_y)

    r1_v,r2_v,blue_v=None, None, float('inf')
    if valid_x:
        r1_v, r2_v, blue_v=vertical_sweep(red_segments,blue_segments,valid_x)

    if blue_h<=blue_v and r1_h is not None:
       return {
        'success':True,
        'rectangle1':r1_h.to_dict(),
        'rectangle2':r2_h.to_dict(),
        'blue_count': int(blue_h),
        'seperator_type':'horizontal',
        'total_red_segments': len(red_segments),
        'total_blue_segments': len(blue_segments)
       }
    elif r1_v is not None:
        return{
            'success':True,
            'rectangle1': r1_v.to_dict(),
            'rectangle2': r2_v.to_dict(),
            'blue_count': int(blue_v),
            'seperator_type':'vertical',
            'total_red_segments': len(red_segments),
            'total_blue_segments': len(blue_segments)
        }
    else:
        return {
            'success':False,
            'error':'No valid rectangles found'
        }

# print("Checking imports and syntax")
