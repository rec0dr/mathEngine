from dataclasses import dataclass
from .style import Style
from .text_style import TextStyle

@dataclass
class TickStyle(Style):
    show_ui: bool = False
    factor_x: int = 10
    factor_y: int = 10

    base_dist0x: float = 1
    base_dist0y: float = base_dist0x

    thickness: int = 2

    labeled: bool = False
    label_style: TextStyle = None

    