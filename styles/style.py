from dataclasses import dataclass

@dataclass
class Style:
    color: tuple = (255,255,255)
    opacity: int = 255
    visible: bool = True