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
from styles.axis_style import AxisStyle
from styles.text_style import TextStyle
from styles.axis_label import AxisLabel
from .graph_object import GraphObject

class Renderer:
    def __init__(self, screen, viewport):
        self.screen = screen
        self.viewport = viewport
        self.boundL, self.boundU = self.viewport.screen_to_graph(0, 0)
        self.boundR, self.boundD = self.viewport.screen_to_graph(self.viewport.width, self.viewport.height)
        self.overlay = pygame.Surface(screen.get_size(), pygame.SRCALPHA)

        self.tick_font = pygame.font.SysFont(None, self.viewport.ui_scale(18))
        self.tick_font2 = pygame.font.SysFont(None, self.viewport.ui_scale(15))

        # Defaults
        self.default_CurveStyle = CurveStyle((255,255,255), 255, True, 2)
        self.default_PointStyle = PointStyle((255,0,0), 255, True, True)
        self.default_AxisLabelX = AxisLabel("x", TextStyle((0,0,255), font_size=self.viewport.ui_scale(18)))
        self.default_AxisLabelY = AxisLabel("y", TextStyle((255,0,0), font_size=self.viewport.ui_scale(18)))
        self.default_AxisStyle = AxisStyle((255,255,255), origin_radius=self.viewport.ui_scale(5), arrow_dims=(self.viewport.ui_scale(25), self.viewport.ui_scale(10)), label_negatives=True, label_x = self.default_AxisLabelX, label_y = self.default_AxisLabelY)
        self.default_PointTextStyle = TextStyle((255,255,255), font_size=self.viewport.ui_scale(15), italic=True)
        self.default_UITextStyle = TextStyle((255,0,0), font_size=self.viewport.ui_scale(18), bold=True)

    def clear(self):
        self.screen.fill((0,0,0))
        self.overlay.fill((0,0,0,0))

    def update_bounds(self):
        self.boundL, self.boundU = self.viewport.screen_to_graph(0, 0)
        self.boundR, self.boundD = self.viewport.screen_to_graph(self.viewport.width, self.viewport.height)

    def draw_line(self, x1, y1, x2, y2, style):
        p1 = self.viewport.graph_to_screen(x1, y1)
        p2 = self.viewport.graph_to_screen(x2, y2)

        if style.visible:
            pygame.draw.line(self.overlay, (*style.color, style.opacity), p1, p2, style.thickness)
    
    def draw_line_px(self, x1, y1, x2, y2, style):
        if style.visible:
            pygame.draw.line(self.overlay, (*style.color, style.opacity), (x1, y1), (x2,y2), style.thickness)
    
    def draw_text_px(self, x=None, y=None, txt="", style: TextStyle = None, xLeft=None, xRight=None, yBot=None, yTop=None):
        if style is None:
            style = TextStyle((255,255,255), font_size=self.viewport.ui_scale(15))
        if style.visible:
            font = pygame.font.SysFont(style.font_type, style.font_size, style.bold, style.italic)
            text = font.render(txt, True, (*style.color, style.opacity))

            text_rect = text.get_rect()
            if xLeft is not None:
                text_rect.left = xLeft
            if xRight is not None:
                text_rect.right = xRight
            if yBot is not None:
                text_rect.bottom = yBot
            if yTop is not None:
                text_rect.top = yTop
            if x is not None:
                text_rect.centerx = x
            if y is not None:
                text_rect.centery = y
            
            self.screen.blit(text, text_rect)


    
    def draw_axes(self, style: AxisStyle = None):
        if style is None:
            style = self.default_AxisStyle
        self.update_bounds()

        offset_l, offset_w = self.viewport.ui_scale(30), self.viewport.ui_scale(10)

        if style.draw_x:
            self.draw_line(self.boundL, 0, self.boundR, 0, style)
            if style.label_x.text != "":
                x,y = self.viewport.graph_to_screen(self.boundR, 0)
                self.draw_text_px(x-offset_w, y+offset_l, style.label_x.text, style.label_x.style)
                if style.label_negatives:
                    x,y = self.viewport.graph_to_screen(self.boundL, 0)
                    self.draw_text_px(x+offset_w, y+offset_l, style.label_x.text, style.label_x.style)

        if style.draw_y:
            self.draw_line(0, self.boundD, 0, self.boundU, style)
            if style.label_y.text != "":
                x,y = self.viewport.graph_to_screen(0, self.boundU)
                self.draw_text_px(x+offset_l, y+offset_w, style.label_y.text, style.label_y.style)
                if style.label_negatives:
                    x,y = self.viewport.graph_to_screen(0, self.boundD)
                    self.draw_text_px(x+offset_l, y-offset_w, style.label_y.text, style.label_y.style)
        
        if style.show_origin:
            pygame.draw.circle(self.overlay, (255,255,255,255), (self.viewport.graph_to_screen(0,0)), style.origin_radius)
        
        if style.show_arrows:
            x,y = self.viewport.graph_to_screen(self.boundR, 0)
            l,w = style.arrow_dims
            self.draw_line_px(x-w,y-l,x,y,style)
            self.draw_line_px(x,y,x-w,y+l,style)

            x,y = self.viewport.graph_to_screen(self.boundL, 0)
            self.draw_line_px(x+w,y-l,x,y,style)
            self.draw_line_px(x,y,x+w,y+l,style)

            x,y = self.viewport.graph_to_screen(0, self.boundU)
            self.draw_line_px(x-l,y+w,x,y,style)
            self.draw_line_px(x,y,x+l,y+w,style)

            x,y = self.viewport.graph_to_screen(0, self.boundD)
            self.draw_line_px(x-l,y-w,x,y,style)
            self.draw_line_px(x,y,x+l,y-w,style)
        
    
    def draw_ticks(self, style: AxisStyle = None):
        if style is None:
            style = self.default_AxisStyle
        self.update_bounds()
        factorX = 10
        factorY = 10
        amtX = math.log(self.viewport.scale_x, factorX)
        major_distX = factorX**(math.floor(amtX))
        minor_distX = major_distX / factorX
        major_heightX = major_distX / 10
        minor_heightX = major_heightX / factorX

        amtY = math.log(self.viewport.scale_y, factorY)
        major_distY = factorY**(math.floor(amtY))
        minor_distY = major_distY / factorY
        major_heightY = major_distY / 10
        minor_heightY = major_heightY / factorY

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
                self.draw_line(x, major_heightX, x, -major_heightX, style)
                
                text = self.tick_font.render(f"{x:g}", True, (255,255,255))

                text_rect = text.get_rect()
                screen_x, screen_y = self.viewport.graph_to_screen(x, 0)

                text_rect.centerx = screen_x
                text_rect.top = screen_y + (ppu_y * major_heightX * 1.1)

                self.screen.blit(text, text_rect)
            elif minor_visibilityX:
                self.draw_line(x, minor_heightX, x, -minor_heightX, style)

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
                self.draw_line(major_heightY, y, -major_heightY, y, style)
                text = self.tick_font.render(f"{y:g}", True, (255,255,255))

                text_rect = text.get_rect()
                screen_x, screen_y = self.viewport.graph_to_screen(0, y)

                text_rect.centery = screen_y
                text_rect.right = screen_x - (ppu_x * major_heightY * 1.1)

                self.screen.blit(text, text_rect)

            elif minor_visibilityY:
                self.draw_line(minor_heightY, y, -minor_heightY, y, style)
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
        
    def draw_point(self, point: Point, style: PointStyle = None):
        if style is None:
            style = self.default_PointStyle
        x, y = self.viewport.graph_to_screen(point.x, point.y)
        if style.is_solid:
            style.border_width_px = 0
        if style.visible:
            pygame.draw.circle(self.overlay, (*style.color, style.opacity), (x, y), style.radius_px, style.border_width_px)
        if style.labeled:
            if style.label_text_style is None:
                style.label_text_style = self.default_PointTextStyle
            font = pygame.font.SysFont(style.label_text_style.font_type, style.label_text_style.font_size, style.label_text_style.bold, style.label_text_style.italic)
            text = font.render(f"({point.x:.3}, {point.y:.3})", True, (*style.label_text_style.color, style.label_text_style.opacity))
            text_rect = text.get_rect()
            screen_y = y - style.radius_px
            text_rect.centerx = x
            text_rect.bottom = screen_y

            self.screen.blit(text, text_rect)

    def draw_curve(self, curve: Curve, style: CurveStyle = None, graphAccuracy=None):
        if style is None:
            style = self.default_CurveStyle
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
    
    def draw_overlay(self, style: TextStyle = None):
        if style is None:
            style = self.default_UITextStyle
        firstY = self.viewport.ui_scale(20)
        oneLine = style.font_size
        self.draw_text_px(xLeft=self.viewport.ui_scale(20), y=firstY, txt=f"Scale: ({self.viewport.scale_x:g}, {self.viewport.scale_y:g})", style=style)
        self.draw_text_px(xLeft=self.viewport.ui_scale(20), y=firstY + oneLine, txt=f"Center: ({self.viewport.screen_to_graph(self.viewport.width/2, self.viewport.height/2)[0]:g}, {self.viewport.screen_to_graph(self.viewport.width/2, self.viewport.height/2)[1]:g})", style=style)

