from dataclasses import dataclass
from .text_style import TextStyle

@dataclass
class TickStyle:
    color: tuple = (255,255,255)
    opacity: int = 255
    visible: bool = True

    factor_x: int = 10
    factor_y: int = 10

    base_dist0x: float = 1
    base_dist0y: float = base_dist0x

    thickness: int = 2

    labeled: bool = False
    label_style: TextStyle = None

    