from .style import Style
from dataclasses import dataclass

@dataclass
class CurveStyle(Style):
    thickness: int = 2
    show_arrows: bool = False
    arrow_dims: tuple[int, int] = (50, 20)