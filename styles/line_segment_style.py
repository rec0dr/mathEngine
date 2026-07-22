from .style import Style
from .text_style import TextStyle
from .point_style import PointStyle
from dataclasses import dataclass

@dataclass
class LineSegmentStyle(Style):
    thickness: int = 2
    show_ends: bool = True
    endpoint_style: PointStyle = None
    label_ends: bool = False
    label_style: TextStyle = None
