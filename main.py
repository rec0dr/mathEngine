import pygame
from functions.__init__ import *
from styles.__init__ import *
from objects.__init__ import *
from graphing.__init__ import *

width, height = (1200, 1200)
scaleX, scaleY = (10,10)
app = GraphApp(width, height, scaleX, scaleY, fps=60, sensitivity=100)

func1 = Parametric(SIN*X, COS*X)
app.add_graphObject(GraphObject(func1, color=RED, tMin=0, tMax=10*PI))
app.add_animatedPoint(AnimatedPoint(func1, 0, PI/2))
app.run()