from styles.__init__ import *
from objects.__init__ import *
from functions.curve import Curve

DRAW_MAP = {
    Point: "draw_point",
    Curve: "draw_curve",
    Label: "draw_label",
    LineSegment: "draw_line_segment"
}

STYLE_MAP = {
    Point: PointStyle,
    Curve: CurveStyle,
    Label: TextStyle,
    LineSegment: LineSegmentStyle
}