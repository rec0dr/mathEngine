import pygame
from functions.__init__ import *
from styles.__init__ import *
from objects.__init__ import *
from graphing.__init__ import *

width, height = (800,800)
scaleX, scaleY = (10,10)
app = GraphApp(width, height, scaleX, scaleY, fps=60, sensitivity=100)

func1 = Parametric((X**2) * COS, (X**3) * SIN)
app.add_graphObject(GraphObject(func1, color=BLUE))
app.add_animatedPoint(AnimatedPoint(func1, 0, PI/2))

app.run()
