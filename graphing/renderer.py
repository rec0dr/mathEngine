import pygame
import math

from .viewport import Viewport
from functions.function import Function, Constant
from functions.parametric import Parametric
from objects.point import Point
from styles.style import Style
from styles.func_style import FuncStyle
from styles.point_style import PointStyle
from styles.parametric_style import ParametricStyle
from .graph_object import GraphObject

class Renderer:
    def __init__(self, screen, viewport):
        self.screen = screen
        self.viewport = viewport
        self.boundL, self.boundU = self.viewport.screen_to_graph(0, 0)
        self.boundR, self.boundD = self.viewport.screen_to_graph(self.viewport.width, self.viewport.height)
        self.overlay = pygame.Surface(screen.get_size(), pygame.SRCALPHA)

    def clear(self):
        self.screen.fill((0,0,0))
        self.overlay.fill((0,0,0,0))

    def update_bounds(self):
        self.boundL, self.boundU = self.viewport.screen_to_graph(0, 0)
        self.boundR, self.boundD = self.viewport.screen_to_graph(self.viewport.width, self.viewport.height)

    def draw_line(self, x1, y1, x2, y2, style: FuncStyle = FuncStyle()):
        p1 = self.viewport.graph_to_screen(x1, y1)
        p2 = self.viewport.graph_to_screen(x2, y2)

        if style.visible:
            pygame.draw.line(self.overlay, (*style.color, style.opacity), p1, p2, style.thickness)
    
    def draw_axes(self, style: FuncStyle = FuncStyle()):
        self.update_bounds()

        self.draw_line(self.boundL, 0, self.boundR, 0, style)
        self.draw_line(0, self.boundD, 0, self.boundU, style)
    
    def draw_graph(self, graph: GraphObject, graphAccuracy=None):
        func = graph.obj
        style = graph.style

        if isinstance(func, Function):
            self.draw_explicit(func, style, graphAccuracy)
        elif isinstance(func, (float, int)):
            func = Constant(func)
            self.draw_explicit(func, style, graphAccuracy)
        elif isinstance(func, Parametric):
            self.draw_parametric(func, style, graphAccuracy)
        elif isinstance(func, Point):
            self.draw_point(func, style)
        
    def draw_point(self, point: Point, style: PointStyle = PointStyle()):
        x, y = self.viewport.graph_to_screen(point.x, point.y)
        if style.is_solid:
            style.border_widthPX = 0
        if style.visible:
            pygame.draw.circle(self.overlay, (*style.color, style.opacity), (x, y), style.radiusPX, style.border_widthPX)
    
    def draw_explicit(self, func: Function, style: FuncStyle = FuncStyle(), graphAccuracy=None):
        if graphAccuracy is None:
            graphAccuracy = 0.001*self.viewport.scale_x
        self.update_bounds()

        x1 = self.boundL
        while x1 < self.boundR:
            x2 = x1 + graphAccuracy
            y1 = func.evaluate(x1)
            y2 = func.evaluate(x2)
            
            if y1 is None or y2 is None:
                x1 += graphAccuracy
                continue
            elif y1 > self.boundU or y1 < self.boundD:
                x1 += graphAccuracy
                continue
            else:
                self.draw_line(x1, y1, x2, y2, style)
                x1 += graphAccuracy

    def draw_parametric(self, parametric: Parametric, style: ParametricStyle = ParametricStyle(), graphAccuracy=None):
        if graphAccuracy is None:
            graphAccuracy = (style.tMax - style.tMin) / 1000
        self.update_bounds()

        t = style.tMin
        x1, y1 = parametric.evaluate(t)
        while t <= style.tMax:
            x2, y2 = parametric.evaluate(t + graphAccuracy)
            
            if y1 is None or y2 is None:
                x1, y1 = x2, y2
                t += graphAccuracy
                continue
            elif (
                    (x1 < self.boundL and x2 < self.boundL) or
                    (x1 > self.boundR and x2 > self.boundR) or
                    (y1 < self.boundD and y2 < self.boundD) or
                    (y1 > self.boundU and y2 > self.boundU)
                ):
                x1, y1 = x2, y2
                t += graphAccuracy
                continue
            else:
                self.draw_line(x1, y1, x2, y2, style)
                x1, y1 = x2, y2
                t += graphAccuracy

