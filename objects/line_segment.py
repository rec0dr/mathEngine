from functions.function import Function, Value
from .point import Point

class LineSegment:
    def __init__(self, pos1, pos2):
        if isinstance(pos1, Point):
            p = pos1
            pos1 = (
                Value(lambda p=p: p.x),
                Value(lambda p=p: p.y)
            )

        if isinstance(pos2, Point):
            p = pos2
            pos2 = (
                Value(lambda p=p: p.x),
                Value(lambda p=p: p.y)
            )

        self.x1, self.y1 = pos1
        self.x2, self.y2 = pos2

    @classmethod
    def from_path(cls, path):
        if len(path) < 2:
            raise ValueError("Path must contain at least two points to create a line segment.")

        lineset = []
        previous_point = None
        for point in path:
            if previous_point is not None:
                lineset.append(cls(previous_point, point))
            previous_point = point
        return lineset
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
        return f"({self.pos1[0]:.3f}, {self.pos1[1]:.3f}) to ({self.pos2[0]:.3f}, {self.pos2[1]:.3f})"