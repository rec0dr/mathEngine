import math
from enum import Enum, auto
def lerp(a, b, t):
    return a + (b - a) * t

def interpolate(a, b, t):
    if isinstance(a, tuple) and isinstance(b, tuple):
        return tuple(interpolate(x, y, t) for x, y in zip(a, b))
    return lerp(a, b, t)


class EaseType(Enum):
    LINEAR = auto()
    SIN_IN = auto()
    SIN_OUT = auto()
    SIN_IN_OUT = auto()
    QUADRATIC_IN = auto()
    QUADRATIC_OUT = auto()
    CUBIC_IN = auto()
    CUBIC_OUT = auto()
    QUARTIC_IN = auto()
    QUARTIC_OUT = auto()

def linear(t):
    return t

def sin_in(t):
    return math.sin((math.pi/2)*(t-1)) + 1

def sin_out(t):
    return math.sin((math.pi/2)*t)

def sin_in_out(t):
    return 1/2 * math.sin(math.pi*(t-0.5)) + 0.5

# General polynomial ease functions

def n_deg_in(n, t):
    return t**n

def n_deg_out(n, t):
    return 1 - ((1-t)**n)

def quadratic_in(t):
    return t * t

def quadratic_out(t):
    return 1 - (1-t)**2

def cubic_in(t):
    return n_deg_in(3, t)

def cubic_out(t):
    return n_deg_out(3, t)

def quartic_in(t):
    return n_deg_in(4, t)

def quartic_out(t):
    return n_deg_out(4, t)

EASING = {
    EaseType.LINEAR: linear,
    EaseType.SIN_IN: sin_in,
    EaseType.SIN_OUT: sin_out,
    EaseType.SIN_IN_OUT: sin_in_out,
    EaseType.QUADRATIC_IN: quadratic_in,
    EaseType.QUADRATIC_OUT: quadratic_out,
    EaseType.CUBIC_IN: cubic_in,
    EaseType.CUBIC_OUT: cubic_out,
    EaseType.QUARTIC_IN: quartic_in,
    EaseType.QUARTIC_OUT: quartic_out,
}
