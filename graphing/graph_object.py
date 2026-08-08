import math
from styles.style import Style
from .registries import STYLE_MAP
class GraphObject:
    def __init__(self, drawable, style=None):
        self.drawable = drawable
        self.style = style
        self.z_index = 0

    @classmethod
    def from_atts(cls, drawable, **style_kwargs):
        for clas in type(drawable).__mro__:
            if clas in STYLE_MAP:
                style_name = STYLE_MAP[clas]
                break
        
        return cls(drawable, style_name(**style_kwargs))
        