import pygame
from functions.__init__ import *
from styles.__init__ import *
from objects.__init__ import *
from graphing.__init__ import *

width, height = (1200, 1200)
scaleX, scaleY = (10,10)
app = GraphApp(width, height, scaleX, scaleY, fps=60, pan_sensitivity=100, zoom_sensitivity=100)
app.renderer.default_CurveStyle = CurveStyle(BLUE, thickness=2)
func0 = PARAMETRIC_ELLIPSE(2, 5)
func1 = AnimatedPoint(func0, 0, 0.5)
app.add_graphObject(GraphObject(func0))
app.add_graphObject(GraphObject(func1, PointStyle(radius_px=10, labeled=True)))
app.run()