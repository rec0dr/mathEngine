from functions.function import Function, Value

class Point:
    def __init__(self, *args):
        if len(args) == 1 and isinstance(args[0], (tuple, list)):
            self._x, self._y = args[0]
        elif len(args) == 2:
            self._x, self._y = args
        else:
            raise ValueError

        if isinstance(self._x, (int, float)):
            self._x = Value(self._x)

        if isinstance(self._y, (int, float)):
            self._y = Value(self._y)



    def evaluate(self, value):
        return value.evaluate(0)

    @property
    def pos(self): 
        return (self.evaluate(self._x), self.evaluate(self._y))

    @property
    def x(self):
        return self.evaluate(self._x)

    @x.setter
    def x(self, value):
        self._x = value

    @property
    def y(self):
        return self.evaluate(self._y)

    @y.setter
    def y(self, value):
        self._y = value

    @pos.setter
    def pos(self, tuple):
        self._x, self._y = tuple
    
    def update(self, dt):
        pass
    
    def __str__(self):
        return f"({self.x}, {self.y})"