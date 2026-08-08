import math
from .easing import *

class Animation:
    def __init__(self, target, property_name, end=1, duration=1, ease_type: EaseType = EaseType.LINEAR, start=None, loop=True, two_way=True):
        self.target = target
        
        parts = property_name.split(".")
        for part in parts[:-1]:
            self.target = getattr(self.target, part)
        
        self.property_name = parts[-1]
        # print(self.target, self.property_name)

        if start is None:
            start = getattr(self.target, self.property_name)
        self.start = start
        self.end = end
        self.duration = duration
        self.ease_type = ease_type

        self.elapsed = 0
        self.finished = False
        self.loop = loop
        self.two_way = two_way
    
    @classmethod
    def multiple(cls, target, duration=1, ease_type=EaseType.LINEAR, loop=True, two_way=True, **attrs):
        return [
            cls(target, name, end, duration, ease_type, loop=loop, two_way=two_way) 
            for name, end in attrs.items()
        ]
    
    def linear(self, a, b, t):
        if isinstance(a, tuple):
            return tuple(self.linear(x, y, t) for x, y in zip(a, b))
        return a + (b - a) * t

    def sin_smooth(self, a, b, t):
        if isinstance(a, tuple):
            return tuple(self.sin_smooth(x, y, t) for x, y in zip(a, b))
        return self.linear(a, b, (1/2 * math.sin(math.pi*(t-0.5))) + 0.5)
    
    def update(self, dt):

        self.elapsed += dt
        
        t = min(self.elapsed / self.duration, 1)
        
        if t == 1:
            if self.loop:
                self.elapsed = 0
            else:
                self.finished = True

        real_t = t
        if self.two_way:
            if t < 0.5:
                real_t = 2*t
            else:
                real_t = 2*(1 - t)
        
        a, b = self.start, self.end
        real_t = EASING[self.ease_type](real_t)
        value = interpolate(a, b, real_t)
        
        setattr(self.target, self.property_name, value)