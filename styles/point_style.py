from .style import Style
from .text_style import TextStyle
from dataclasses import dataclass, field

@dataclass
class PointStyle(Style):
    is_solid: bool = True
    radius_px: float = 3
    border_width_px: int = 0
    labeled: bool = False
    label_text_style: TextStyle = None