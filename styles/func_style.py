from .style import Style
from dataclasses import dataclass

@dataclass
class FuncStyle(Style):
    thickness: int = 2
