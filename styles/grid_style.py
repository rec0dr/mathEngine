from .style import Style
from dataclasses import dataclass

@dataclass
class GridStyle(Style):
    color: tuple = (255,255,255)
    opacity: int = 100
    visible: bool = True

    show_ui: bool = False
    name: str = ""
    
    thickness: int = 2
    minor_color: tuple = (255,255,255)
    minor_opacity: int = 50
    minor_thickness: int = 1
    minor_visible: bool = True

    

