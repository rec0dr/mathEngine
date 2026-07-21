import pygame
import math

from .viewport import Viewport
from functions.curve import Curve
from functions.function import Function, Value
from functions.parametric import Parametric
from objects.point import Point
from objects.line_segment import LineSegment
from objects.label import Label
from styles.style import Style
from styles.curve_style import CurveStyle
from styles.point_style import PointStyle
from styles.axis_style import AxisStyle
from styles.text_style import TextStyle
from styles.tick_style import TickStyle
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
        self.default_BackgroundColor = (0,0,0)
        self.default_CurveStyle = CurveStyle((255,255,255), 255, True, 2)
        self.default_PointStyle = PointStyle((255,0,0), 255, True, True)
        self.default_AxisLabelX = AxisLabel("x", TextStyle((0,0,255), font_size=self.viewport.ui_scale(18)))
        self.default_AxisLabelY = AxisLabel("y", TextStyle((255,0,0), font_size=self.viewport.ui_scale(18)))
        self.default_AxisStyle = AxisStyle((255,255,255), origin_radius=self.viewport.ui_scale(5), arrow_dims=(self.viewport.ui_scale(25), self.viewport.ui_scale(10)), label_negatives=True, label_x = self.default_AxisLabelX, label_y = self.default_AxisLabelY)
        self.default_PointTextStyle = TextStyle((255,255,255), font_size=self.viewport.ui_scale(15), italic=True)
        self.default_UITextStyle = TextStyle((255,0,0), font_size=self.viewport.ui_scale(18), bold=True)
        self.default_MajorTickStyle = TickStyle((255,255,255), 255, True, 10, 10, 1, 1, 4, True, TextStyle((255,255,255), font_size=self.viewport.ui_scale(16)))
        self.default_MinorTickStyle = TickStyle((255,255,255), 128, True, 10, 10, 0.1, 0.1, 2, False, TextStyle((255,255,255), font_size=self.viewport.ui_scale(13)))

    def clear(self):
        self.screen.fill(self.default_BackgroundColor)
        self.overlay.fill((*self.default_BackgroundColor, 0))

    def update_bounds(self):
        self.boundL, self.boundU = self.viewport.screen_to_graph(0, 0)
        self.boundR, self.boundD = self.viewport.screen_to_graph(self.viewport.width, self.viewport.height)

    def draw_line(self, x1, y1, x2, y2, style):
        p1 = self.viewport.graph_to_screen(x1, y1)
        p2 = self.viewport.graph_to_screen(x2, y2)

        if style.visible:
            pygame.draw.line(self.overlay, (*style.color, style.opacity), p1, p2, int(style.thickness))
    
    def rotate(self, vx, vy, angle):
        c = math.cos(angle)
        s = math.sin(angle)
        return (
            vx * c - vy * s,
            vx * s + vy * c
        )
        
    def draw_line_px(self, x1, y1, x2, y2, style):
        if style.visible:
            pygame.draw.line(self.overlay, (*style.color, style.opacity), (x1, y1), (x2,y2), style.thickness)
    
    def draw_text_px(self, x=None, y=None, txt="", style: TextStyle = None, xLeft=None, xRight=None, yBot=None, yTop=None):
        if style is None:
            style = TextStyle((255,255,255), font_size=self.viewport.ui_scale(15))
        if style.visible:
            actual_font_size = style.font_size
            if style.fixed_zoom:
                actual_font_size = style.font_size / max(self.viewport.scale_x, self.viewport.scale_y) * style.base_scale
            actual_font_size = int(actual_font_size)
            font = pygame.font.SysFont(style.font_type, actual_font_size, style.bold, style.italic)
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
    
    def draw_arrowhead(self, tip_x, tip_y, dx, dy, width, length, style):
        mag = math.hypot(dx, dy)
        if mag == 0:
            return

        dx /= mag
        dy /= mag

        px = -dy
        py = dx

        base_x = tip_x - length * dx
        base_y = tip_y - length * dy

        left_x = base_x + (width / 2) * px
        left_y = base_y + (width / 2) * py

        right_x = base_x - (width / 2) * px
        right_y = base_y - (width / 2) * py

        self.draw_line(tip_x, tip_y, left_x, left_y, style)
        self.draw_line(tip_x, tip_y, right_x, right_y, style)
    
    def draw_ticks(self, style: TickStyle = None, style2: TickStyle = None):
        if style is None:
            style = self.default_MajorTickStyle
        if style2 is None:
            style2 = self.default_MinorTickStyle
        
        major_height_px = 32
        minor_height_px = 8

        self.update_bounds()
        major_factorX = style.factor_x
        major_factorY = style.factor_y
        major_amtX = math.log(self.viewport.scale_x, major_factorX)
        major_distX = major_factorX**(math.floor(major_amtX)) * style.base_dist0x
        major_amtY = math.log(self.viewport.scale_y, major_factorY)
        major_distY = major_factorY**(math.floor(major_amtY)) * style.base_dist0y
        major_heightX = major_height_px / self.viewport.ppu_x
        major_heightY = major_height_px / self.viewport.ppu_x

        # For now, minor ticks are determined by same factor as major, possible custom later?

        minor_factorX = style.factor_x
        minor_factorY = style.factor_y
        minor_amtX = math.log(self.viewport.scale_x, minor_factorX)
        minor_distX = minor_factorX**(math.floor(minor_amtX)) * style2.base_dist0x
        minor_amtY = math.log(self.viewport.scale_y, minor_factorY)
        minor_distY = minor_factorY**(math.floor(minor_amtY)) * style2.base_dist0y
        minor_heightX = minor_height_px / self.viewport.ppu_x
        minor_heightY = minor_height_px / self.viewport.ppu_x



        ppu_x = self.viewport.ppu_x
        ppu_y = self.viewport.ppu_y

        fractionX = minor_amtX - math.floor(minor_amtX)
        alpha_minorX = int(128 * (1 - fractionX)) + 127
        alpha_majorX = 255 - alpha_minorX + 127

        fractionY = minor_amtY - math.floor(minor_amtY)
        alpha_minorY = int(128 * (1 - fractionY)) + 127
        alpha_majorY = 255 - alpha_minorY + 127

        if style.visible or style2.visible:
            first = math.floor(self.boundL / minor_distX)
            last = math.ceil(self.boundR / minor_distX)
            every = round(major_distX / minor_distX)

            for i in range(first, last + 1):
                x = i * minor_distX
                x = round(x, 10)
                if i == 0:
                    continue
                if i % every == 0:
                    if style.visible:
                        self.draw_line(x, major_heightX, x, -major_heightX, CurveStyle(color=(style.color),opacity=style.opacity, thickness=style.thickness))

                        if style.labeled:
                            screen_x, screen_y = self.viewport.graph_to_screen(x, 0)
                            self.draw_text_px(x=screen_x, yTop = screen_y + (ppu_y * major_heightX * 1.1), txt=f"{x:g}", style=style.label_style)
                    
                else:
                    if style2.visible:
                        self.draw_line(x, minor_heightX, x, -minor_heightX, CurveStyle(color=(style2.color),opacity=style2.opacity, thickness=style2.thickness))

                        if style2.labeled:
                            screen_x, screen_y = self.viewport.graph_to_screen(x, 0)
                            self.draw_text_px(x=screen_x, yTop = screen_y + (ppu_y * minor_heightX * 1.1), txt=f"{x:g}", style=style2.label_style)
        
            first = math.floor(self.boundD / minor_distY)
            last = math.ceil(self.boundU / minor_distY)
            every = round(major_distY / minor_distY)

            for i in range(first, last + 1):
                y = i * minor_distY

                if i == 0:
                    continue

                if i % every == 0:
                    if style.visible:
                        self.draw_line(major_heightY, y, -major_heightY, y, CurveStyle(color=(style.color),opacity=style.opacity, thickness=style.thickness))

                        if style.labeled:
                            screen_x, screen_y = self.viewport.graph_to_screen(0, y)
                            self.draw_text_px(xRight=screen_x - (ppu_x * major_heightY * 1.1), y = screen_y, txt=f"{y:g}", style=style.label_style)

                else:
                    if style2.visible:
                        self.draw_line(minor_heightY, y, -minor_heightY, y, CurveStyle(color=(style2.color),opacity=style2.opacity, thickness=style2.thickness))

                        if style2.labeled:
                            screen_x, screen_y = self.viewport.graph_to_screen(0, y)
                            self.draw_text_px(xRight=screen_x - (ppu_x * minor_heightY * 1.1), y = screen_y, txt=f"{y:g}", style=style2.label_style)
            

    
    def draw_graph(self, graph: GraphObject, graphAccuracy=None):
        func = graph.drawable
        style = graph.style

        if isinstance(func, Curve):
            self.draw_curve(func, style)
        elif isinstance(func, Point):
            self.draw_point(func, style)
        elif isinstance(func, Label):
            self.draw_label(func, style)
    
    def draw_label(self, label: Label, label_style: TextStyle = None):
        if label_style is None:
            label_style = self.default_PointTextStyle
        
        x_PX, y_PX = self.viewport.graph_to_screen(label.x, label.y)
        self.draw_text_px(x_PX, y_PX, txt=label.text, style=label_style)
        
    def draw_point(self, point: Point, style: PointStyle = None):
        if style is None:
            style = self.default_PointStyle
        x, y = self.viewport.graph_to_screen(point.x, point.y)
        if style.is_solid:
            style.border_width_px = 0
        if style.visible:
            pygame.draw.circle(self.overlay, (*style.color, style.opacity), (x, y), style.radius_px, style.border_width_px)
        if style.labeled:
            if style.label_style is None:
                style.label_style = self.default_PointTextStyle
            
            self.draw_text_px(x = x, yBot = y, txt = f"({point.x:g}, {point.y:g})", style = style.label_style)

    def draw_curve(self, curve: Curve, style: CurveStyle = None, graphAccuracy=None):
        if style is None:
            style = self.default_CurveStyle
        self.update_bounds()
        if graphAccuracy is None:
            min_parameter, max_parameter = curve.parameter_interval(self)
            graphAccuracy = (max_parameter - min_parameter) / 1000

        t = min_parameter
        x1, y1 = curve.point(t)

        first_visible = None
        last_visible = None

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
                if first_visible is None:
                    first_visible = ((x1, y1), (x2, y2))
                
                self.draw_line(x1, y1, x2, y2, style)
                last_visible = ((x1, y1), (x2, y2))
                x1, y1 = x2, y2
                t += graphAccuracy
        
        if style.show_arrows:
            width_px, length_px = style.arrow_dims
            width = width_px / self.viewport.ppu_x
            length = length_px / self.viewport.ppu_y

            if last_visible is not None:

                (x1, y1), (x2, y2) = last_visible
                dx = x2 - x1
                dy = y2 - y1

                self.draw_arrowhead(x2, y2, dx, dy, width, length, style)

            if first_visible is not None:

                (x1, y1), (x2, y2) = first_visible
                dx = x1 - x2
                dy = y1 - y2

                self.draw_arrowhead(x1, y1, dx, dy, width, length, style)


            


            

    
    def draw_overlay(self, app = None, style: TextStyle = None):
        if style is None:
            style = self.default_UITextStyle
        firstY = self.viewport.ui_scale(20)
        oneLine = style.font_size
        self.draw_text_px(xLeft=self.viewport.ui_scale(20), y=firstY, txt=f"Scale: ({self.viewport.scale_x:g}, {self.viewport.scale_y:g})", style=style)
        self.draw_text_px(xLeft=self.viewport.ui_scale(20), y=firstY + oneLine, txt=f"Center: ({self.viewport.screen_to_graph(self.viewport.width/2, self.viewport.height/2)[0]:g}, {self.viewport.screen_to_graph(self.viewport.width/2, self.viewport.height/2)[1]:g})", style=style)
        self.draw_text_px(xLeft=self.viewport.ui_scale(20), y=firstY + 2 * oneLine, txt=f"Move Speed: {app.slide_multi:g}", style=style)

