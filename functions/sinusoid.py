from .function import Function, Combination, Value, Operation
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
    def __init__(self, arg = X, trig_type = TrigType.SIN, eqString=None):
        super().__init__()
        self.trig_type = trig_type
        self.arg = arg
        self._custom_eqString = eqString
    
    def derivative(self):
        if self.trig_type == TrigType.SIN:
            return Combination(
                Sinusoid(self.arg, TrigType.COS, eqString=f"{self._custom_eqString}'"),
                Operation.MULTIPLY,
                self.arg.derivative())
        
        elif self.trig_type == TrigType.COS:
            return Combination(
                Value(-1),
                Operation.MULTIPLY,
                Combination(
                    Sinusoid(self.arg, TrigType.SIN, eqString=f"{self._custom_eqString}'"),
                    Operation.MULTIPLY,
                    self.arg.derivative()
                ))

        elif self.trig_type == TrigType.TAN:
            return Combination(
                Combination(
                    Sinusoid(self.arg, TrigType.SEC, eqString=f"{self._custom_eqString}'"),
                    Operation.POWER,
                    Value(2)
                ),
                Operation.MULTIPLY,
                self.arg.derivative()
            )

        # DO OTHERS LATER
    
    def __str__(self):
        if self._custom_eqString is not None:
            return self._custom_eqString
    
        res = f"{self.trig_type.value}({str(self.arg)})"
        return res
    
    def evaluate(self,x):
        theta = self.arg.evaluate(x)
        
        if self.trig_type == TrigType.SIN:
            return math.sin(theta)
        elif self.trig_type == TrigType.COS:
            return math.cos(theta)
        elif self.trig_type == TrigType.TAN:
            return math.tan(theta)
        elif self.trig_type == TrigType.CSC:
            try:
                return 1/(math.sin(theta))
            except ZeroDivisionError:
                return None
        elif self.trig_type == TrigType.SEC:
            try:
                return 1/(math.cos(theta))
            except ZeroDivisionError:
                return None
        elif self.trig_type == TrigType.COT:
            try:
                return 1/(math.tan(theta))
            except ZeroDivisionError:
                return None