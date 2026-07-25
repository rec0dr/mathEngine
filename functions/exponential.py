import math
from .function import Function
from .function import Variable

X = Variable("x")

class Exponential(Function):
    
    def __init__(self, base, arg, eqString=None):
        super().__init__()
        self._custom_eqString = eqString
        
        self.base, self.arg = base, arg
    
    def __str__(self):
        if self._custom_eqString is not None:
            return self._custom_eqString
        
        res = f"({self.base}) ^ ({self.arg})"
        return res
    
    def evaluate(self, x):
        return (self.base ** self.arg.evaluate(x))