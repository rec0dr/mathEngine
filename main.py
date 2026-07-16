import pygame
from functions.__init__ import *
from styles.__init__ import *
from objects.__init__ import *
from graphing.__init__ import *

width, height = (600, 600)
scaleX, scaleY = (10,10)
app = GraphApp(width, height, scaleX, scaleY, fps=60, pan_sensitivity=100, zoom_sensitivity=100)
app.renderer.default_CurveStyle = CurveStyle(BLUE, thickness=2)
app.renderer.default_PointStyle = PointStyle(color=RED, radius_px=3, border_width_px=0, labeled=True)

app.add_graphObject(GraphObject(AnimatedPoint(Sinusoid.from_basic(TrigType.SIN), 0, 1)))
app.add_graphObject(GraphObject(Sinusoid.from_basic(TrigType.SIN)))
app.add_graphObject(GraphObject(PARAMETRIC_ELLIPSE(1,3), style=CurveStyle(RED, thickness=2)))
app.run()