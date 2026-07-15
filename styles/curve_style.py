from .style import Style
from dataclasses import dataclass

@dataclass
class CurveStyle(Style):
    thickness: int = 2
