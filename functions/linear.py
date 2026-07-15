import math
from .function import Function

class Linear(Function):
    def __init__(self, a, b, c, eqString=None):
        super().__init__()
        self.a = float(a)
        self.b = float(b)
        self.c = float(c)
        self._custom_eqString = eqString
    
    @classmethod
    def from_standard(cls, a, b, c, eqString=None):
        return cls(a, b, c, eqString)
    
    @classmethod
    def from_slope_intercept(cls, slope, yInt, eqString=None):
        return cls(-slope, 1, yInt, eqString)
    
    @classmethod
    def from_point_slope(cls, x1, y1, slope, eqString=None):
        return cls(-slope,1,y1 - slope*x1, eqString)
    
    @classmethod
    def from_points(cls, x1, y1, x2, y2, eqString=None):
        if x1 == x2:
            return cls(1, 0, x1, eqString)

        slope = (y2 - y1)/(x2 - x1)
        return cls.from_point_slope(x1, y1, slope, eqString)
    
    def __str__(self):
        if self._custom_eqString is not None:
            return self._custom_eqString
        
        slope = -self.a/self.b
        yInt = self.c/self.b
        
        res = ""
        if slope == -1:
            res = res + "-x"
        elif slope == 1:
            res = res + "x"
        elif slope != 0:
            res = res + f"{slope}x"
        
        if yInt != 0:
            if yInt < 0:
                res = res + f" - {yInt}"
            else:
                res = res + f" + {yInt}"
            
        return res
    
    def evaluate(self, x):
        return (self.c/self.b) - (self.a/self.b)*x
    
    def stats(self):
        print(f"Standard: {self.a}x + {self.b}y = {self.c}")
        print(f"eqStringing:", self.eqStringing)