from .traced_point import TracedPoint
from functions.curve import Curve
from functions.parametric import Parametric

class AnimatedPoint(TracedPoint):
    def __init__(self, curve: Curve, tStart, motion):
        self.motion = motion
        super().__init__(curve, tStart)
    
    def update(self, fps):
        self.moveBy(self.motion/fps)

