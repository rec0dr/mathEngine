from functions.function import Function, Value

class LineSegment:
    def __init__(self, pos1, pos2):
        self.x1, self.y1 = pos1
        self.x2, self.y2 = pos2

    def evaluate_point(self, point):
        x, y = point

        if isinstance(x, Function):
            x = x.evaluate(0)

        if isinstance(y, Function):
            y = y.evaluate(0)

        return (x, y)

    @property
    def pos1(self):
        return self.evaluate_point((self.x1, self.y1))

    @property
    def pos2(self):
        return self.evaluate_point((self.x2, self.y2))

    @pos1.setter
    def pos1(self, value):
        self.x1, self.y1 = value

    @pos2.setter
    def pos2(self, value):
        self.x2, self.y2 = value

    def update(self, dt):
        pass

    def __str__(self):
        return f"{self.pos1} -> {self.pos2}"