from functions.function import Function, Value

from .point import Point
from functions.curve import Curve

class TracedPoint(Point):
    def __init__(self, curve: Curve, parameter):
        self.curve = curve
        self._parameter = parameter

    @property
    def parameter(self):
        if isinstance(self._parameter, Function):
            return self._parameter.evaluate(0)
        return self._parameter

    @parameter.setter
    def parameter(self, value):
        self._parameter = value

    @property
    def _x(self):
        return Value(self.curve.point(self.parameter)[0])

    @property
    def _y(self):
        return Value(self.curve.point(self.parameter)[1])

    def moveBy(self, parameter_increment: float):
        self.parameter += parameter_increment

    def moveTo(self, new_parameter: float):
        self.parameter = new_parameter