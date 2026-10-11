import math
from .parametric import Parametric
from .sinusoid import Sinusoid, TrigType

class Polar(Parametric):
    def __init__(self, r, thetaMin, thetaMax):
        super().__init__(
            r * Sinusoid(trig_type=TrigType.COS),
            r * Sinusoid(trig_type=TrigType.SIN),
            thetaMin,
            thetaMax
        )