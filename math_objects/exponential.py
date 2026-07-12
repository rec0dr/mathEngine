import math
from .function import Function
from .symbols import X

class Exponential(Function):
    
    def __init__(self, base, vs, arg, vt, eqString=None):
        self._data = [base, vs, arg, vt]
        self._custom_eqString = eqString
        
        self.base, self.vs, self.arg, self.vt = self._data
        
    @classmethod
    def from_basic(cls, base, vs=1, vt=0, eqString=None):
        return cls(base, vs, X, vt, eqString)
    
    def __str__(self):
        if self._custom_eqString is not None:
            return self._custom_eqString
        
        res = ""
        if self.vs == 0:
            return f"{self.vt}"
        elif self.vs == 1:
            res = res + f"({self.base})^"
        elif self.vs == -1:
            res = res + f"-({self.base})^"
        else:
            res = res + f"{self.vs}({self.base})^"
        
        res = res + f"({str(self.arg)[4:]})"
        
        if self.vt != 0:
            if self.vt > 0:
                res = res + f" + {self.vt}"
            else:
                res = res + f" - {self.vt}"
        return res
    
    def evaluate(self, x):
        return (self.vs * (self.base**self.arg.evaluate(x)) + self.vt)