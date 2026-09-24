from functions.function import Function

class Label:
    def __init__(self, x=0, y=0, text=None):
        self._x = x
        self._y = y

        self._auto_text = text is None
        self._text = f"({x}, {y})" if self._auto_text else text
    
    def update(self, dt):
        pass

    def evaluate(self, value):
        if isinstance(value, Function):
            return value.evaluate(0)
        return value

    @property
    def x(self):
        return self.evaluate(self._x)

    @x.setter
    def x(self, value):
        self._x = value
        if self._auto_text:
            self._text = f"({self.x}, {self.y})"

    @property
    def y(self):
        return self.evaluate(self._y)

    @y.setter
    def y(self, value):
        self._y = value
        if self._auto_text:
            self._text = f"({self.x}, {self.y})"

    @property
    def text(self):
        if callable(self._text):
            return self._text()
        return self._text

    @text.setter
    def text(self, value):
        self._text = value
        self._auto_text = False

    @property
    def pos(self):
        return (self._x, self._y)

    @pos.setter
    def pos(self, value):
        self._x, self._y = value
        if self._auto_text:
            self._text = f"({self._x}, {self._y})"

    def __str__(self):
        return f"{self._x, self._y}"