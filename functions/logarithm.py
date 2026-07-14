import math
from .function import Function
from .function import Variable

X = Variable("x")

class Logarithm(Function):
    def __init__(self, base, vs, arg, vt, eqString=None):
        self._data = [base, vs, arg, vt]
        self.base, self.vs, self.arg, self.vt = self._data
        self._custom_eqString = eqString
    
    @classmethod
    def from_basic(cls, base, vs=1, vt=0, eqString=None):
        return cls(base, vs, X, vt, eqString)
        
    def __str__(self):
        if self._custom_eqString is not None:
            return self._custom_eqString
    
        res = ""
        if self.vs == -1:
            res = "-"
        elif self.vs != 1:
            res = res + f"{self.vs}*"
        
        res = res + f"log({self.base})({str(self.arg)})"
        
        if self.vt != 0:
            if self.vt < 0:
                res = res + f" - {self.vt}"
            else:
                res = res + f" + {self.vt}"
        
        return res
        
    def evaluate(self, x):
        argument = self.arg.evaluate(x)
        try:
            return ((self.vs * math.log(argument, self.base)) + self.vt)
        except ValueError:
            return None
        except TypeError:
            return None