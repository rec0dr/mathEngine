import pygame
import time

from .viewport import Viewport
from .renderer import Renderer
from styles.point_style import PointStyle
from functions.function import Function
from functions.parametric import Parametric
from objects.point import Point
from objects.animated_point import AnimatedPoint
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

        self.graphObjects = []

        self.traceStyle = PointStyle(color=(255,0,0),opacity=255,visible=True,is_solid=True)

    def pan_mouse(self):
        dx, dy = pygame.mouse.get_rel()

        if pygame.mouse.get_pressed()[0]:
            factor = 1/100 * BASE_SENSITIVITY_POWER
            dx = -dx * (self.pan_sensitivity*factor)
            dy = dy * (self.pan_sensitivity*factor)
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
    
    def do_animations(self, dt):
        for graph in self.graphObjects:
            if isinstance(graph.drawable, AnimatedPoint):
                graph.drawable.update(dt)
    
    def add_graphObject(self, obj: GraphObject):
        self.graphObjects.append(obj)
    
    def draw_graphObjects(self):
        for graph in self.graphObjects:
            self.renderer.draw_graph(graph)
    
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
                if event.key == pygame.K_q:
                    self.running = False
                elif event.key == pygame.K_f:
                    current_fps = self.clock.get_fps()
                    print(current_fps)
                elif event.key == pygame.K_h:
                    for obj in self.graphObjects:
                        obj.hide()
                elif event.key == pygame.K_s:
                    for obj in self.graphObjects:
                        obj.show()
                
                

                        
    
    def handle_inputs(self):
        events = pygame.event.get()

        self.check_quit(events)
        self.zoom_mouse(events)
        self.pan_mouse()
        self.key_inputs(events)
        self.show_camera_status()
    
    def run(self):
        self.running = True
        while self.running:
            dt = self.clock.tick(self.fps) / 1000
            self.handle_inputs()
            
            self.begin_frame()
            self.do_animations(dt)
            self.draw_graphObjects()
            self.end_frame()
        pygame.quit()
    

        