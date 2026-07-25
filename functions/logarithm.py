import math
from .function import Function
from .function import Variable

X = Variable("x")

class Logarithm(Function):
    def __init__(self, base=math.e, arg=Variable("x"), eqString=None):
        super().__init__()
        self.base, self.arg = base, arg
        self._custom_eqString = eqString
        
    def __str__(self):
        if self._custom_eqString is not None:
            return self._custom_eqString
    
        res = f"log({self.base})({str(self.arg)})"
        
        return res
        
    def evaluate(self, x):
        argument = self.arg.evaluate(x)
        try:
            return math.log(argument, self.base)
        except ValueError:
            return None
        except TypeError:
            return None