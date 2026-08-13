import pygame

from .viewport import Viewport
from .animation_manager import AnimationManager
from .camera_controller import CameraController
from .renderer import Renderer
from .graph_object import GraphObject
from .graph_manager import GraphManager
from .analyzer import Analyzer
from .registries import STYLE_MAP, NAME_MAP

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
    def __init__(self, width, height, scaleX=10, scaleY=10, pan_sensitivity=100, zoom_sensitivity=None, fps=60, show_camera_center: bool = False, fixed_center: Point = None):
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

        self.show_camera_center = show_camera_center
        self.allow_mouse = True
        self.prev_point = None

        pygame.display.set_caption("Le, Evan - Math Engine Indev 0.0.1")



    def show_camera_status(self):
        if pygame.mouse.get_pressed()[2]:
            self.viewport.status()
    
    def begin_frame(self):
        self.renderer.clear()
        self.renderer.draw_axes()
        self.renderer.draw_ticks()


    def add_animation(self, target, property_name, end=1, duration=1, ease_type: EaseType = EaseType.LINEAR, start=None, loop=True, two_way=True):
        self.animation_manager.add(Animation(target, property_name, end, duration, ease_type, start, loop, two_way))
        
    def add_animations(self, *animations: Animation):
        self.animation_manager.add(*animations)
    
    def add_graph_objects(self, *objects: GraphObject):
        self.graph_manager.add(*objects)

    def add_styled_object(self, object, **style_kwargs):
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

    def add_styled_objects(self, object_list, **style_kwargs):
        for object in object_list:
            self.add_styled_object(object, **style_kwargs)

    def add_object(self, object, **style_kwargs):
        self.add_styled_object(object, **style_kwargs)

    def add_unstyled_objects(self, *objects):
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
                    cur_point = Point(x, y)
                    self.add_object(cur_point, color=(255, 0, 0), radius_px=10, draggable=True)

                    if self.prev_point is not None:
                        self.add_object(LineSegment(self.prev_point, cur_point), show_ends=False)
                        print(self.prev_point.x, self.prev_point.y)

                    self.prev_point = cur_point
                elif event.key == pygame.K_c:
                    self.graph_manager.graph_objects = []

                        
    
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

    def handle_settings(self):
        if self.show_camera_center:
            self.renderer.draw_point(Point(self.viewport.screen_to_graph(self.viewport.width/2, self.viewport.height/2)))

    def move_dragged(self):
        mouse_pos = pygame.mouse.get_pos()
        any_hover = False
        for object in self.graph_manager:
            style = object.style
            drawable = object.drawable
            if isinstance(drawable, Point) and isinstance(style, PointStyle):
                if not style.draggable:
                    return
                
                if style.hovered:
                    if pygame.mouse.get_pressed()[0]:
                        if not any_hover:
                            if isinstance(drawable, TracedPoint):
                                mouse_x = self.viewport.screen_to_graph(*mouse_pos)[0]
                                drawable.parameter = mouse_x
                            else:
                                drawable.pos = self.viewport.screen_to_graph(*mouse_pos)
                            any_hover = True
                        self.camera_controller.locked = True
                    else:
                        self.camera_controller.locked = False
                point_pos = self.viewport.graph_to_screen(*drawable.pos)

                if isinstance(drawable, TracedPoint):
                    if style.hovered:
                        if abs(mouse_pos[0] - point_pos[0]) <= style.radius_px:
                            style.hovered = True
                        else:
                            style.hovered = False
                    else:
                        if abs(mouse_pos[0] - point_pos[0]) <= style.radius_px and abs(mouse_pos[1] - point_pos[1]) <= style.radius_px:
                            style.hovered = True
                        else:
                            style.hovered = False
                else:
                    if abs(mouse_pos[0] - point_pos[0]) <= style.radius_px and abs(mouse_pos[1] - point_pos[1]) <= style.radius_px:
                        style.hovered = True
                    else:
                        style.hovered = False
                
                print(style.hovered)

    def draw_UI(self, dt):
        self.renderer.fps = round(self.clock.get_fps(), 3)
        self.renderer.draw_def_UI()
        ln = 4

        for graph in self.graph_manager.graph_objects:
            if graph.style.show_ui:
                for cls in type(graph.drawable).__mro__:
                    if cls in NAME_MAP:
                        graph_name = NAME_MAP[cls]
                        break
                name = f"{graph_name}"
                if graph.style.name != "":
                    name = name + " "
                name = name + f"{graph.style.name}: {str(graph.drawable)}"

                self.renderer.draw_UI_line(ln, self.viewport.ui_scale(20), self.viewport.ui_scale(20), name, text_style=TextStyle(color=graph.style.color, font_size=self.viewport.ui_scale(18), bold=True))
                ln += 1

    def run(self):

        self.prev_point = None

        self.running = True
        while self.running:
            dt = self.clock.tick(self.fps) / 1000
            self.handle_inputs(self.clock.get_fps())
            self.begin_frame()

            self.update_animations(dt)
            self.draw_objects()
            self.handle_settings()
            self.move_dragged()
            
            self.draw_UI(dt)
            self.end_frame()
        pygame.quit()
    

        