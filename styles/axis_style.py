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
    show_origin: bool = True

    label_x: AxisLabel = field(default_factory=lambda: AxisLabel("x"))
    label_y: AxisLabel = field(default_factory=lambda: AxisLabel("y"))
    label_negatives: bool = False