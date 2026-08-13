from styles.__init__ import *
from objects.__init__ import *
from functions.parametric import Parametric
from functions.function import Function
from functions.curve import Curve

DRAW_MAP = {
    Point: "draw_point",
    Curve: "draw_curve",
    Label: "draw_label",
    LineSegment: "draw_line_segment",
    Circle: "draw_circle"
}

NAME_MAP = {
    Point: "Point",
    Parametric: "Parametric",
    Function: "Function",
    Label: "Label",
    LineSegment: "Line Segment",
    Circle: "Circle"
}

STYLE_MAP = {
    Point: PointStyle,
    Curve: CurveStyle,
    Label: TextStyle,
    LineSegment: LineSegmentStyle,
    Circle: CircleStyle
}