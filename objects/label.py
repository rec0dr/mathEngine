class Label:
    def __init__(self, x=0, y=0, text=None):
        self._x = x
        self._y = y

        self._auto_text = text is None
        self._text = f"({x}, {y})" if self._auto_text else text

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, value):
        self._x = value
        if self._auto_text:
            self._text = f"({self._x}, {self._y})"

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, value):
        self._y = value
        if self._auto_text:
            self._text = f"({self._x}, {self._y})"

    @property
    def text(self):
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