from .style import Style
from dataclasses import dataclass

@dataclass
class TextStyle(Style):
    font_size: float = 18
    font_type: any = None
    bold: bool = False
    italic: bool = False
    