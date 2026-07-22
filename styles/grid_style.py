from .style import Style
from dataclasses import dataclass

@dataclass
class GridStyle(Style):
    major_color: tuple = (255,255,255)
    major_opacity: int = 255
    major_spacing: float = 1

    minor_color: tuple = (255,255,255)
    minor_opacity: int = 128
    minor_spacing: int = 0.2

    

