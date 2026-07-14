import math

from .style import Style
from .func_style import FuncStyle
from dataclasses import dataclass

@dataclass
class ParametricStyle(FuncStyle):
    tMin: float = 0
    tMax: float = 2*math.pi