from .point import Point
from functions.curve import Curve

class TracedPoint(Point):
    def __init__(self, curve: Curve, parameter: float):
        self.curve = curve
        self.parameter = parameter

    def _update_position(self):
        self.x, self.y = self.curve.point(self.parameter)

    @property
    def parameter(self):
        return self._parameter

    @parameter.setter
    def parameter(self, value):
        self._parameter = value
        self._update_position()

    def moveBy(self, parameter_increment: float):
        self.parameter += parameter_increment

    def moveTo(self, new_parameter: float):
        self.parameter = new_parameter