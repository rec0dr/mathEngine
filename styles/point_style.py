from .style import Style
from dataclasses import dataclass

@dataclass
class PointStyle(Style):
    is_solid: bool = True
    radiusPX: float = 5
    border_widthPX: int = 0