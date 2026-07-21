import pygame
import time

from .viewport import Viewport
from anim.animation import Animation, EaseType
from .renderer import Renderer
from styles.point_style import PointStyle
from styles.curve_style import CurveStyle
from styles.text_style import TextStyle
from functions.curve import Curve
from functions.function import Function
from functions.parametric import Parametric
from objects.point import Point
from objects.animated_point import AnimatedPoint
from objects.traced_point import TracedPoint
from objects.label import Label
from .graph_object import GraphObject


BASE_SENSITIVITY_POWER = 1
BASE_ZOOM_FACTOR = 1.1

class GraphApp:
    def __init__(self, width, height, scaleX=10, scaleY=10, pan_sensitivity=100, zoom_sensitivity=None, fps=60):
        if zoom_sensitivity is None:
            zoom_sensitivity = pan_sensitivity
        pygame.init()
        pygame.font.init()
        
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((width, height))
        self.viewport = Viewport(width, height, scaleX, scaleY)
        self.renderer = Renderer(self.screen, self.viewport)

        self.running = False
        self.width = width
        self.height = height
        self.pan_sensitivity = pan_sensitivity
        self.zoom_sensitivity = zoom_sensitivity
        self.fps = fps
        self.slide_multi = 1

        self.graphObjects = []
        self.animations = []

        self.traceStyle = PointStyle(color=(255,0,0),opacity=255,visible=True,is_solid=True)

    def pan_mouse(self):
        dx, dy = pygame.mouse.get_rel()

        if pygame.mouse.get_pressed()[0]:
            factor = 1/100 * BASE_SENSITIVITY_POWER
            dx = -dx * (self.pan_sensitivity*factor)
            dy = -dy * (self.pan_sensitivity*factor)
            self.viewport.pan_pixels(dx, dy)
    
    def zoom_mouse(self, events):
        for event in events:
            if event.type == pygame.MOUSEWHEEL:
                zoom_factor = BASE_ZOOM_FACTOR ** event.y
                if zoom_factor < 0:
                    zoom_factor **= (self.zoom_sensitivity/100)
                    zoom_factor *= -1
                else:
                    zoom_factor **= (self.zoom_sensitivity/100)
                
                # Panning such that space expands/contracts about the mouse's position

                mx, my = pygame.mouse.get_pos()

                x1, y1 = self.viewport.screen_to_graph(mx, my)
                self.viewport.zoom_by(zoom_factor)
                x2, y2 = self.viewport.screen_to_graph(mx, my)

                self.viewport.pan_by(x1 - x2, y1 - y2)

    def show_camera_status(self):
        if pygame.mouse.get_pressed()[2]:
            self.viewport.status()
    
    def begin_frame(self):
        self.renderer.clear()
        self.renderer.draw_axes()
        self.renderer.draw_ticks()
    
    def move_animPoints(self, dt):
        for graph in self.graphObjects:
            if isinstance(graph.drawable, (AnimatedPoint, TracedPoint)):
                graph.drawable.update(dt)
    
    def update_animations(self, dt):
        for animation in self.animations:
            animation.update(dt)
            
            if animation.finished:
                self.animations.remove(animation)

    def add_animation(self, animation: Animation):
        self.animations.append(animation)
    
    def add_animations(self, animations: list[Animation]):
        self.animations.extend(animations)
    
    def animate_to(
        self,
        center=None,
        scale=None,
        duration=3,
        ease_type=EaseType.SIN_IN_OUT
    ):
        attrs = {}

        if center is not None:
            center_x, center_y = center

            attrs["center_x"] = center_x
            attrs["center_y"] = center_y

        if scale is not None:
            scale_x, scale_y = scale
            attrs["scale_x"] = scale_x
            attrs["scale_y"] = scale_y

        for animation in Animation.multiple(
            self.viewport,
            duration,
            ease_type,
            **attrs
        ):
            self.add_animation(animation)
    
    def add_graphObject(self, obj: GraphObject):
        self.graphObjects.append(obj)
    
    def add_graphObjects(self, objectSet):
        self.graphObjects.extend(objectSet)
    
    def add(self, obj, **style_kwargs):
        if isinstance(obj, Point):
            style = PointStyle(**style_kwargs)
        elif isinstance(obj, Curve):
            style = CurveStyle(**style_kwargs)
        elif isinstance(obj, Label):
            style = TextStyle(**style_kwargs)
        else:
            raise TypeError("Not implemented man, check back later :/")
        
        graph_object = GraphObject(obj, style)
        self.add_graphObject(graph_object)
        return graph_object

    def draw_graphObjects(self):
        for graph in self.graphObjects:
            self.renderer.draw_graph(graph)
    
    def draw_UI(self):
        self.renderer.draw_overlay(self)
    
    def end_frame(self):
        self.screen.blit(self.renderer.overlay,(0,0))
        pygame.display.flip()
    
    def check_quit(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                self.running = False
    
    def key_inputs(self, events, dt):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LSHIFT]:
            self.slide_multi = 1/5
        elif keys[pygame.K_RSHIFT]:
            self.slide_multi = 5
        elif keys[pygame.K_MINUS]:
            self.slide_multi -= 0.3 * dt
        elif keys[pygame.K_EQUALS]:
            self.slide_multi += 0.3 * dt
        elif keys[pygame.K_1]:
            self.slide_multi = 1
        
        if self.slide_multi < 0:
            self.slide_multi = 0
        
        pan_ratio = 1 / 60
        zoom_ratio = 1 / 3
        #WASD/Arrows for panning
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            self.renderer.viewport.pan_by(0, self.renderer.viewport.scale_y * pan_ratio * self.slide_multi)
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            self.renderer.viewport.pan_by(0, -self.renderer.viewport.scale_y * pan_ratio * self.slide_multi)
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.renderer.viewport.pan_by(-self.renderer.viewport.scale_x * pan_ratio * self.slide_multi, 0)
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.renderer.viewport.pan_by(self.renderer.viewport.scale_x * pan_ratio * self.slide_multi, 0)

        #Z/X for zooming in/out
        if keys[pygame.K_z]:
            zoom_factor = BASE_ZOOM_FACTOR ** (zoom_ratio * self.slide_multi)
            mx, my = pygame.mouse.get_pos()

            x1, y1 = self.viewport.screen_to_graph(mx, my)
            self.viewport.zoom_by(zoom_factor)
            x2, y2 = self.viewport.screen_to_graph(mx, my)

            self.viewport.pan_by(x1 - x2, y1 - y2)
        if keys[pygame.K_x]:
            zoom_factor = BASE_ZOOM_FACTOR ** (-zoom_ratio * self.slide_multi)
            mx, my = pygame.mouse.get_pos()

            x1, y1 = self.viewport.screen_to_graph(mx, my)
            self.viewport.zoom_by(zoom_factor)
            x2, y2 = self.viewport.screen_to_graph(mx, my)

            self.viewport.pan_by(x1 - x2, y1 - y2)

        for event in events:
            if event.type == pygame.KEYDOWN:
                #Other key inputs
                
                if event.key == pygame.K_q:
                    self.running = False
                elif event.key == pygame.K_f:
                    current_fps = self.clock.get_fps()
                    print(current_fps)
                elif event.key == pygame.K_r:
                    self.animate_to((0,0),(10,10),duration=3, ease_type=EaseType.SIN_IN_OUT)

                        
    
    def handle_inputs(self, dt):
        events = pygame.event.get()

        self.check_quit(events)
        self.zoom_mouse(events)
        self.pan_mouse()
        self.key_inputs(events, dt)
        self.show_camera_status()
    
    def run(self):
        self.running = True
        while self.running:
            dt = self.clock.tick(self.fps) / 1000
            self.handle_inputs(dt)
            
            self.begin_frame()
            self.move_animPoints(dt)
            self.update_animations(dt)
            self.draw_graphObjects()
            self.draw_UI()
            self.end_frame()
        pygame.quit()
    

        