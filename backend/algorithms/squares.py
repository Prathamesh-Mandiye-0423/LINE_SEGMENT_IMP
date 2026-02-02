#Compute disjoint squares using Prioirty Search Trees
# Time Complexity: O(nmlogm)

from typing import List, Tuple, Optional
from algorithms.data_structures import(
    LineSegment, Square, Point,
    PrioritySearchTree, count_segments_in_square
)

from algorithms.rectangles import (
    compute_valid_x_positions,
    compute_valid_y_positions
)

# print("Checking relative imports")

def candidate_squares(segments: List[LineSegment],
                    blue_segments: List[LineSegment]
                    )->List[Square]:
    if not segments:
        return []
    endpoints=[]
    for seg in segments:
        endpoints.extend(seg.endpoints())
    
    if not endpoints:
        return []

    x_coords= [p.x for p in endpoints]
    y_coords= [p.y for p in endpoints]

    x_min=min(x_coords)
    x_max=max(x_coords)
    y_min=min(y_coords) 
    y_max=max(y_coords)

    width=x_max-x_min
    height=y_max-y_min
    side_length= max(width,height)
    candidates=[]

    if width>height:
        fixed_x_min=x_min
        blue_y_coords=set()

        for seg in blue_segments:
            for p in seg.endpoints():
                if fixed_x_min<=p.x<=fixed_x_min+side_length:
                    blue_y_coords.add(p.y)

        blue_y_coords.add(y_min)
        blue_y_coords.add(y_min-(side_length-height))

        for y_bottom in sorted(blue_y_coords):
            if y_bottom<=y_min and y_bottom+side_length>=y_max:
                square= Square(fixed_x_min,y_bottom,side_length)
                blue_count = count_segments_in_square(blue_segments,square)
                square.blue_count= blue_count
                candidates.append(square)
    elif width<height:
        fixed_y_min=y_min
        blue_x_coords=set()

        for seg in blue_segments:
            for p in seg.endpoints():
                if fixed_y_min<=p.y<=fixed_y_min+side_length:
                    blue_x_coords.add(p.x)

        blue_x_coords.add(x_min)
        blue_x_coords.add(x_min-(side_length-width))

        for x_left in sorted(blue_x_coords):
            if x_left<=x_min and x_left+side_length>=x_max:
                square= Square(x_left,fixed_y_min,side_length)
                blue_count = count_segments_in_square(blue_segments,square)
                square.blue_count= blue_count
                candidates.append(square)
            else:
                square= Square(x_min, y_min, side_length)
                blue_count = count_segments_in_square(blue_segments,square)
                square.blue_count=blue_count
                candidates.append(square)
    if not candidates:
        square = Square(x_min, y_min, side_length)
        blue_count = count_segments_in_square(blue_segments, square)
        square.blue_count = blue_count
        candidates.append(square)
    unique_candidates=[]
    visited=set()
    for s in candidates:
        key= (round(s.x_min,6),round(s.y_min,6),round(s.side_length,6))
        if key not in visited:
            visited.add(key)
            unique_candidates.append(s)
    return unique_candidates[:100]

def find_optimal_disjoint_pair(A1: List[Square],
                                A2: List[Square])-> Tuple[Optional[Square], Optional[Square], int]:
    if not A1 or not A2:
        return None, None, float('inf')

    pst_points=[(s.x_min,s.y_min,s.blue_count) for s in A2]
    pst= PrioritySearchTree(pst_points)
    min_total=float('inf')
    best_s1=None
    best_s2=None

    for s1 in A1:
        result=pst.minquery(s1.x_max,s1.y_max)
        if result:
            s2_x,s2_y,s2_blue_count=result
            matching_s2=None
            for s in A2:
                if (abs(s.x_min-s2_x)<1e-9 and
                abs(s.y_min-s2_y)<1e-9 and s.blue_count==s2_blue_count):
                    matching_s2=s
                    break
            if matching_s2 and s1.disjointCheck(matching_s2):
                total=s1.blue_count + matching_s2.blue_count
                if total<min_total:
                    min_total=total
                    best_s1=s1
                    best_s2=matching_s2

    return best_s1,best_s2,min_total
def horizontal_sweep_squares(red_segment: List[LineSegment], blue_segments: List[LineSegment], valid_y_positions: List[float],use_pst: bool = True) -> Tuple[Square, Square, int]:
    min_blue_count= float('inf')
    best_s1=None
    best_s2=None
    for y_pos in valid_y_positions:
        Q1=[seg for seg in red_segment if seg.y_max()<=y_pos]
        Q2=[seg for seg in red_segment if seg.y_min()>=y_pos]
        if not Q1 or not Q2:
            continue
        A1=candidate_squares(Q1,blue_segments)
        A2=candidate_squares(Q2,blue_segments)

        if not A1 or not A2:
            continue

        s1, s2, total = find_optimal_disjoint_pair(A1, A2)
        if s1 and s2 and min_blue_count>total:
            min_blue_count=total
            best_s1=s1
            best_s2=s2
    return best_s1, best_s2, min_blue_count

def vertical_sweep_squares(red_segments: List[LineSegment], blue_segments:List[LineSegment],
                           valid_x_positions: List[float],use_pst: bool= True )->Tuple[Square,Square,int]:
    min_blue_count= float('inf')
    best_s1=None
    best_s2= None
    for x_pos in valid_x_positions:
        Q1=[seg for seg in red_segments if seg.x_max()<=x_pos]
        Q2=[seg for seg in red_segments if seg.x_min()>=x_pos]
        if not Q1 or not Q2:
            continue
        
        A1=candidate_squares(Q1,blue_segments)
        A2=candidate_squares(Q2,blue_segments)
        if not A1 or not A2:
            continue

        s1,s2,total=find_optimal_disjoint_pair(A1,A2)

        if s1 and s2 and min_blue_count>total:
            min_blue_count=total
            best_s1=s1
            best_s2=s2

    return best_s1, best_s2, min_blue_count

def compute_two_squares(red_segments: List[LineSegment],
                        blue_segments: List[LineSegment],
                        use_pst: bool = True)-> dict:
    if len(red_segments)<2:
        return{
            'success': False,
            'error': 'Need at least 2 red segments'
        }
    valid_y=compute_valid_y_positions(red_segments)
    valid_x=compute_valid_x_positions(red_segments)

    if not valid_x and not valid_y:
        return{
            'success': False,
            'error': 'No valid positions found'
        }
    
    s1_h,s2_h,blue_h= None, None, float('inf')
    if valid_y:
        s1_h,s2_h,blue_h= horizontal_sweep_squares(red_segments,blue_segments,valid_y,use_pst)
    s1_v,s2_v, blue_v = None, None, float('inf')
    if valid_x:
        s1_v,s2_v,blue_v= vertical_sweep_squares(red_segments,blue_segments,valid_x,use_pst)
    if blue_h<=blue_v and s1_h is not None:
        return {
            'success': True,
            'square1':s1_h.to_dict(),
            'square2':s2_h.to_dict(),
            'blue_count': int(blue_h),
            'seperator_type': 'horizontal',
            'algorithm':'PST',
            'total_red_segments': len(red_segments),
            'total_blue_segments': len(blue_segments)
        }
    elif s1_v is not None:
        return {
            'success': True,
            'square1': s1_v.to_dict(),
            'square2': s2_v.to_dict(),
            'blue_count': int(blue_v),
            'seperator_type': 'vertical',
            'algorithm': 'PST',
            'total_red_segments': len(red_segments),
            'total_blue_segments': len(blue_segments)
        }
    else:
        return {
            'success': False,
            'error': 'Could not find valid disjoint squares'
        }