import math
from enum import Enum

class Operation(Enum):
    ADD = "+"
    SUBTRACT = "-"
    MULTIPLY = "*"
    DIVIDE = "/"
    POWER = "**"

# Function combination logic

class Function:
    # Function combo logic
    
    def __add__(self, other):
        if isinstance(other, (int, float)):
            other = Constant(other)
        return Combination(self, Operation.ADD, other)

    def __radd__(self, other):
        return self.__add__(other)
    
    def __sub__(self, other):
        if isinstance(other, (int, float)):
            other = Constant(other)
        return Combination(self, Operation.SUBTRACT, other)
    
    def __rsub__(self, other):
        if isinstance(other, (int, float)):
            other = Constant(other)
        return Combination(other, Operation.SUBTRACT, self)
    
    def __mul__(self, other):
        if isinstance(other, (int, float)):
            other = Constant(other)
        return Combination(self, Operation.MULTIPLY, other)
    
    def __rmul__(self, other):
        return self.__mul__(other)
    
    def __truediv__(self, other):
        if isinstance(other, (int, float)):
            other = Constant(other)
        return Combination(self, Operation.DIVIDE, other)
    
    def __rtruediv__(self, other):
        if isinstance(other, (int, float)):
            other = Constant(other)
        return Combination(other, Operation.DIVIDE, self) 
    
    def __pow__(self, other):
        if isinstance(other, (int, float)):
            other = Constant(other)
        return Combination(self, Operation.POWER, other)
    
    def __rpow__(self, other):
        if isinstance(other, (int, float)):
            other = Constant(other)
        return Combination(other, Operation.POWER, self)
    
    def __neg__(self):
        return Combination(Constant(0), Operation.SUBTRACT, self)

    def to_expression(self):
        return "y = " + str(self)
    
    # Framework for subclasses
    
    def evaluate(self, x):
        raise NotImplementedError
    
    def __str__(self):
        raise NotImplementedError
    
class Combination(Function):
    def __init__(self, left, operation, right):
        self.left = left
        self.right = right
        self.operation = operation
    
    def evaluate(self, x):
        a = self.left.evaluate(x)
        b = self.right.evaluate(x)
        if a is None or b is None:
            return None
        
        if self.operation == Operation.ADD:
            return a + b
        elif self.operation == Operation.SUBTRACT:
            return a - b
        elif self.operation == Operation.MULTIPLY:
            return a * b
        elif self.operation == Operation.DIVIDE:
            return a / b
        elif self.operation == Operation.POWER:
            return a ** b
    
    def __str__(self):
        return f"({str(self.left)}) {self.operation.value} ({str(self.right)})"

class Constant(Function):
    def __init__(self, value):
        self.value = value
    
    def __str__(self):
        return f"{self.value}"
    
    def evaluate(self, x):
        return self.value

class Variable(Function):
    def __init__(self, name):
        self.name = name
    
    def __str__(self):
        return f"{self.name}"
    
    def evaluate(self, x):
        return x
    