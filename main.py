import math
import random

from anim.__init__ import *
from functions.__init__ import *
from styles.__init__ import *
from objects.__init__ import *
from graphing.__init__ import *

width, height = (1000, 1000)
scaleX, scaleY = (10,10)

app = GraphApp(width, height, scaleX, scaleY, fps=90, pan_sensitivity=100, zoom_sensitivity=100, fixed_center = None)

def bezier(p0, p1, p2, p3, p4):
    t0 = ((1 - X) ** 4) * p0
    t1 = ((1 - X) ** 3) * X * p1
    t2 = ((1 - X) ** 2) * (X**2) * p2
    t3 = ((1 - X)) * (X**3) * p3
    t4 = (X**4) * p4
    return t0 + t1 + t2 + t3 + t4

x_curve = SIN(X) - 5
app.add_object(x_curve, name="start", color=RED)
traced_pt = TracedPoint(x_curve, 0)
#app.add_animation(traced_pt, "parameter", 20, 30, EaseType.LINEAR)
app.add_object(traced_pt, name="start", color=RED, draggable=True)
other_pt = TracedPoint(X**2, Value(lambda: traced_pt.y + 5))
app.add_object(X**2, name="result", color=BLUE)
app.add_object(other_pt, radius_px=8, color=BLUE, name="result")
mod_pt = TracedPoint(X**2, 2 * Value(lambda: traced_pt.y + 5))
app.add_object(mod_pt, radius_px=8, color=PURPLE, name="mod_result")
app.add_object(LineSegment(other_pt, mod_pt))
app.run()