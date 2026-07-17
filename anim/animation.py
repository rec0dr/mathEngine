import math
from enum import Enum

class EaseType(Enum):
    LINEAR = 0
    SIN_SMOOTH = 1

class Animation:
    def __init__(self, target, property_name, end=1, duration=1, ease_type: EaseType = EaseType.LINEAR, start=None):
        self.target = target
        
        parts = property_name.split(".")
        for part in parts[:-1]:
            self.target = getattr(self.target, part)
        
        self.property_name = parts[-1]

        if start is None:
            start = getattr(self.target, self.property_name)
        self.start = start
        self.end = end
        self.duration = duration
        self.ease_type = ease_type

        self.elapsed = 0
        self.finished = False
    
    @classmethod
    def multiple(cls, target, duration, ease_type, **attrs):
        return [
            cls(target, name, end, duration, ease_type, start=getattr(target, name)) 
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
            self.finished = True
        
        a, b = self.start, self.end

        if self.ease_type == EaseType.LINEAR:
            value = self.linear(a, b, t)
        elif self.ease_type == EaseType.SIN_SMOOTH:
            value = self.sin_smooth(a, b, t)
        else:
            raise ValueError(f"Unknown easing type: {self.ease_type}")
        
        setattr(self.target, self.property_name, value)