from .style import Style
from dataclasses import dataclass

@dataclass
class PointStyle(Style):
    is_solid: bool = True
    radius_px: float = 3
    border_width_px: int = 0
    labeled: bool = False