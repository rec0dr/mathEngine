import pygame
from graphing.app import GraphApp
from functions.__init__ import *
from styles.func_style import FuncStyle
from graphing.graph_object import GraphObject

width, height = (800,800)
app = GraphApp(width, height, 100)
app.graphFunctions = [
    GraphObject(Parametric(2*SIN, COS), color=T_BLUE),
    GraphObject(X**3, color=T_PINK)
]

app.run()