import math
from .function import Function, Combination, Value, Operation
from .function import Variable

X = Variable("x")

class Exponential(Function):
    
    def __init__(self, base=Value(math.e), arg=Variable("x"), eqString=None):
        super().__init__()
        self._custom_eqString = eqString
        
        self.base, self.arg = base, arg
        if isinstance(self.base, (int, float)):
            self.base = Value(self.base)

        if isinstance(self.arg, (int, float)):
            self.arg = Value(self.arg)
    
    def derivative(self):
        return Combination(Combination(math.log(self.base), Operation.MULTIPLY, Combination(self.base, Operation.POWER, self.arg)),
            Operation.MULTIPLY,
            self.arg.derivative())
    
    def __str__(self):
        if self._custom_eqString is not None:
            return self._custom_eqString
        
        res = str(Combination(self.base, Operation.POWER, self.arg))
        return res
    
    def evaluate(self, x):
        return (self.base.evaluate(x) ** self.arg.evaluate(x))