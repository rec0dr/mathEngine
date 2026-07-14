import math

from functions.function import Function
from styles.func_style import FuncStyle

class GraphObject:
    def __init__(self, function, style=None, **style_kwargs):
        if style is not None and style_kwargs:
            raise ValueError(
                "Cannot specify both 'style' and individual style properties!"
            )
        
        if style is not None:
            if not isinstance(style, FuncStyle):
                raise TypeError("style must be a FuncStyle")
            else:
                self.style = style
        else:
            self.style = FuncStyle(**style_kwargs)

        self.function = function
        