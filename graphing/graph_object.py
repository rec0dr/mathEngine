import math

from functions.function import Function
from functions.parametric import Parametric
from objects.point import Point
from objects.line_segment import LineSegment

from styles.style import Style
from styles.func_style import FuncStyle
from styles.parametric_style import ParametricStyle
from styles.point_style import PointStyle

class GraphObject:
    def __init__(self, obj, style=None, **style_kwargs):
        if style is not None and style_kwargs:
            raise ValueError(
                "Cannot specify both 'style' and individual style properties!"
            )
        
        if style is not None:
            if not isinstance(style, Style):
                raise TypeError("style must be a Style")
            else:
                self.style = style
        else:
            if isinstance(obj, Function):
                self.style = FuncStyle(**style_kwargs)
            elif isinstance(obj, Parametric):
                self.style = ParametricStyle(**style_kwargs)
            elif isinstance(obj, Point):
                self.style = PointStyle(**style_kwargs)
            elif isinstance(obj, LineSegment):
                self.style = FuncStyle(**style_kwargs)

        self.obj = obj
    
    def hide(self):
        self.style.visible = False
    
    def show(self):
        self.style.visible = True
        

        