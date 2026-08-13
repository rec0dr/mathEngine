import math
from .curve import Curve
from .function import Value
from styles.curve_style import CurveStyle
class Parametric(Curve):
    def __init__(self, argX, argY, tMin=-10, tMax=10):
        self.argX, self.argY = argX, argY
        if isinstance(self.argX, (int, float)):
            self.argX = Value(self.argX)
        if isinstance(self.argY, (int, float)):
            self.argY = Value(self.argY)
            
        self.tMin = tMin
        self.tMax = tMax

        super().__init__()

    def __str__(self):
        return f"({str(self.argX)}, {str(self.argY)})"
    
    def evaluate(self, t):
        return (self.argX.evaluate(t), self.argY.evaluate(t))
    
    # For superclass Curve

    def point(self, t):
        return self.evaluate(t)
    
    def parameter_interval(self, renderer):
        return self.tMin, self.tMax

    def inverse(self, tMin=None, tMax=None):

        if tMin is None:
            tMin = self.tMin
        if tMax is None:
            tMax = self.tMax

        return Parametric(self.argY, self.argX, tMin, tMax)