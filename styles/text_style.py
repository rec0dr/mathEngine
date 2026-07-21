from .style import Style
from dataclasses import dataclass

@dataclass
class TextStyle(Style):
    font_size: float = 18
    # In case of wanting permanent size no matter the zoom
    fixed_zoom: bool = False
    base_scale: float = 10
    
    font_type: any = None
    bold: bool = False
    italic: bool = False
    