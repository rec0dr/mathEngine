import math
from .curve import Curve
from .function import Value
from objects.point import Point
from styles.curve_style import CurveStyle
class Parametric(Curve):
    def __init__(self, argX, argY, tMin=-10, tMax=10):
        self.argX, self.argY = argX, argY
        if isinstance(self.argX, (int, float)):
            self.argX = Value(self.argX)
        if isinstance(self.argY, (int, float)):
            self.argY = Value(self.argY)
            
        self.tMin, self.tMax = tMin, tMax
        if isinstance(self.tMin, (int, float)):
            self.tMin = Value(self.tMin)
        if isinstance(self.tMax, (int, float)):
            self.tMax = Value(self.tMax)

        super().__init__()

    def __str__(self):
        return f"({str(self.argX)}, {str(self.argY)})"

    def __add__(self, other):
        if isinstance(other, Parametric):
            return Parametric(self.argX+other.argX, self.argY+other.argY, self.tMin, self.tMax)
        elif isinstance(other, Point):
            return Parametric(self.argX+other._x, self.argY+other._y, self.tMin, self.tMax)
        else:
            raise TypeError

    def __radd__(self, other):
        if isinstance(other, Parametric):
            return Parametric(self.argX+other.argX, self.argY+other.argY, other.tMin, other.tMax)
        elif isinstance(other, Point):
            return Parametric(self.argX+other._x, self.argY+other._y, self.tMin, self.tMax)
        else:
            raise TypeError

    def __sub__(self, other):
        if isinstance(other, Parametric):
            return Parametric(self.argX-other.argX, self.argY-other.argY, self.tMin, self.tMax)
        elif isinstance(other, Point):
            return Parametric(self.argX-other._x, self.argY-other._y, self.tMin, self.tMax)
        else:
            raise TypeError

    def __rsub__(self, other):
        if isinstance(other, Parametric):
            return Parametric(other.argX-self.argX, other.argY-self.argY, other.tMin, other.tMax)
        elif isinstance(other, Point):
            return Parametric(other._x-self.argX, other._y-self.argY, self.tMin, self.tMax)
        else:
            raise TypeError

    def __mul__(self, other):
        if isinstance(other, (float, int)):
            other = Value(other)

        if isinstance(other, Value):
            return Parametric(self.argX*other, self.argY*other, self.tMin, self.tMax)
        else:
            raise TypeError

    def __rmul__(self, other):
        if isinstance(other, (float, int)):
            other = Value(other)

        if isinstance(other, Value):
            return Parametric(self.argX*other, self.argY*other, self.tMin, self.tMax)
        else:
            raise TypeError

    def __truediv__(self, other):
        if isinstance(other, (float, int)):
            other = Value(other)

        if isinstance(other, Value):
            return Parametric(self.argX/other, self.argY/other, self.tMin, self.tMax)
        else:
            raise TypeError

    def __rtruediv__(self, other):
        if isinstance(other, (float, int)):
            other = Value(other)

        if isinstance(other, Value):
            return Parametric(other.value/self.argX, other.value/self.argY, self.tMin, self.tMax)
        else:
            raise TypeError


    
    def evaluate(self, t):
        return (self.argX.evaluate(t), self.argY.evaluate(t))
    
    # For superclass Curve

    def point(self, t):
        return self.evaluate(t)

    def parameter_interval(self, renderer):
        return (self.tMin.evaluate(), self.tMax.evaluate())

    def inverse(self, tMin=None, tMax=None):

        if tMin is None:
            tMin = self.tMin
        if tMax is None:
            tMax = self.tMax

        return Parametric(self.argY, self.argX, tMin, tMax)