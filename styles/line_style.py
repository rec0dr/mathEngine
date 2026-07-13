from .style import Style
from dataclasses import dataclass

@dataclass
class LineStyle(Style):
    thickness: int = 2
