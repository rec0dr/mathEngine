import pygame
import math

from .viewport import Viewport
from functions.function import Function, Constant
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

    def draw_line(self, x1, y1, x2, y2, style: LineStyle = LineStyle()):
        p1 = self.viewport.graph_to_screen(x1, y1)
        p2 = self.viewport.graph_to_screen(x2, y2)

        if style.visible:
            pygame.draw.line(self.overlay, (*style.color, style.opacity), p1, p2, style.thickness)
    
    def draw_axes(self, style: LineStyle = LineStyle()):
        self.boundL, self.boundU = self.viewport.screen_to_graph(0, 0)
        self.boundR, self.boundD = self.viewport.screen_to_graph(self.viewport.width, self.viewport.height)

        self.draw_line(self.boundL, 0, self.boundR, 0, style)
        self.draw_line(0, self.boundD, 0, self.boundU, style)
    
    def draw_function(self, func, style: LineStyle = LineStyle(), graphAccuracy=0.01):
        if isinstance(func, (int, float)):
            func = Constant(func)
        self.boundL, self.boundU = self.viewport.screen_to_graph(0, 0)
        self.boundR, self.boundD = self.viewport.screen_to_graph(self.viewport.width, self.viewport.height)

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
