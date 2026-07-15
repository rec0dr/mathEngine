import pygame
import math

from .viewport import Viewport
from functions.curve import Curve
from functions.function import Function, Constant
from functions.parametric import Parametric
from objects.point import Point
from objects.line_segment import LineSegment
from styles.style import Style
from styles.curve_style import CurveStyle
from styles.point_style import PointStyle
from .graph_object import GraphObject

class Renderer:
    def __init__(self, screen, viewport):
        self.tick_font = pygame.font.SysFont(None, 25)
        self.tick_font2 = pygame.font.SysFont(None, 18)
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

    def draw_line(self, x1, y1, x2, y2, style: CurveStyle = CurveStyle()):
        p1 = self.viewport.graph_to_screen(x1, y1)
        p2 = self.viewport.graph_to_screen(x2, y2)

        if style.visible:
            pygame.draw.line(self.overlay, (*style.color, style.opacity), p1, p2, style.thickness)
    
    def draw_axes(self, style: CurveStyle = CurveStyle()):
        self.update_bounds()

        self.draw_line(self.boundL, 0, self.boundR, 0, style)
        self.draw_line(0, self.boundD, 0, self.boundU, style)
    
    def draw_tick_text(self, x, y):
        # print(self.tick_font)
        text = self.tick_font.render(f"{x:g}", True, (255,255,255))

        text_rect = text.get_rect()
        screen_x, screen_y = self.viewport.graph_to_screen(x, y)

        text_rect.centerx = screen_x

        self.screen.blit(text, text_rect)
    
    def draw_ticks(self, style=None):
        self.update_bounds()
        factorX = 10
        factorY = 10
        amtX = math.log(self.viewport.scale_x, factorX)
        major_distX = factorX**(math.floor(amtX))
        minor_distX = major_distX / factorX
        major_heightX = major_distX / 5
        minor_heightX = major_heightX / 4

        amtY = math.log(self.viewport.scale_y, factorY)
        major_distY = factorY**(math.floor(amtY))
        minor_distY = major_distY / factorY
        major_heightY = major_distY / 5
        minor_heightY = major_heightY / 4

        major_heightX = min(major_heightX, major_heightY)
        major_heightY = major_heightX
        minor_heightX = min(minor_heightX, minor_heightY)
        minor_heightY = minor_heightX

        first = math.floor(self.boundL / minor_distX)
        last = math.ceil(self.boundR / minor_distX)

        ppu_x = self.viewport.ppu_x
        ppu_y = self.viewport.ppu_y

        minor_visibilityX = (amtX <= math.floor(amtX) + 0.5)
        minor_visibilityY = (amtY <= math.floor(amtY) + 0.5)

        for i in range(first, last + 1):
            x = i * minor_distX
            if i == 0:
                continue
            if i % factorX == 0:
                self.draw_line(x, major_heightX, x, -major_heightX)
                
                text = self.tick_font.render(f"{x:g}", True, (255,255,255))

                text_rect = text.get_rect()
                screen_x, screen_y = self.viewport.graph_to_screen(x, 0)

                text_rect.centerx = screen_x
                text_rect.top = screen_y + (ppu_y * major_heightX * 1.1)

                self.screen.blit(text, text_rect)
            elif minor_visibilityX:
                self.draw_line(x, minor_heightX, x, -minor_heightX)

                text = self.tick_font2.render(f"{x:g}", True, (255,255,255))

                text_rect = text.get_rect()
                screen_x, screen_y = self.viewport.graph_to_screen(x, 0)

                text_rect.centerx = screen_x
                text_rect.top = screen_y + (ppu_y * minor_heightX * 1.1)

                self.screen.blit(text, text_rect)
        
        first = math.floor(self.boundD / minor_distY)
        last = math.ceil(self.boundU / minor_distY)

        for i in range(first, last + 1):
            y = i * minor_distY

            if i == 0:
                continue

            if i % factorY == 0:
                self.draw_line(major_heightY, y, -major_heightY, y)
                text = self.tick_font.render(f"{y:g}", True, (255,255,255))

                text_rect = text.get_rect()
                screen_x, screen_y = self.viewport.graph_to_screen(0, y)

                text_rect.centery = screen_y
                text_rect.right = screen_x - (ppu_x * major_heightY * 1.1)

                self.screen.blit(text, text_rect)

            elif minor_visibilityY:
                self.draw_line(minor_heightY, y, -minor_heightY, y)
                text = self.tick_font2.render(f"{y:g}", True, (255,255,255))

                text_rect = text.get_rect()
                screen_x, screen_y = self.viewport.graph_to_screen(0, y)

                text_rect.centery = screen_y
                text_rect.right = screen_x - (ppu_x * minor_heightY * 1.1)

                self.screen.blit(text, text_rect)
            

    
    def draw_graph(self, graph: GraphObject, graphAccuracy=None):
        func = graph.drawable
        style = graph.style

        if isinstance(func, Curve):
            self.draw_curve(func, style)
        elif isinstance(func, Point):
            self.draw_point(func, style)
        
    def draw_point(self, point: Point, style: PointStyle = PointStyle()):
        x, y = self.viewport.graph_to_screen(point.x, point.y)
        if style.is_solid:
            style.border_widthPX = 0
        if style.visible:
            pygame.draw.circle(self.overlay, (*style.color, style.opacity), (x, y), style.radiusPX, style.border_widthPX)
        if style.labeled:
            text = self.tick_font2.render(f"({point.x:.3}, {point.y:.3})", True, (255,255,255))
            text_rect = text.get_rect()
            screen_y = y - style.radiusPX
            text_rect.centerx = x
            text_rect.bottom = screen_y

            self.screen.blit(text, text_rect)

    def draw_curve(self, curve: Curve, style: CurveStyle = CurveStyle(), graphAccuracy=None):
        self.update_bounds()
        if graphAccuracy is None:
            min_parameter, max_parameter = curve.parameter_interval(self)
            graphAccuracy = (max_parameter - min_parameter) / 1000

        t = min_parameter
        x1, y1 = curve.point(t)
        while t <= max_parameter:
            x2, y2 = curve.point(t + graphAccuracy)
            
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

