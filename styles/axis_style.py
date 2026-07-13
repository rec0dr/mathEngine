from .style import Style
from dataclasses import dataclass

@dataclass
class AxisStyle(Style):

    draw_x: bool = True
    draw_y: bool = True

    show_arrows: bool = True
    show_origin: bool = True

    label_x: str = "x"
    label_y: str = "y"
