from .point import Point
from functions.curve import Curve

class TracedPoint(Point):
    def __init__(self, curve: Curve, parameter: float):
        self.curve = curve
        self.parameter = parameter
        self.x, self.y = self.curve.point(self.parameter)
    
    def update(self, dt):
        self.x, self.y = self.curve.point(self.parameter)
    
    def moveBy(self, parameter_increment: float):
        self.parameter += parameter_increment
        self.x, self.y = self.curve.point(self.parameter)
    
    def moveTo(self, new_parameter: float):
        self.parameter = new_parameter
        self.x, self.y = self.curve.point(self.parameter)