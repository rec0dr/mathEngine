from .style import Style
from .point_style import PointStyle
from dataclasses import dataclass

@dataclass
class CircleStyle(Style):
    thickness: int = 2
    show_center: bool = False
    center_style: PointStyle | None = None
    