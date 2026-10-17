import math
from enum import Enum
from .curve import Curve
from styles.curve_style import CurveStyle

class Operation(Enum):
    ADD         = "+"
    SUBTRACT    = "-"
    MULTIPLY    = "*"
    DIVIDE      = "/"
    POWER       = "^"
    ABS         = "|"

# Function combination logic

class Function(Curve):

    def __init__(self):
        super().__init__()

    # Function combo logic
    
    def __add__(self, other):
        if isinstance(other, (int, float)):
            other = Value(other)
        return Combination(self, Operation.ADD, other)

    def __radd__(self, other):
        return self.__add__(other)
    
    def __sub__(self, other):
        if isinstance(other, (int, float)):
            other = Value(other)
        return Combination(self, Operation.SUBTRACT, other)
    
    def __rsub__(self, other):
        if isinstance(other, (int, float)):
            other = Value(other)
        return Combination(other, Operation.SUBTRACT, self)
    
    def __mul__(self, other):
        if isinstance(other, (int, float)):
            other = Value(other)
        return Combination(self, Operation.MULTIPLY, other)
    
    def __rmul__(self, other):
        return self.__mul__(other)
    
    def __truediv__(self, other):
        if isinstance(other, (int, float)):
            other = Value(other)
        return Combination(self, Operation.DIVIDE, other)
    
    def __rtruediv__(self, other):
        if isinstance(other, (int, float)):
            other = Value(other)
        return Combination(other, Operation.DIVIDE, self) 
    
    def __pow__(self, other):
        if isinstance(other, (int, float)):
            other = Value(other)
        return Combination(self, Operation.POWER, other)
    
    def __rpow__(self, other):
        if isinstance(other, (int, float)):
            other = Value(other)
        return Combination(other, Operation.POWER, self)
    
    def __neg__(self):
        return Combination(Value(0), Operation.SUBTRACT, self)
    
    def __abs__(self):
        return Combination(self, Operation.ABS, Value(0))

    def to_expression(self):
        return "y = " + str(self)
    
    # For superclass Curve
    
    def point(self, x):
        return (x, self.evaluate(x))
    
    def parameter_interval(self, renderer):
        return renderer.boundL, renderer.boundR
    
    # Framework for subclasses
    
    def evaluate(self, x):
        raise NotImplementedError
    
    def __str__(self):
        raise NotImplementedError
    
