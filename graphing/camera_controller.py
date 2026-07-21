import math
import pygame
from .viewport import Viewport
from .animation_manager import AnimationManager
from anim.animation import Animation, EaseType

PAN_KEY_SPEED = 1/60
ZOOM_KEY_SPEED = 1/3
BASE_SENSITIVITY_POWER = 1
BASE_ZOOM_FACTOR = 1.1

class CameraController:
    def __init__(self, viewport: Viewport, animation_manager: AnimationManager = None, base_speed: int = 1, mouse_sensitivity: float = 100):
        
        self.viewport = viewport
        self.animation_manager = animation_manager

        self.speed = base_speed
        self.mouse_sensitivity = mouse_sensitivity
    
    def zoom_to(self, screen_x, screen_y, zoom_factor):
        mx, my = screen_x, screen_y

        x1, y1 = self.viewport.screen_to_graph(mx, my)
        self.viewport.zoom_by(zoom_factor)
        x2, y2 = self.viewport.screen_to_graph(mx, my)

        self.viewport.pan_by(x1 - x2, y1 - y2)
    
    def animate_to(self,center=None,scale=None,duration=3,ease_type=EaseType.SIN_IN_OUT):
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
            self.animation_manager.add(animation)

    def handle_panning_keys(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            self.viewport.pan_by(0, self.viewport.scale_y * PAN_KEY_SPEED * self.speed)
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.viewport.pan_by(self.viewport.scale_x * PAN_KEY_SPEED * self.speed, 0)
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            self.viewport.pan_by(0, -self.viewport.scale_y * PAN_KEY_SPEED * self.speed)
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.viewport.pan_by(-self.viewport.scale_x * PAN_KEY_SPEED * self.speed, 0)
    
    def handle_zooming_keys(self):
        keys = pygame.key.get_pressed()
        pos = pygame.mouse.get_pos()
        if keys[pygame.K_z]:
            self.zoom_to(*pos, BASE_ZOOM_FACTOR ** (ZOOM_KEY_SPEED * self.speed))
        if keys[pygame.K_x]:
            self.zoom_to(*pos, BASE_ZOOM_FACTOR ** (-ZOOM_KEY_SPEED * self.speed))
    
    def handle_panning_mouse(self):
        dx, dy = pygame.mouse.get_rel()

        if pygame.mouse.get_pressed()[0]:
            factor = 1/100 * BASE_SENSITIVITY_POWER
            dx = -dx * (self.mouse_sensitivity*factor)
            dy = -dy * (self.mouse_sensitivity*factor)
            self.viewport.pan_pixels(dx, dy)
        
    def handle_zooming_mouse(self, events):
        for event in events:
            if event.type == pygame.MOUSEWHEEL:
                zoom_factor = BASE_ZOOM_FACTOR ** (event.y * self.mouse_sensitivity/100)
                
                # Panning such that space expands/contracts about the mouse's position

                pos = pygame.mouse.get_pos()
                self.zoom_to(*pos, zoom_factor)
    
    def handle_home(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    self.animate_to((0,0),(10,10),duration=3, ease_type=EaseType.SIN_IN_OUT)
    
    def update(self, events):
        self.handle_panning_keys()
        self.handle_zooming_keys()

        self.handle_panning_mouse()
        self.handle_zooming_mouse(events)

        self.handle_home(events)

        
