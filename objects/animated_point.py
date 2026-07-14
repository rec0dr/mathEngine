from .point import Point
from functions.function import Function
from functions.parametric import Parametric

class AnimatedPoint(Point):
    def __init__(self, func, Xmin, motion):
        if isinstance(func, Function):
            pos = [Xmin, func.evaluate(Xmin)]
        elif isinstance(func, Parametric):
            pos = func.evaluate(Xmin)

        self.motion = motion
        self.func = func
        self.x = Xmin
        super().__init__(pos)
    
    def update(self, fps):
        self.x += self.motion/fps
        if isinstance(self.func, Function):
            pos = [self.x, self.func.evaluate(self.x)]
        elif isinstance(self.func, Parametric):
            pos = self.func.evaluate(self.x)
        self.pos = pos

