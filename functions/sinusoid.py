"""
Simple class for trig functions.

Allows the user to implement a trig function
of any other function for rendering.

Author: Evan Le
Date: 2026-10-21
License: Personal Use
"""

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