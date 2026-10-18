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

from styles.style import Style
from styles.point_style import PointStyle, LockType
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

        self.fps = fps
        self.time_ran = 0
        self.dt = 0

        self.running = False
        self.width = width
        self.height = height
        self.pan_sensitivity = pan_sensitivity
        self.zoom_sensitivity = zoom_sensitivity
        self.slide_multi = 1
        self.key_binds = {}

        self.graphObjects = []
        self.extraUILines = []

        self.show_camera_center = show_camera_center
        self.allow_mouse = True
        self.prev_point = None

        pygame.display.set_caption("Le, Evan - Math Engine Indev 0.0.1")

    def show_camera_status(self):
        """Helps the developer test the camera status at any given time."""

        if pygame.mouse.get_pressed()[2]:
            self.viewport.status()
    
    def begin_frame(self):
        """Runs at the beginning of each frame by clearing the renderer, drawing the axes, and drawing the grid."""
        self.dt = self.clock.tick(self.fps) / 1000

        self.renderer.clear()
        self.renderer.draw_axes()
        self.renderer.draw_grid()


    def add_animation(self, target, property_name, end=1, duration=1, ease_type: EaseType = EaseType.LINEAR, start=None, loop=True, two_way=True):
        """Adds an animation to the app with customizable parameters."""
        self.animation_manager.add(Animation(target, property_name, end, duration, ease_type, start, loop, two_way))
        
    def add_animations(self, *animations: Animation):
        """Adds multiple animations, each in the form of an Animation() class."""

        self.animation_manager.add(*animations)
    
    def add_graph_objects(self, *objects: GraphObject):
        """Adds multiple graphs to the app simultaneously, each being a GraphObject object."""

        self.graph_manager.add(*objects)

    def add_styled_object(self, object, **style_kwargs):
        """Adds a styled object to the app via customizable parameters for the style."""

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
        """Adds multiple styled objects to the app via a dictionary. Not recommended."""

        for object in object_list:
            self.add_styled_object(object, **style_kwargs)

    def add_object(self, object, **style_kwargs):
        """Default function for adding an object; identical to add_styled_object()."""

        self.add_styled_object(object, **style_kwargs)

    def add_unstyled_objects(self, *objects):
        """Adds multiple objects at the same time, all unstyled."""

        for object in objects:
            self.add_object(object)
    
    def end_frame(self):
        """Runs at the end of each frame. (Default procedures)"""

        self.screen.blit(self.renderer.overlay,(0,0))
        self.draw_text()
        pygame.display.flip()
    
    def check_quit(self, events):
        """Checks for if the user exited the window to trigger a quit sequence."""

        for event in events:
            if event.type == pygame.QUIT:
                self.running = False
    
    def key_inputs(self, events):
        """Checks for various non-camera keyboard inputs."""

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
                        # print(self.prev_point.x, self.prev_point.y)

                    self.prev_point = cur_point
                elif event.key == pygame.K_c:
                    self.graph_manager.clear()
                    self.camera_controller.locked = False

                elif event.key in self.key_binds:
                    if callable(self.key_binds[event.key]):
                        self.key_binds[event.key]()

    def handle_inputs(self, dt):
        """General function for handling all inputs, camera and non-camera, along with exit checks."""

        events = pygame.event.get()

        self.check_quit(events)
        self.key_inputs(events)
        self.camera_controller.update(events, dt)
    
    def update_animations(self, dt):
        """Runs each frame. Uses the animation manager to update each individual animation given a change in time."""

        self.animation_manager.update(dt)
    
    def draw_objects(self):
        """Standard procedure for drawing all non-default objects in the app."""

        for layer in self.graph_manager.graph_objects:
            if layer != "Labels":
                for object in self.graph_manager.graph_objects[layer]:
                    self.renderer.draw_graph(object)

    def handle_settings(self):
        """Procedure for handling all custom settings."""

        if self.show_camera_center:
            self.renderer.draw_point(Point(self.viewport.screen_to_graph(self.viewport.width/2, self.viewport.height/2)))

    def move_dragged(self):
        """Moves draggable points each frame via various checks and style customs."""

        mouse_pos = pygame.mouse.get_pos()
        click_count = 0
        for object in self.graph_manager["Points"]:
            style = object.style
            drawable = object.drawable
            if isinstance(drawable, Point) and isinstance(style, PointStyle):
                if style.hovered and pygame.mouse.get_pressed()[0]:
                    click_count += 1
                    
        for object in self.graph_manager["Points"]:
            style = object.style
            drawable = object.drawable
            if isinstance(drawable, Point) and isinstance(style, PointStyle):
                if not style.draggable:
                    return
                
                if style.hovered:
                    if pygame.mouse.get_pressed()[0]:
                        if click_count == 1:
                            if isinstance(drawable, TracedPoint):
                                mouse_x = self.viewport.screen_to_graph(*mouse_pos)[0]
                                if style.lock_type == LockType.FREE:
                                    drawable.parameter = mouse_x
                            else:
                                mouse = self.viewport.screen_to_graph(*mouse_pos)
                                if style.lock_type == LockType.FREE:
                                    drawable.pos = mouse
                                elif style.lock_type == LockType.X:
                                    drawable.y = mouse[1]
                                elif style.lock_type == LockType.Y:
                                    drawable.x = mouse[0]
                            
                        self.camera_controller.locked = True
                    else:
                        self.camera_controller.locked = False
                else:
                    pass

                #print(click_count)

                point_pos = self.viewport.graph_to_screen(*drawable.pos)
                flag_x = (abs(mouse_pos[0] - point_pos[0]) <= style.radius_px)
                flag_y = (abs(mouse_pos[1] - point_pos[1]) <= style.radius_px)
                flag_press = pygame.mouse.get_pressed()[0]
                #print(flag_x, flag_y)

                if isinstance(drawable, TracedPoint):
                    if style.hovered and flag_press:
                        style.hovered = flag_x
                    else:
                        style.hovered = (flag_x and flag_y)
                else:
                    if style.hovered and flag_press:
                        if style.lock_type == LockType.X:
                            style.hovered = flag_y
                        elif style.lock_type == LockType.Y:
                            style.hovered = flag_x
                        else:
                            style.hovered = (flag_x and flag_y)
                    else:
                        style.hovered = (flag_x and flag_y)
                
                #print(style.hovered)
    
    def draw_text(self):
        self.draw_UI()
        self.draw_labels()

    def draw_UI(self):
        """Runs every frame to draw the UI - default and user-created."""

        self.renderer.fps = round(self.clock.get_fps(), 3)
        self.renderer.time_ran = round(pygame.time.get_ticks() / 1000)
        self.renderer.reset_UI()

        for layer in self.graph_manager.graph_objects:
            if layer != "Labels":
                for graph in self.graph_manager.graph_objects[layer]:
                    if isinstance(graph.style, Style):
                        if graph.style.show_ui:
                            name = ""
                            if graph.style.show_type:
                                for cls in type(graph.drawable).__mro__:
                                    if cls in NAME_MAP:
                                        graph_name = NAME_MAP[cls]
                                        break
                                name = f"{graph_name}"
                                if graph.style.name != "":
                                    name = name + " "
                            name = name + f"{graph.style.name}: {str(graph.drawable)}"

                            self.renderer.add_UI_line(None, None, name, None, "NW")

        for line in self.extraUILines:
            marginX, marginY, txt, text_style, corner = line
            if callable(marginX):
                marginX = marginX()
            elif isinstance(marginX, Value):
                marginX = marginX.value

            if callable(marginY):
                marginY = marginY()
            elif isinstance(marginY, Value):
                marginY = marginY.value

            if callable(txt):
                txt = txt()
            self.renderer.add_UI_line(marginX, marginY, txt, text_style, corner)

        self.renderer.draw_UI()

    def add_UI_line(self, marginX: float = None, marginY: float = None, txt: str = "", text_style: TextStyle = None, corner: str = "NW"):
        if marginX is None:
            marginX = self.viewport.ui_scale(20)
        if marginY is None:
            marginY = self.viewport.ui_scale(20)
        if text_style is None:
            text_style = self.renderer.default_UITextStyle
        self.extraUILines.append([marginX, marginY, txt, text_style, corner])

    def draw_labels(self):
        for label in self.graph_manager.graph_objects["Labels"]:
            self.renderer.draw_graph(label)

    def run(self):
        """General procedure for starting up the app.
        Handles inputs, updates animations, draws graphs,
        handles settings, moves dragged points, and runs until
        an exit sequence is triggered."""

        self.prev_point = None

        self.running = True
        while self.running:
            self.handle_inputs(self.clock.get_fps())
            self.begin_frame()

            self.update_animations(self.dt)
            self.draw_objects()
            self.handle_settings()
            self.move_dragged()
            
            self.end_frame()
        pygame.quit()
    

        