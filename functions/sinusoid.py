from .function import Function
from .function import Variable
from enum import Enum
import math

X = Variable("x")

class TrigType(Enum):
    SIN = "sin"
    COS = "cos"
    TAN = "tan"
    CSC = "csc"
    SEC = "sec"
    COT = "cot"

class Sinusoid(Function):
    def __init__(self, vs = 1, arg = Variable("x"), vt = 0, trig_type = TrigType.SIN, eqString=None):
        self.trig_type = trig_type
        self.amp, self.arg, self.vt = vs, arg, vt
        self._custom_eqString = eqString
    
    def __str__(self):
        if self._custom_eqString is not None:
            return self._custom_eqString
    
        res = ""
        if self.amp == -1:
            res = "-"
        elif self.amp != 1:
            res = res + f"{self.amp}*"
        
        res = res + f"{self.trig_type.value}({str(self.arg)})"
        
        if self.vt != 0:
            if self.vt < 0:
                res = res + f" - {self.vt}"
            else:
                res = res + f" + {self.vt}"
        
        return res
    
    @classmethod
    def from_basic(cls, trig_type, vs=1, vt=0, eqString=None):
        return cls(vs, X, vt, trig_type, eqString)
            
    
    def evaluate(self,x):
        theta = self.arg.evaluate(x)
        
        if self.trig_type == TrigType.SIN:
            return (self.amp * math.sin(theta)) + self.vt
        elif self.trig_type == TrigType.COS:
            return (self.amp * math.cos(theta)) + self.vt
        elif self.trig_type == TrigType.TAN:
            return (self.amp * math.tan(theta)) + self.vt
        elif self.trig_type == TrigType.CSC:
            try:
                return (self.amp * 1/(math.sin(theta))) + self.vt
            except ZeroDivisionError:
                return None
        elif self.trig_type == TrigType.SEC:
            try:
                return (self.amp * 1/(math.cos(theta))) + self.vt
            except ZeroDivisionError:
                return None
        elif self.trig_type == TrigType.COT:
            try:
                return (self.amp * 1/(math.tan(theta))) + self.vt
            except ZeroDivisionError:
                return None