class Combination(Function):
    def __init__(self, left, operation, right):
        super().__init__()
        self.left = left
        if isinstance(self.left, (int, float)):
            self.left = Value(self.left)

        self.right = right
        if isinstance(self.right, (int, float)):
            self.right = Value(self.right)
        
        self.operation = operation
        #print(self.left, self.right, type(self.left), type(self.right))
    
    def evaluate(self, x):
        a = self.left.evaluate(x)
        b = self.right.evaluate(x)
        if a is None or b is None:
            result = None
        else:

            try:
                if self.operation == Operation.ADD:
                    result = a + b
                elif self.operation == Operation.SUBTRACT:
                    result = a - b
                elif self.operation == Operation.MULTIPLY:
                    result = a * b
                elif self.operation == Operation.DIVIDE:
                    result = a / b
                elif self.operation == Operation.POWER:
                    result = a ** b
                elif self.operation == Operation.ABS:
                    result = abs(a)

            except ZeroDivisionError:
                result = None
            except TypeError:
                result = None
            except ValueError:
                result = None

        if not isinstance(result, (int, float)):
            result = None

        # print(f"{x:g}", result)
        return result
        
    def __str__(self):
        string = ""
        if self.operation == Operation.ADD:
            if (str(self.left) == "0" or isinstance(self.left, Value)) and (str(self.right) == "0" or isinstance(self.right, Value)):
                return str(self.left.evaluate(0) + self.right.evaluate(0))
            
            if isinstance(self.left, Value):
                if self.left.evaluate(0) == 0:
                    return str(self.right)
                else:
                    return f"{str(self.left)} + ({str(self.right)})"

            if isinstance(self.right, Value):
                if self.right.evaluate(0) == 0:
                    return str(self.left)
                elif self.right.evaluate(0) < 0:
                    return f"({str(self.left)}) - {str(Value(-self.right.evaluate(0)))}"
                else:
                    return f"({str(self.left)}) + {str(self.right)}"
            
            return f"({str(self.left)}) + ({str(self.right)})"

        elif self.operation == Operation.SUBTRACT:
            if (str(self.left) == "0" or isinstance(self.left, Value)) and (str(self.right) == "0" or isinstance(self.right, Value)):
                return str(self.left.evaluate(0) - self.right.evaluate(0))
            
            if isinstance(self.left, Value):
                if self.left.evaluate(0) == 0:
                    return f"-({str(self.right)})"
                else:
                    return f"{str(self.left)} - ({str(self.right)})"

            if isinstance(self.right, Value):
                if self.right.evaluate(0) == 0:
                    return str(self.left)
                elif self.right.evaluate(0) < 0:
                    return f"({str(self.left)}) + {str(Value(-self.right.evaluate(0)))}"
                else:
                    return f"({str(self.left)}) - {str(self.right)}"
            
            return f"({str(self.left)}) - ({str(self.right)})"

        elif self.operation == Operation.MULTIPLY:
            if (str(self.left) == "0" or isinstance(self.left, Value)) and (str(self.right) == "0" or isinstance(self.right, Value)):
                return str(self.left.evaluate(0) * self.right.evaluate(0))
            
            if isinstance(self.left, Value):
                if self.left.evaluate(0) == 0:
                    return "0"
                elif self.left.evaluate(0) == 1:
                    return str(self.right)
                else:
                    # New logic for multiplication with combinations
                    if isinstance(self.right, Combination):
                        if self.right.operation == Operation.MULTIPLY:
                            if isinstance(self.right.left, Value):
                                return f"{str(Combination(self.left.evaluate(0) * self.right.left.evaluate(0), Operation.MULTIPLY, self.right.right))}"
                            elif isinstance(self.right.right, Value):
                                return f"{str(Combination(self.left.evaluate(0) * self.right.right.evaluate(0), Operation.MULTIPLY, self.right.left))}"

                        elif self.right.operation == Operation.DIVIDE:
                            if isinstance(self.right.left, Value):
                                return f"{str(Combination(self.left.evaluate(0) * self.right.left.evaluate(0), Operation.DIVIDE, self.right.right))}"
                            elif isinstance(self.right.right, Value):
                                return f"{str(Combination(self.left.evaluate(0) / self.right.right.evaluate(0), Operation.MULTIPLY, self.right.left))}"
                        
                    return f"{str(self.left)} * ({str(self.right)})"

            if isinstance(self.right, Value):
                if self.right.evaluate(0) == 0:
                    return "0"
                elif self.right.evaluate(0) == 1:
                    return str(self.left)
                elif isinstance(self.left, Variable):
                    return f"{str(self.left)} * {str(self.right)}"
                else:
                    return f"({str(self.left)}) * {str(self.right)}"
            
            return f"({str(self.left)}) * ({str(self.right)})"

        elif self.operation == Operation.DIVIDE:
            if (str(self.left) == "0" or isinstance(self.left, Value)) and (str(self.right) == "0" or isinstance(self.right, Value)):
                try:
                    return str(self.left.evaluate(0) / self.right.evaluate(0))
                except ZeroDivisionError:
                    return str("NaN")
            
            if isinstance(self.left, Value):
                if self.left.evaluate(0) == 0:
                    return "0"
                else:
                    return f"{str(self.left)} / ({str(self.right)})"

            if isinstance(self.right, Value):
                if self.right.evaluate(0) == 1:
                    return str(self.left)
                elif isinstance(self.left, Variable):
                    return f"{str(self.left)} / {str(self.right)}"
                else:
                    return f"({str(self.left)}) / {str(self.right)}"
            
            return f"({str(self.left)}) / ({str(self.right)})"
        
        elif self.operation == Operation.POWER:
            if (str(self.left) == "0" or isinstance(self.left, Value)) and (str(self.right) == "0" or isinstance(self.right, Value)):
                return str(self.left.evaluate(0) ** self.right.evaluate(0))
            
            if isinstance(self.left, Value):
                if self.left.evaluate(0) == 0:
                    return "0"
                elif self.left.evaluate(0) == 1:
                    return "1"
                elif self.left.evaluate(0) > 0:
                    return f"{str(self.left)} ^ ({str(self.right)})"

            if isinstance(self.right, Value):
                if self.right.evaluate(0) == 0:
                    return "1"
                elif self.right.evaluate(0) == 1:
                    return str(self.left)
                elif isinstance(self.left, Variable):
                    return f"{str(self.left)} ^ {str(self.right)}"
                else:
                    return f"({str(self.left)}) ^ {str(self.right)}"
            
            return f"({str(self.left)}) ^ ({str(self.right)})"
        
        return f"({str(self.left)}) {self.operation} ({str(self.right)})"

class Value(Function):
    def __init__(self, value):
        super().__init__()
        self._value = value

    @property
    def value(self):
        if callable(self._value):
            return self._value()
        return self._value

    @value.setter
    def value(self, new):
        self._value = new

    def __str__(self):
        return f"{self.value:.3f}"

    def __add__(self, other):
        if isinstance(other, Value):
            return Value(lambda: self.evaluate() + other.evaluate())
        elif isinstance(other, (float, int)):
            return Value(lambda: self.evaluate()+ other)
        else:
            raise TypeError

    def __radd__(self, other):
        return self + other

    def __sub__(self, other):
        if isinstance(other, Value):
            return Value(lambda: self.evaluate() - other.evaluate())
        elif isinstance(other, (float, int)):
            
            return Value(lambda: self.evaluate() - other)
        else:
            raise TypeError

    def __rsub__(self, other):
        if isinstance(other, Value):
            return Value(lambda: other.evaluate() - self.evaluate())
        elif isinstance(other, (float, int)):
            return Value(lambda: other - self.evaluate())
        else:
            raise TypeError

    def __mul__(self, other):
        if isinstance(other, Value):
            return Value(lambda: self.evaluate() * other.evaluate())
        elif isinstance(other, (float, int)):
            return Value(lambda: self.evaluate() * other)
        else:
            raise TypeError

    def __rmul__(self, other):
        return self * other

    def __truediv__(self, other):
        if isinstance(other, Value):
            return Value(lambda: self.evaluate() / other.evaluate())
        elif isinstance(other, (float, int)):
            return Value(lambda: self.evaluate() / other)
        else:
            raise TypeError

    def __rtruediv__(self, other):
        if isinstance(other, Value):
            return Value(lambda: other.evaluate() / self.evaluate())
        elif isinstance(other, (float, int)):
            return Value(lambda: other / self.evaluate())
        else:
            raise TypeError

    def evaluate(self, x=0):
        return self.value

def dynamic(value):
    if callable(value):
        return Value(value)
    return Value(lambda: value)

class Variable(Function):
    def __init__(self, name):
        super().__init__()
        self.name = name

    
    def __str__(self):
        return f"{self.name}"
    
    def evaluate(self, x):
        return x
    