import bisect
from typing import List, Tuple, Optional
from dataclasses import dataclass


@dataclass
class Point:
    x: float
    y: float
    def __iter__(self):
        return iter((self.x,self.y))
    def __repr__(self):
        return f"Point({self.x}, {self.y})"


@dataclass
class LineSegment:
    start: Point
    end: Point
    segment_id: int
    color: str 

    def x_min(self):
        return min(self.start.x,self.end.x)

    def y_min(self):
        return min(self.start.y,self.end.y)

    def x_max(self):
        return max(self.start.x,self.end.x)

    def y_max(self):
        return max(self.start.y,self.end.y)

    def endpoints(self):
        return [self.start,self.end]


@dataclass
class Rectangle:
    x_min: float
    y_min: float
    x_max: float
    y_max: float

    def contains_point(self,p: Point) -> bool:
        return ((self.x_min <= p.x <= self.x_max) and (self.y_min <= p.y <= self.y_max))

    def contains_segment(self,seg:LineSegment)->bool:
        return (self.contains_point(seg.start) 
        and self.contains_point(seg.end))

    def disjointCheck(self, other: 'Rectangle') -> bool:
        return (self.x_max < other.x_min or self.x_min > other.x_max or
                self.y_max < other.y_min or self.y_min > other.y_max)
    
    def to_dict(self):
        return {
            'x_min': self.x_min,
            'y_min': self.y_min,
            'x_max': self.x_max,
            'y_max': self.y_max,
            'width': self.x_max - self.x_min,
            'height': self.y_max - self.y_min
        }

@dataclass
class Square:
    x_min: float
    y_min: float
    side_length: float
    blue_count:int=0

    @property
    def x_max(self):   
        return self.x_min + self.side_length
    @property
    def y_max(self):
        return self.y_min + self.side_length

    def contains_point(self,p: Point) -> bool:
        return ((self.x_min <= p.x <= self.x_max) 
        and (self.y_min <= p.y <= self.y_max))

    def contains_segment(self,seg:LineSegment)->bool:
        return (self.contains_point(seg.start) 
        and self.contains_point(seg.end))

    def disjointCheck(self, other: 'Square') -> bool:
        return (self.x_max < other.x_min or self.x_min > other.x_max or
                self.y_max < other.y_min or self.y_min > other.y_max)

    def to_dict(self):
        return{
            'x_min':self.x_min,
            'y_min':self.y_min,
            'x_max':self.x_max,
            'y_max':self.y_max,
            'side_length':self.side_length,
            'blue_count':self.blue_count
        }

class RangeTree2D:
    def __init__(self,points: List[Tuple[float,float,int]]):
        self.points=sorted(points, key=lambda p:(p[0],p[1]))
        self.root= self._build_tree(self.points, depth=0)

    def _build_tree(self,points):
        if not points:
            return None
        if len(points)==1:
            return{
                'point': points[0],
                'left': None,
                'right': None,
                'y_tree':sorted([points[0][1]], key=lambda y:y),
                'segment_ids': [points[0][2]]
            }
        mid = len(points)//2
        node = {
            'point': points[mid],
            'left': self._build_tree(points[:mid]),
            'right': self._build_tree(points[mid+1:]),
            'y_tree': sorted([p[1] for p in points], key=lambda y:y),
            'segment_ids': [p[2] for p in points]
        }
        return node

    def query(self,x_min:float, x_max:float, y_min: float, y_max:float)->List[int]:
        result=[]
        self._query_help(self.root, x_min, x_max, y_min, y_max, result)
        return result

    def _query_help(self, node, x_min, x_max, y_min, y_max, result):
        if not node:
            return
        if (x_min <= node['point'][0] <= x_max and
            y_min <= node['point'][1] <= y_max):
            result.append(node['point'][2])
        if node['left'] and x_min <= node['left']['point'][0] <= x_max:
            self._query_help(node['left'], x_min, x_max, y_min, y_max, result)
        if node['right'] and x_min <= node['right']['point'][0] <= x_max:
            self._query_help(node['right'], x_min, x_max, y_min, y_max, result)

class PrioritySearchTree:
    def __init__(self,points: List[Tuple[float,float,int]]):
        self.points=sorted(points,key=lambda p: (p[1],p[0]))
        self.root=self._build_tree(list(range(len(self.points))))

    def _build_tree(self,indices:List[int]):
        if not indices:
            return None
        
        if len(indices)==1:
            idx=indices[0]
            x,y,value=self.points[idx]
            return{
                'x':x,
                'y':y,
                'value':value,
                'min_value': value,
                'left': None,
                'right': None
            }
        min_yidx=indices[0]
        x_min,y_min,value_min=self.points[min_yidx]
        remaining=indices[1:]

        x_coords=[self.points[i][0] for i in remaining]
        if not x_coords:
            return {
                'x':x_min,
                'y':y_min,
                'value':value_min,
                'min_value': value_min,
                'left': None,
                'right': None
            }
        x_mid=sorted(x_coords)[len(x_coords)//2]

        left_idxs=[i for i in remaining if self.points[i][0]<=x_mid]
        right_idxs=[i for i in remaining if self.points[i][0]>x_mid]

        left_child=self._build_tree(left_idxs)
        right_child=self._build_tree(right_idxs)

        min_val=value_min
        if left_child:
            min_val=min(min_val,left_child['min_value'])
        if right_child:
            min_val=min(min_val,right_child['min_value'])

        return {
            'x':x_min,
            'y':y_min,
            'value':value_min,
            'min_value': min_val,
            'left': left_child,
            'right': right_child
        }

    def minquery(self,x_min:float,y_min:float)->Optional[Tuple[float,float,float]]:
       return self._range_min_helper(self.root,x_min,y_min)

    def _range_min_helper(self,node,x_min,y_min):
        if node is None:
            return None
        curr_minm=None
        if node['x']>=x_min and node['y']>=y_min:
            curr_minm=(node['x'],node['y'],node['value'])

        if node['left'] and x_min<=node['x']:
            left_res=self._range_min_helper(node['left'],x_min,y_min)
            if left_res:
                if curr_minm is None or left_res[2]<curr_minm[2]:
                    curr_minm=left_res
        if node['right'] and x_min<=node['x']:
            right_res=self._range_min_helper(node['right'],x_min,y_min)
            if right_res:
                if curr_minm is None or right_res[2]<curr_minm[2]:
                    curr_minm=right_res
        return curr_minm

def count_segments_in_rectangle(segments: List[LineSegment],rect: Rectangle)->int:
    count=0
    for seg in segments:
        if rect.contains_segment(seg):
            count+=1
    return count

def count_segments_in_square(segments: List[LineSegment],square: Square)->int:
    count=0
    for seg in segments:
        if square.contains_segment(seg):
            count+=1
    return count