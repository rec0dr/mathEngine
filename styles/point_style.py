from .style import Style
from .text_style import TextStyle
from dataclasses import dataclass, field
from enum import Enum

class LockType(Enum):
    X       = "X"
    Y       = "Y"
    BOTH    = "X,Y"
    FREE    = ""

@dataclass
class PointStyle(Style):
    is_solid: bool = True
    radius_px: float = 3
    border_width_px: int = 0
    labeled: bool = False
    label_style: TextStyle = None

    draggable: bool = False
    lock_type: str = LockType.FREE
    hovered: bool = False
