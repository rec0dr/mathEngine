import pygame
from graphing.app import GraphApp
from functions.__init__ import Exponential, LinEq, Logarithm, Polynomial, Sinusoid, TrigType
from functions.parametric import Parametric
from functions.symbols import X
from styles.line_style import LineStyle

width, height = (800,800)
app = GraphApp(width, height, 100)
app.functions = [
    X
]

app.run()