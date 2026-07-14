import math
from .parametric import Parametric
from .sinusoid import Sinusoid, TrigType

class Polar(Parametric):
    def __init__(self, r):
        super().__init__(
            r * Sinusoid.from_basic(TrigType.COS),
            r * Sinusoid.from_basic(TrigType.SIN)
        )