from .style import Style
from .text_style import TextStyle
from .axis_label import AxisLabel
from dataclasses import dataclass, field

@dataclass
class AxisStyle(Style):

    thickness: int = 2

    draw_x: bool = True
    draw_y: bool = True

    show_arrows: bool = True
    arrow_dims: tuple[int, int] = (50, 20)
    show_origin: bool = True
    origin_radius: int = 10

    label_x: AxisLabel = None
    label_y: AxisLabel = None
    label_negatives: bool = False