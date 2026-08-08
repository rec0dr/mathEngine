import pygame

from .viewport import Viewport
from .animation_manager import AnimationManager
from .camera_controller import CameraController
from .renderer import Renderer
from .graph_object import GraphObject
from .graph_manager import GraphManager
from .analyzer import Analyzer
from .registries import STYLE_MAP

from anim.animation import Animation, EaseType

from styles.point_style import PointStyle
from styles.curve_style import CurveStyle
from styles.text_style import TextStyle
from styles.line_segment_style import LineSegmentStyle

from functions.curve import Curve
from functions.function import Function, Value
from functions.parametric import Parametric

from objects.point import Point
from objects.traced_point import TracedPoint
from objects.label import Label
from objects.line_segment import LineSegment


BASE_SENSITIVITY_POWER = 1
BASE_ZOOM_FACTOR = 1.1

class GraphApp:
    def __init__(self, width, height, scaleX=10, scaleY=10, pan_sensitivity=100, zoom_sensitivity=None, fps=60, fixed_center: Point = None):
        if zoom_sensitivity is None:
            zoom_sensitivity = pan_sensitivity
        pygame.init()
        pygame.font.init()
        
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((width, height))
        self.viewport = Viewport(width, height, scaleX, scaleY)
        self.animation_manager = AnimationManager()
        self.graph_manager = GraphManager()

        default_set = [0, 0]
        default_set.extend([scaleX, scaleY])

        self.camera_controller = CameraController(self.viewport, self.animation_manager, 1, pan_sensitivity, fixed_center, default_set)
        self.renderer = Renderer(self.screen, self.viewport, self.graph_manager, self.animation_manager, self.camera_controller)
        self.analyzer = Analyzer()

        self.running = False
        self.width = width
        self.height = height
        self.pan_sensitivity = pan_sensitivity
        self.zoom_sensitivity = zoom_sensitivity
        self.fps = fps
        self.slide_multi = 1

        self.graphObjects = []

        pygame.display.set_caption("Le, Evan - Math Engine Indev 0.0.1")

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
        if isinstance(object, (int, float)):
            object = Value(object)
        drawable = object
        for cls in type(object).__mro__:
            if cls in STYLE_MAP:
                style_name = STYLE_MAP[cls]
                break
        else:
            raise TypeError(f"No drawer registered for {type(object).__name__}")
        
        style = style_name(**style_kwargs)

        new_object = GraphObject(drawable, style)
        self.graph_manager.add(new_object)
        return new_object

    def add_dobjects(self, *objects):
        for object in objects:
            self.add_object(object)
    
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
                elif event.key == pygame.K_e:
                    x, y = self.viewport.screen_to_graph(*pygame.mouse.get_pos())
                    self.add_object(Point(x, y), color=(255, 0, 0), radius_px=5, labeled=True)

                    if self.prevpoint is not None:
                        self.add_object(LineSegment(Point(self.prevpoint.x, self.prevpoint.y), Point(x, y)))

                    self.prevpoint = Point(x, y)

                        
    
    def handle_inputs(self, dt):
        events = pygame.event.get()

        self.check_quit(events)
        self.key_inputs(events)
        self.camera_controller.update(events, dt)
    
    def update_animations(self, dt):
        self.animation_manager.update(dt)
    
    def draw_objects(self):
        for object in self.graph_manager:
            self.renderer.draw_graph(object)
    
    def run(self):

        self.prevpoint = None

        self.running = True
        while self.running:
            dt = self.clock.tick(self.fps) / 1000
            self.handle_inputs(self.clock.get_fps())
            self.begin_frame()

            self.update_animations(dt)
            self.draw_objects()
            
            self.renderer.draw_UI()
            self.end_frame()
        pygame.quit()
    

        