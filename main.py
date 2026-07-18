import pygame
from anim.__init__ import *
from functions.__init__ import *
from styles.__init__ import *
from objects.__init__ import *
from graphing.__init__ import *

width, height = (1200, 1200)
scaleX, scaleY = (10,10)
app = GraphApp(width, height, scaleX, scaleY, fps=60, pan_sensitivity=100, zoom_sensitivity=100)
app.renderer.default_AxisStyle.arrow_dims = (20,10)

func0 = Value(0)
func1 = Value(2)
app.add_graphObject(GraphObject(func0))
point0 = GraphObject(TracedPoint(func0, 0), style=PointStyle(labeled=True, label_style=TextStyle(font_size=25, color=(255,0,0))))
point1 = GraphObject(TracedPoint(func1, 0), style=PointStyle(labeled=True, label_style=TextStyle(font_size=25, color=(255,0,0))))
app.add_graphObject(point0)
app.add_graphObject(point1)

animations = Animation.multiple(point0, 5, EaseType.QUADRATIC_OUT, **{
    "drawable.parameter": 10,
    "style.color": (0,0,255),
    "style.radius_px": 10,
    "style.label_style.color": (0,0,255),
    "style.label_style.font_size": 50
})

app.add_animations(animations)
animations2 = Animation.multiple(point1, 5, EaseType.QUADRATIC_IN, **{
    "drawable.parameter": 10,
    "style.color": (0,0,255),
    "style.radius_px": 10,
    "style.label_style.color": (0,0,255),
    "style.label_style.font_size": 50
})

app.add_animations(animations2)
app.run()