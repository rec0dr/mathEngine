from dataclasses import dataclass, field
from .text_style import TextStyle
@dataclass
class AxisLabel:
    text: str
    style: TextStyle = field(default_factory=TextStyle)