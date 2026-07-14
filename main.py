import pygame
from graphing.app import GraphApp
from functions.__init__ import *
from styles.func_style import FuncStyle
from graphing.graph_object import GraphObject

width, height = (800,800)
scaleX, scaleY = (10,10)
app = GraphApp(width, height, scaleX, scaleY, fps=120, sensitivity=100)

func1 = Parametric(SIN, COS)

app.add_graphObject(GraphObject(func1, color=PINK))
app.add_animatedPoint(AnimatedPoint(func1, 0, 2*PI))

app.run()
