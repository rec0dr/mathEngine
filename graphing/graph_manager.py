from enum import Enum
from functions.curve import Curve
from objects.circle import Circle
from objects.label import Label
from objects.line_segment import LineSegment
from objects.point import Point
from .graph_object import GraphObject

class GraphManager:
    def __init__(self):
        self.graph_objects = {"Curves": [], "Points": [], "Labels": []}
    
    def add(self, *objects: GraphObject):
        for obj in objects:
            # Object layer handling
            if isinstance(obj.drawable, (Curve, Circle, LineSegment)):
                self.graph_objects["Curves"].append(obj)
            elif isinstance(obj.drawable, Point):
                self.graph_objects["Points"].append(obj)
            elif isinstance(obj.drawable, Label):
                self.graph_objects["Labels"].append(obj)
            else:
                raise NotImplementedError("No layer implemented for this object.")
    
    def remove(self, *objects: GraphObject):
        for obj in objects:
            if isinstance(obj.drawable, (Curve, Circle, LineSegment)):
                self.graph_objects["Curves"].remove(obj)
            elif isinstance(obj.drawable, Point):
                self.graph_objects["Points"].remove(obj)
            elif isinstance(obj.drawable, Label):
                self.graph_objects["Labels"].remove(obj)
            else:
                raise NotImplementedError("No layer implemented for this object.")
    
    def clear(self):
        for key in self.graph_objects:
            self.graph_objects[key] = []

    def __len__(self):
        res = 0
        for key in self.graph_objects:
            res += len(self.graph_objects[key])
        return res
    
    def __getitem__(self, index):
        return self.graph_objects[index]
            



