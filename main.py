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


point0 = GraphObject(Point((3,5)), style=PointStyle(labeled=True, label_style=TextStyle(font_size=25, color=(255,0,0))))
app.add_graphObject(point0)

animations = Animation.multiple(point0, 5, EaseType.SIN_SMOOTH, **{
    "drawable.x": -3,
    "drawable.y": 2,
    "style.color": (0,0,255),
    "style.radius_px": 10,
    "style.label_style.color": (0,0,255),
    "style.label_style.font_size": 50
})
app.add_animations(animations)
app.run()