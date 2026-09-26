import pygame
import math

from .viewport import Viewport
from .animation_manager import AnimationManager
from .camera_controller import CameraController
from .graph_manager import GraphManager
from .graph_object import GraphObject
from .registries import DRAW_MAP

from functions.curve import Curve
from functions.function import Function, Value
from functions.parametric import Parametric

from objects.point import Point
from objects.line_segment import LineSegment
from objects.label import Label
from objects.circle import Circle

from styles.style import Style
from styles.axis_label import AxisLabel
from styles.axis_style import AxisStyle
from styles.circle_style import CircleStyle
from styles.curve_style import CurveStyle
from styles.grid_style import GridStyle
from styles.line_segment_style import LineSegmentStyle
from styles.point_style import PointStyle
from styles.text_style import TextStyle
from styles.tick_style import TickStyle

class Renderer:
    def __init__(self, screen: pygame.Surface, viewport: Viewport, graph_manager: GraphManager, animation_manager: AnimationManager, camera_controller: CameraController, fps=60):
        self.screen                     = screen
        self.viewport                   = viewport
        self.graph_manager              = graph_manager
        self.animation_manager          = animation_manager
        self.camera_controller          = camera_controller
        self.boundL, self.boundU        = self.viewport.screen_to_graph(0, 0)
        self.boundR, self.boundD        = self.viewport.screen_to_graph(self.viewport.width, self.viewport.height)
        self.overlay                    = pygame.Surface(screen.get_size(), pygame.SRCALPHA)

        self.tick_font                  = pygame.font.SysFont(None, self.viewport.ui_scale(18))
        self.tick_font2                 = pygame.font.SysFont(None, self.viewport.ui_scale(15))

        self.fps                        = fps
        self.ui_space                   = {"NW": [], "NE": [], "SW": [], "SE": []}

        # Defaults
        self.default_BackgroundColor    = (0,0,0)

        self.default_CurveStyle         = CurveStyle((255,255,255), 255, True, False, "", False, 2)
        self.default_PointStyle         = PointStyle((255,0,0), 255, True, False, "", False, True, 5, 0, True)
        self.default_LineSegmentStyle   = LineSegmentStyle()
        self.default_CircleStyle        = CircleStyle()

        self.default_AxisLabelX         = AxisLabel("x", TextStyle((0,0,255), font_size=self.viewport.ui_scale(18)))
        self.default_AxisLabelY         = AxisLabel("y", TextStyle((255,0,0), font_size=self.viewport.ui_scale(18)))
        self.default_AxisStyle          = AxisStyle((255,255,255), origin_radius=self.viewport.ui_scale(5), arrow_dims=(self.viewport.ui_scale(25), self.viewport.ui_scale(10)), label_negatives=True, label_x = self.default_AxisLabelX, label_y = self.default_AxisLabelY)

        self.default_GridStyle          = GridStyle()

        self.default_PointTextStyle     = TextStyle((0,0,255), font_size=self.viewport.ui_scale(20), italic=True, y_offset = -10)
        self.default_UITextStyle        = TextStyle((255, 255, 255), font_size=self.viewport.ui_scale(18), bold=True)

        self.default_MajorTickStyle     = TickStyle((255,255,255), 255, True, False, "", False, 10, 10, 1, 1, 4, True, TextStyle((255,255,255), font_size=self.viewport.ui_scale(16)))
        self.default_MinorTickStyle     = TickStyle((255,255,255), 128, True, False, "", False, 10, 10, 0.1, 0.1, 2, False, TextStyle((255,255,255), font_size=self.viewport.ui_scale(13)))

    def clear(self):
        """Standard clearing procedure. Clears the screen and fills the overlay in case of custom opacities."""

        self.screen.fill(self.default_BackgroundColor)
        self.overlay.fill((*self.default_BackgroundColor, 0))

    def update_bounds(self):
        """Checks the current camera status to update the camera bounds (grid coords)."""

        self.boundL, self.boundU = self.viewport.screen_to_graph(0, 0)
        self.boundR, self.boundD = self.viewport.screen_to_graph(self.viewport.width, self.viewport.height)

    def draw_line(self, x1, y1, x2, y2, style):
        """Standard procedure for drawing a line (grid coords)."""

        p1 = self.viewport.graph_to_screen(x1, y1)
        p2 = self.viewport.graph_to_screen(x2, y2)

        if style.visible:
            pygame.draw.line(self.overlay, (*style.color, style.opacity), p1, p2, int(style.thickness))
    
    def rotate(self, vx, vy, angle):
        """Uses standard rotation matrix to rotate any point by any angle."""

        c = math.cos(angle)
        s = math.sin(angle)
        return (
            vx * c - vy * s,
            vx * s + vy * c
        )
        
    def draw_line_px(self, x1, y1, x2, y2, style):
        """Standard procedure for drawing a line. (screen px)"""

        if style.visible:
            pygame.draw.line(self.overlay, (*style.color, style.opacity), (x1, y1), (x2,y2), style.thickness)
    
    def draw_text_px(self, x=None, y=None, txt="", text_style: TextStyle = None, xLeft=None, xRight=None, yBot=None, yTop=None):
        
        if text_style is None:
            text_style = TextStyle((255,255,255), font_size=self.viewport.ui_scale(15))
        if text_style.visible:
            actual_font_size = text_style.font_size
            if text_style.fixed_zoom:
                actual_font_size = text_style.font_size / max(self.viewport.scale_x, self.viewport.scale_y) * text_style.base_scale
            actual_font_size = int(actual_font_size)
            font = pygame.font.SysFont(text_style.font_type, actual_font_size, text_style.bold, text_style.italic)
            text = font.render(txt, True, (*text_style.color, text_style.opacity))

            text_rect = text.get_rect()
            if xLeft is not None:
                text_rect.left = xLeft + text_style.x_offset
            if xRight is not None:
                text_rect.right = xRight + text_style.x_offset
            if yBot is not None:
                text_rect.bottom = yBot + text_style.y_offset
            if yTop is not None:
                text_rect.top = yTop + text_style.y_offset
            if x is not None:
                text_rect.centerx = x + text_style.x_offset
            if y is not None:
                text_rect.centery = y + text_style.y_offset
            
            self.screen.blit(text, text_rect)

    def draw_axes(self, axis_style: AxisStyle = None):
        if axis_style is None:
            axis_style = self.default_AxisStyle
        self.update_bounds()

        offset_l, offset_w = self.viewport.ui_scale(30), self.viewport.ui_scale(10)

        if axis_style.draw_x:
            self.draw_line(self.boundL, 0, self.boundR, 0, axis_style)
            if axis_style.label_x.text != "":
                x,y = self.viewport.graph_to_screen(self.boundR, 0)
                self.draw_text_px(x-offset_w, y+offset_l, axis_style.label_x.text, axis_style.label_x.style)
                if axis_style.label_negatives:
                    x,y = self.viewport.graph_to_screen(self.boundL, 0)
                    self.draw_text_px(x+offset_w, y+offset_l, axis_style.label_x.text, axis_style.label_x.style)

        if axis_style.draw_y:
            self.draw_line(0, self.boundD, 0, self.boundU, axis_style)
            if axis_style.label_y.text != "":
                x,y = self.viewport.graph_to_screen(0, self.boundU)
                self.draw_text_px(x+offset_l, y+offset_w, axis_style.label_y.text, axis_style.label_y.style)
                if axis_style.label_negatives:
                    x,y = self.viewport.graph_to_screen(0, self.boundD)
                    self.draw_text_px(x+offset_l, y-offset_w, axis_style.label_y.text, axis_style.label_y.style)
        
        if axis_style.show_origin:
            pygame.draw.circle(self.overlay, (255,255,255,255), (self.viewport.graph_to_screen(0,0)), axis_style.origin_radius)
        
        if axis_style.show_arrows:
            x,y = self.viewport.graph_to_screen(self.boundR, 0)
            l,w = axis_style.arrow_dims
            self.draw_line_px(x-w,y-l,x,y,axis_style)
            self.draw_line_px(x,y,x-w,y+l,axis_style)

            x,y = self.viewport.graph_to_screen(self.boundL, 0)
            self.draw_line_px(x+w,y-l,x,y,axis_style)
            self.draw_line_px(x,y,x+w,y+l,axis_style)

            x,y = self.viewport.graph_to_screen(0, self.boundU)
            self.draw_line_px(x-l,y+w,x,y,axis_style)
            self.draw_line_px(x,y,x+l,y+w,axis_style)

            x,y = self.viewport.graph_to_screen(0, self.boundD)
            self.draw_line_px(x-l,y-w,x,y,axis_style)
            self.draw_line_px(x,y,x+l,y-w,axis_style)
    
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
    
    def draw_grid(self, tick_style: TickStyle = None, tick_style2: TickStyle = None, grid_style: GridStyle = None):
        if tick_style is None:
            tick_style = self.default_MajorTickStyle
        if tick_style2 is None:
            tick_style2 = self.default_MinorTickStyle
        if grid_style is None:
            grid_style = self.default_GridStyle
        
        major_height_px = 32
        minor_height_px = 8

        self.update_bounds()
        major_factorX = tick_style.factor_x
        major_factorY = tick_style.factor_y
        major_amtX = math.log(self.viewport.scale_x, major_factorX)
        major_distX = major_factorX**(math.floor(major_amtX)) * tick_style.base_dist0x
        major_amtY = math.log(self.viewport.scale_y, major_factorY)
        major_distY = major_factorY**(math.floor(major_amtY)) * tick_style.base_dist0y
        major_heightX = major_height_px / self.viewport.ppu_x
        major_heightY = major_height_px / self.viewport.ppu_y

        # For now, minor ticks are determined by same factor as major, possible custom later?

        minor_factorX = tick_style.factor_x
        minor_factorY = tick_style.factor_y
        minor_amtX = math.log(self.viewport.scale_x, minor_factorX)
        minor_distX = minor_factorX**(math.floor(minor_amtX)) * tick_style2.base_dist0x
        minor_amtY = math.log(self.viewport.scale_y, minor_factorY)
        minor_distY = minor_factorY**(math.floor(minor_amtY)) * tick_style2.base_dist0y
        minor_heightX = minor_height_px / self.viewport.ppu_x
        minor_heightY = minor_height_px / self.viewport.ppu_y

        ppu_x = self.viewport.ppu_x
        ppu_y = self.viewport.ppu_y

        fractionX = minor_amtX - math.floor(minor_amtX)
        alpha_minorX = int(128 * (1 - fractionX)) + 127
        alpha_majorX = 255 - alpha_minorX + 127

        fractionY = minor_amtY - math.floor(minor_amtY)
        alpha_minorY = int(128 * (1 - fractionY)) + 127
        alpha_majorY = 255 - alpha_minorY + 127

        if tick_style.visible or tick_style2.visible:
            first = math.floor(self.boundL / minor_distX)
            last = math.ceil(self.boundR / minor_distX)
            every = round(major_distX / minor_distX)

            for i in range(first, last + 1):
                x = i * minor_distX
                
                if i == 0:
                    continue

                if i % every == 0:
                    if tick_style.visible:
                        if grid_style.visible:
                            self.draw_line(x, self.boundD, x, self.boundU, style=CurveStyle(color=(grid_style.color), opacity=grid_style.opacity, thickness=grid_style.thickness))
                        self.draw_line(x, major_heightX, x, -major_heightX, CurveStyle(color=(tick_style.color),opacity=tick_style.opacity, thickness=tick_style.thickness))

                        if tick_style.labeled:
                            screen_x, screen_y = self.viewport.graph_to_screen(x, 0)
                            self.draw_text_px(x = screen_x, yTop = screen_y + (ppu_y * major_heightX * 1.1), txt=f"{x:g}", text_style=tick_style.label_style)
                    
                else:
                    if tick_style2.visible:
                        if grid_style.minor_visible:
                            self.draw_line(x, self.boundD, x, self.boundU, style=CurveStyle(color=(grid_style.minor_color), opacity=grid_style.minor_opacity, thickness=grid_style.minor_thickness))
                        self.draw_line(x, minor_heightX, x, -minor_heightX, CurveStyle(color=(tick_style2.color),opacity=tick_style2.opacity, thickness=tick_style2.thickness))

                        if tick_style2.labeled:
                            screen_x, screen_y = self.viewport.graph_to_screen(x, 0)
                            self.draw_text_px(x = screen_x, yTop = screen_y + (ppu_y * minor_heightX * 1.1), txt=f"{x:g}", text_style=tick_style2.label_style)
        
            first = math.floor(self.boundD / minor_distY)
            last = math.ceil(self.boundU / minor_distY)
            every = round(major_distY / minor_distY)

            for i in range(first, last + 1):
                y = i * minor_distY

                if i == 0:
                    continue

                if i % every == 0:
                    if tick_style.visible:
                        if grid_style.visible:
                            self.draw_line(self.boundL, y, self.boundR, y, style=CurveStyle(color=(grid_style.color), opacity=grid_style.opacity, thickness=grid_style.thickness))
                        self.draw_line(major_heightY, y, -major_heightY, y, CurveStyle(color=(tick_style.color),opacity=tick_style.opacity, thickness=tick_style.thickness))

                        if tick_style.labeled:
                            screen_x, screen_y = self.viewport.graph_to_screen(0, y)
                            self.draw_text_px(xRight=screen_x - (ppu_x * major_heightY * 1.1), y = screen_y, txt=f"{y:g}", text_style=tick_style.label_style)

                else:
                    if tick_style2.visible:
                        if grid_style.minor_visible:
                            self.draw_line(self.boundL, y, self.boundR, y, style=CurveStyle(color=(grid_style.minor_color), opacity=grid_style.minor_opacity, thickness=grid_style.minor_thickness))
                        self.draw_line(minor_heightY, y, -minor_heightY, y, CurveStyle(color=(tick_style2.color),opacity=tick_style2.opacity, thickness=tick_style2.thickness))

                        if tick_style2.labeled:
                            screen_x, screen_y = self.viewport.graph_to_screen(0, y)
                            self.draw_text_px(xRight=screen_x - (ppu_x * minor_heightY * 1.1), y = screen_y, txt=f"{y:g}", text_style=tick_style2.label_style)
            

    
    def draw_graph(self, obj: GraphObject):
        func = obj.drawable
        style = obj.style
        

        for cls in type(func).__mro__:
            if cls in DRAW_MAP:
                drawer_name = DRAW_MAP[cls]
                break
        else:
            raise TypeError(f"No drawer registered for {type(func).__name__}")
        
        drawer = getattr(self, drawer_name)
        drawer(func, style)

    def draw_line_segment(self, line_segment: LineSegment, line_segment_style: LineSegmentStyle = None):
        if line_segment_style is None:
            line_segment_style = self.default_LineSegmentStyle

        x1, y1 = line_segment.pos1
        x2, y2 = line_segment.pos2

        self.draw_line(x1, y1, x2, y2, style=CurveStyle(line_segment_style.color, line_segment_style.opacity, line_segment_style.visible, line_segment_style.thickness))

        if line_segment_style.show_ends:
            if line_segment_style.endpoint_style is None:
                line_segment_style.endpoint_style = self.default_PointStyle
            self.draw_point(Point((x1, y1)), point_style=line_segment_style.endpoint_style)
            self.draw_point(Point((x2, y2)), point_style=line_segment_style.endpoint_style)

        if line_segment_style.label_ends:
            if line_segment_style.label_style is None:
                line_segment_style.label_style = self.default_PointTextStyle
            pos1 = self.viewport.graph_to_screen(x1, y1)
            pos2 = self.viewport.graph_to_screen(x2, y2)
            self.draw_text_px(x=pos1[0], yBot=pos1[1], txt=f"({x1:g}, {y1:g})", text_style=line_segment_style.label_style)
            self.draw_text_px(x=pos2[0], yBot=pos2[1], txt=f"({x2:g}, {y2:g})", text_style=line_segment_style.label_style)


    def draw_circle(self, circle: Circle, circle_style: CircleStyle = None):
        if circle_style is None:
            circle_style = self.default_CircleStyle

        center = self.viewport.graph_to_screen(*circle.center)
        radius_x = self.viewport.ppu_x * circle.radius
        radius_y = self.viewport.ppu_y * circle.radius

        rect = pygame.Rect(0, 0, radius_x * 2, radius_y * 2)
        rect.center = center

        if circle_style.visible:
            pygame.draw.ellipse(self.screen, (*circle_style.color, circle_style.opacity), rect, circle_style.thickness)

            if circle_style.show_center:
                self.draw_point(Point(*circle.center), circle_style.center_style)
    
    def draw_label(self, label: Label, label_style: TextStyle = None):
        if label_style is None:
            label_style = self.default_PointTextStyle

        x_PX, y_PX = self.viewport.graph_to_screen(label.x, label.y)
        self.draw_text_px(x_PX, y_PX, txt=label.text, text_style=label_style)
        
    def draw_point(self, point: Point, point_style: PointStyle = None):
        if point_style is None:
            point_style = self.default_PointStyle
        if point.x is None or point.y is None:
            return
        x, y = self.viewport.graph_to_screen(point.x, point.y)
        if point_style.is_solid:
            point_style.border_width_px = 0
        if point_style.visible:
            pygame.draw.circle(self.overlay, (*point_style.color, point_style.opacity), (x, y), point_style.radius_px, point_style.border_width_px)
        if point_style.labeled:
            if point_style.label_style is None:
                point_style.label_style = self.default_PointTextStyle
            
            self.draw_text_px(x = x, yBot = y - point_style.radius_px, txt = f"({point.x:g}, {point.y:g})", text_style = point_style.label_style)

    def draw_curve(self, curve: Curve, curve_style: CurveStyle = None, graphAccuracy=None):
        if curve_style is None:
            curve_style = self.default_CurveStyle
        self.update_bounds()
        if graphAccuracy is None:
            min_parameter, max_parameter = curve.parameter_interval(self)
            graphAccuracy = (max_parameter - min_parameter) / 1000

        t = min_parameter
        x1, y1 = curve.point(t)

        first_visible = None
        last_visible = None

        jump_threshold = 5 * max(
            self.boundR - self.boundL,
            self.boundU - self.boundD
        )

        while t <= max_parameter:
            x2, y2 = curve.point(t + graphAccuracy)

            if y1 is None or y2 is None:
                x1, y1 = x2, y2
                t += graphAccuracy
                continue
            elif (
                    # Same-side out of bounds
                    (x1 < self.boundL and x2 < self.boundL) or
                    (x1 > self.boundR and x2 > self.boundR) or
                    (y1 < self.boundD and y2 < self.boundD) or
                    (y1 > self.boundU and y2 > self.boundU) or

                    # Crossing entire viewport
                    (x1 < self.boundL and x2 > self.boundR) or
                    (x1 > self.boundR and x2 < self.boundL) or
                    (y1 < self.boundD and y2 > self.boundU) or
                    (y1 > self.boundU and y2 < self.boundD)
                ):
                x1, y1 = x2, y2
                t += graphAccuracy
                continue
            else:
                if first_visible is None:
                    first_visible = ((x1, y1), (x2, y2))
                
                self.draw_line(x1, y1, x2, y2, curve_style)
                last_visible = ((x1, y1), (x2, y2))
                x1, y1 = x2, y2
                t += graphAccuracy
        
        if curve_style.show_arrows:
            width_px, length_px = curve_style.arrow_dims
            width = width_px / self.viewport.ppu_x
            length = length_px / self.viewport.ppu_y

            if last_visible is not None:

                (x1, y1), (x2, y2) = last_visible
                dx = x2 - x1
                dy = y2 - y1

                self.draw_arrowhead(x2, y2, dx, dy, width, length, curve_style)

            if first_visible is not None:

                (x1, y1), (x2, y2) = first_visible
                dx = x1 - x2
                dy = y1 - y2

                self.draw_arrowhead(x1, y1, dx, dy, width, length, curve_style)
    
    def draw_UI_line(self, marginX, marginY, txt, text_style: TextStyle = None, corner = "NW", line = 0):
        if text_style is None:
            text_style = self.default_UITextStyle
        one_line_height = text_style.font_size
        x_left = marginX
        y_center = marginY + (line * one_line_height)
        text = txt
        if corner == "NW":
            self.draw_text_px(xLeft = x_left, y = y_center, txt = text, text_style = text_style)
        elif corner == "NE":
            self.draw_text_px(xRight = self.viewport.width - x_left, y = y_center, txt = text, text_style = text_style)
        elif corner == "SW":
            self.draw_text_px(xLeft = x_left, y = self.viewport.height - y_center, txt = text, text_style = text_style)
        elif corner == "SE":
            self.draw_text_px(xRight = self.viewport.width - x_left, y = self.viewport.height - y_center, txt = text, text_style = text_style)

    def draw_UI(self):
        for corner_type in self.ui_space:
            for index, line in enumerate(self.ui_space[corner_type]):
                marginX, marginY, txt, text_style = line
                if marginX is None:
                    marginX = self.viewport.ui_scale(20)
                if marginY is None:
                    marginY = self.viewport.ui_scale(20)
                
                self.draw_UI_line(marginX, marginY, txt, text_style, corner_type, index)

    def add_UI_line(self, marginX: float, marginY: float, txt: str, text_style: TextStyle, corner: str):
        if corner.upper() in ["NW", "NE", "SW", "SE"]:
            self.ui_space[corner].append([marginX, marginY, txt, text_style])
        else:
            raise TypeError

    def clear_UI(self):
        text_style = None
        x_margin = self.viewport.ui_scale(20)
        y_margin = self.viewport.ui_scale(20)
        self.ui_space["NW"] = [[x_margin, y_margin, f"Scale: ({self.viewport.scale_x:g}, {self.viewport.scale_y:g})", text_style],
                                [x_margin, y_margin, f"Center: ({self.viewport.screen_to_graph(self.viewport.width/2, self.viewport.height/2)[0]:g}, {self.viewport.screen_to_graph(self.viewport.width/2, self.viewport.height/2)[1]:g})", text_style],
                                [x_margin, y_margin, f"Move Speed: {self.camera_controller.speed:g}", text_style]]
        self.ui_space["NE"] = [[x_margin, y_margin, f"FPS: {self.fps}", text_style]]

        self.ui_space["SW"] = []
        self.ui_space["SE"] = []
        


