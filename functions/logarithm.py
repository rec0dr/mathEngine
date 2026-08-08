import math
from .function import Function, Combination, Operation, Value
from .function import Variable

X = Variable("x")

class Logarithm(Function):
    def __init__(self, base=Value(math.e), arg=Variable("x"), eqString=None):
        super().__init__()
        self.base, self.arg = base, arg
        if isinstance(self.base, (int, float)):
            self.base = Value(self.base)

        if isinstance(self.arg, (int, float)):
            self.arg = Value(self.arg)

        self._custom_eqString = eqString
    
    def derivative(self):
        # Derivative of log_b(f(x)) = f'(x) / (f(x) * ln(b))
        return Combination(
            self.arg.derivative(),
            Operation.DIVIDE,
            Combination(
                Combination(self.arg, Operation.MULTIPLY, Value(math.log(self.base))),
                Operation.MULTIPLY,
                self
            )
        )
        
    def __str__(self):
        if self._custom_eqString is not None:
            return self._custom_eqString
    
        res = f"log({str(self.base)})({str(self.arg)})"
        
        return res
        
    def evaluate(self, x):
        argument = self.arg.evaluate(x)
        try:
            return math.log(argument, self.base.evaluate(x))
        except ValueError:
            return None
        except TypeError:
            return None