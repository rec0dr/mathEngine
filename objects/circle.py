from functions.function import Function, Value

class Circle:
    def __init__(self, center, radius):
        self._center = center
        x, y = self._center
        if isinstance(x, (int, float)):
            x = Value(x)
        if isinstance(y, (int, float)):
            y = Value(y)
        self._center = (x, y)
        self._radius = radius
        if isinstance(radius, (int, float)):
            self._radius = Value(radius)

    def __str__(self):
        return f"C: {self.center}, R: {self.radius}"

    def evaluate_point(self, point):
        return (point[0].evaluate(0), point[1].evaluate(0))

    def evaluate(self, value):
        return value.evaluate(0)

    @property
    def center(self):
        return self.evaluate_point(self._center)

    @center.setter
    def center(self, value):
        self._center = self.center

    @property
    def radius(self):
        return self.evaluate(self._radius)

    @radius.setter
    def radius(self, value):
        self._radius = self.radius

    