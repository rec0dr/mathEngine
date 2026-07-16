import pygame
from anim.__init__ import *
from functions.__init__ import *
from styles.__init__ import *
from objects.__init__ import *
from graphing.__init__ import *

width, height = (1200, 1200)
scaleX, scaleY = (10,10)
app = GraphApp(width, height, scaleX, scaleY, fps=60, pan_sensitivity=100, zoom_sensitivity=100)
app.renderer.default_CurveStyle = CurveStyle(BLUE, thickness=2)
app.renderer.default_PointStyle = PointStyle(color=RED, radius_px=3, border_width_px=0, labeled=True)
app.renderer.default_AxisStyle.arrow_dims = (20,10)


func0 = SIN
app.add_graphObject(GraphObject(func0))

animValue = Constant(0)

a = GraphObject(TracedPoint(func0, 0), style=PointStyle(color=RED, radius_px=10, labeled=True, label_text_style=TextStyle(font_size=36, color=BLUE, italic=False)))
app.add_animation(Animation(a.drawable, "parameter", end=-10, duration=5, ease_type=EaseType.SIN_SMOOTH))
app.add_graphObject(a)

app.run()