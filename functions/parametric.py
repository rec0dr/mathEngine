import math
from .function import Function
from .function import Variable
class Parametric:
    def __init__(self, argX=Variable("x"), argY=Variable("x"), eqString=None, tMin=-10, tMax=10):
        self._data = [argX, argY]
        self.argX, self.argY = self._data
        self._custom_eqString = eqString
        self.tMin = tMin
        self.tMax = tMax
    
    def __str__(self):
        if self._custom_eqString is not None:
            return self._custom_eqString
        else:
            return f"({str(self.argX)}, {str(self.argY)})"
    
    def evaluate(self, t):
        return [self.argX.evaluate(t), self.argY.evaluate(t)]