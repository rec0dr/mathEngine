import pygame
import math

from .viewport import Viewport
from functions.function import Function, Constant
from functions.parametric import Parametric
from styles.style import Style
from styles.line_style import LineStyle

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

    def draw_line(self, x1, y1, x2, y2, style: LineStyle = LineStyle()):
        p1 = self.viewport.graph_to_screen(x1, y1)
        p2 = self.viewport.graph_to_screen(x2, y2)

        if style.visible:
            pygame.draw.line(self.overlay, (*style.color, style.opacity), p1, p2, style.thickness)
    
    def draw_axes(self, style: LineStyle = LineStyle()):
        self.update_bounds()

        self.draw_line(self.boundL, 0, self.boundR, 0, style)
        self.draw_line(0, self.boundD, 0, self.boundU, style)
    
    def draw_function(self, func: Function, style: LineStyle = LineStyle(), graphAccuracy=None):
        if graphAccuracy is None:
            graphAccuracy = self.viewport.scale_x * 1/1000
        if isinstance(func, (int, float)):
            func = Constant(func)
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
    
    def draw_parametric(self, parametric: Parametric, style: LineStyle = LineStyle(), graphAccuracy=None, tMin=0, tMax=2*math.pi):
        if graphAccuracy is None:
            graphAccuracy = self.viewport.scale_x * 1/1000
        self.update_bounds()

        t = tMin
        while t <= tMax:
            x1, y1 = parametric.evaluate(t)
            x2, y2 = parametric.evaluate(t + graphAccuracy)
            
            if y1 is None or y2 is None:
                t += graphAccuracy
                continue
            elif y1 > self.boundU or y1 < self.boundD:
                t += graphAccuracy
                continue
            else:
                self.draw_line(x1, y1, x2, y2, style)
                t += graphAccuracy
