"""
Simple class for polar functions.

Defined as a branch off of parametric functions,
where x(t) = rcos(t) and y(t) = rsin(t).

Author: Evan Le
Date: 2026-10-21
License: Personal Use
"""

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