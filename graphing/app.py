import pygame
import time

from .viewport import Viewport
from .animation_manager import AnimationManager
from .camera_controller import CameraController
from .renderer import Renderer
from .graph_object import GraphObject
from .graph_manager import GraphManager

from anim.animation import Animation, EaseType

from styles.point_style import PointStyle
from styles.curve_style import CurveStyle
from styles.text_style import TextStyle

from functions.curve import Curve
from functions.function import Function
from functions.parametric import Parametric

from objects.point import Point
from objects.traced_point import TracedPoint
from objects.label import Label


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
        self.animation_manager = AnimationManager()
        self.graph_manager = GraphManager()
        self.camera_controller = CameraController(self.viewport, self.animation_manager, 1, pan_sensitivity)
        self.renderer = Renderer(self.screen, self.viewport, self.graph_manager, self.animation_manager, self.camera_controller)

        self.running = False
        self.width = width
        self.height = height
        self.pan_sensitivity = pan_sensitivity
        self.zoom_sensitivity = zoom_sensitivity
        self.fps = fps
        self.slide_multi = 1

        self.graphObjects = []

    def show_camera_status(self):
        if pygame.mouse.get_pressed()[2]:
            self.viewport.status()
    
    def begin_frame(self):
        self.renderer.clear()
        self.renderer.draw_axes()
        self.renderer.draw_ticks()


    def add_animations(self, *animations: Animation):
        self.animation_manager.add(*animations)
    
    def add_graph_objects(self, *objects: GraphObject):
        self.graph_manager.add(*objects)

    def add_object(self, object, **style_kwargs):
        drawable = object
        if isinstance(drawable, Curve):
            style = CurveStyle(**style_kwargs)
        elif isinstance(drawable, Point):
            style = PointStyle(**style_kwargs)
        elif isinstance(drawable, Label):
            style = TextStyle(**style_kwargs)
        else:
            raise TypeError

        new_object = GraphObject(drawable, style)
        self.graph_manager.add(new_object)
        return new_object

    def add_objects(self, *wrapped_objects):
        for drawable, style_kwargs in wrapped_objects:
            self.add_object(drawable, **style_kwargs)
    
    def end_frame(self):
        self.screen.blit(self.renderer.overlay,(0,0))
        pygame.display.flip()
    
    def check_quit(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                self.running = False
    
    def key_inputs(self, events):

        for event in events:
            if event.type == pygame.KEYDOWN:
                #Other key inputs
                
                if event.key == pygame.K_q:
                    self.running = False
                elif event.key == pygame.K_f:
                    current_fps = self.clock.get_fps()
                    print(current_fps)

                        
    
    def handle_inputs(self):
        events = pygame.event.get()

        self.check_quit(events)
        self.key_inputs(events)
        self.camera_controller.update(events)
    
    def update_animations(self, dt):
        self.animation_manager.update(dt)
    
    def draw_objects(self):
        for object in self.graph_manager:
            self.renderer.draw_graph(object)
    
    def run(self):
        self.running = True
        while self.running:
            dt = self.clock.tick(self.fps) / 1000
            self.handle_inputs()
            self.begin_frame()

            self.update_animations(dt)
            self.draw_objects()
            
            self.renderer.draw_UI()
            self.end_frame()
        pygame.quit()
    

        