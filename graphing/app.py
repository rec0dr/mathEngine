import pygame
import time

from .viewport import Viewport
from .renderer import Renderer
from styles.line_style import LineStyle
from functions.function import Function
from functions.parametric import Parametric


BASE_SENSITIVITY_POWER = 1
BASE_ZOOM_FACTOR = 1.1

class GraphApp:
    def __init__(self, width, height, sensitivity=100):
        pygame.init()
        self.screen = pygame.display.set_mode((width, height))
        self.viewport = Viewport(width, height)
        self.renderer = Renderer(self.screen, self.viewport)

        self.running = False
        self.width = width
        self.height = height
        self.sensitivity = sensitivity

        self.functions = []

    def pan_mouse(self):
        dx, dy = pygame.mouse.get_rel()

        if pygame.mouse.get_pressed()[0]:
            factor = 1/100 * BASE_SENSITIVITY_POWER
            dx = -dx * (self.sensitivity*factor)
            dy = dy * (self.sensitivity*factor)
            self.viewport.pan_pixels(dx, dy)
    
    def zoom_mouse(self, events):
        for event in events:
            if event.type == pygame.MOUSEWHEEL:
                zoom_factor = BASE_ZOOM_FACTOR ** event.y
                
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
    
    def draw_functions(self):
        for function in self.functions:
            if isinstance(function, Function):
                self.renderer.draw_function(function)
            elif isinstance(function, Parametric):
                self.renderer.draw_parametric(function)
    
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
                if event.key == pygame.K_h:
                    curX, curY = self.viewport.screen_to_graph(self.width / 2, self.height / 2)
                    dx = -curX/100
                    dy = -curY/100
                    curScaleX, curScaleY = self.viewport.scale_x, self.viewport.scale_y
                    zoomX, zoomY = curScaleX**(-1/100) * (10**(1/100)), curScaleY**(-1/100) * (10**(1/100))
                    for _ in range(100):
                        self.begin_frame()
                        self.viewport.pan_by(dx, dy)
                        self.draw_functions()
                        self.end_frame()
                        time.sleep(0.01)
                    
                    for _ in range(100):
                        self.begin_frame()
                        self.viewport.zoom_by(1/zoomX, 1/zoomY)
                        self.draw_functions()
                        self.end_frame()
                        time.sleep(0.01)
                elif event.key == pygame.K_q:
                    self.running = False
                        
                        
    
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
            self.handle_inputs()
            
            self.begin_frame()
            self.draw_functions()
            self.end_frame()
        pygame.quit()
    

        