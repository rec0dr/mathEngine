import math
import pygame

from objects.point import Point
from .viewport import Viewport
from .animation_manager import AnimationManager
from anim.animation import Animation, EaseType

PAN_KEY_SPEED = 1/60
ZOOM_KEY_SPEED = 1/3
BASE_SENSITIVITY_POWER = 1
BASE_ZOOM_FACTOR = 1.1

class CameraController:
    def __init__(self, viewport: Viewport, animation_manager: AnimationManager = None, base_speed: int = 1, mouse_sensitivity: float = 100, fixed_center: tuple | Point = None, default_set = [0, 0, 10, 10]):
        self.pan_lock = (fixed_center is not None)
        self.fixed_center = fixed_center
        if not isinstance(self.fixed_center, Point) and self.pan_lock:
            self.fixed_center = Point(self.fixed_center)

        self.viewport = viewport
        self.animation_manager = animation_manager

        self.speed = base_speed
        self.mouse_sensitivity = mouse_sensitivity

        self.default_cx, self.default_cy, self.default_sx, self.default_sy = default_set
        self.locked = False

        self.camera_anims = []
    
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

        animations = []
        for animation in Animation.multiple(
            self.viewport,
            duration,
            ease_type,
            loop=False,
            two_way=False,
            **attrs
        ):
            self.animation_manager.add(animation)
            animations.append(animation)

        return animations

    def handle_panning_keys(self, fps):
        if self.fixed_center is not None:
            return
        
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            self.viewport.pan_by(0, self.viewport.scale_y * PAN_KEY_SPEED * self.speed * (60 / fps))
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.viewport.pan_by(self.viewport.scale_x * PAN_KEY_SPEED * self.speed * (60 / fps), 0)
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            self.viewport.pan_by(0, -self.viewport.scale_y * PAN_KEY_SPEED * self.speed * (60 / fps))
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.viewport.pan_by(-self.viewport.scale_x * PAN_KEY_SPEED * self.speed * (60 / fps), 0)
    
    def handle_zooming_keys(self, fps):
        keys = pygame.key.get_pressed()
        pos = pygame.mouse.get_pos()
        if keys[pygame.K_LSHIFT]:
            pos = (self.viewport.width/2, self.viewport.height/2)

        if self.fixed_center is not None:
            pos = self.viewport.graph_to_screen(self.fixed_center.x, self.fixed_center.y)
        
        if keys[pygame.K_z]:
            self.zoom_to(*pos, BASE_ZOOM_FACTOR ** (ZOOM_KEY_SPEED * self.speed * (60 / fps)))
        if keys[pygame.K_x]:
            self.zoom_to(*pos, BASE_ZOOM_FACTOR ** (-ZOOM_KEY_SPEED * self.speed * (60 / fps)))
    
    def handle_panning_mouse(self):
        if self.fixed_center is not None:
            return
        
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
                if self.fixed_center is not None:
                    pos = self.viewport.graph_to_screen(self.fixed_center.x, self.fixed_center.y)

                self.zoom_to(*pos, zoom_factor)
    
    def handle_anim_keys(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    keys = pygame.key.get_pressed()
                    if keys[pygame.K_LSHIFT]:
                        self.camera_anims = self.animate_to((0, 0), (10, 10), duration=3, ease_type=EaseType.CUBIC_IN_OUT)
                    else:
                        self.camera_anims = self.animate_to((self.default_cx,self.default_cy),(self.default_sx, self.default_sy),duration=3, ease_type = EaseType.CUBIC_IN_OUT)
    
    def handle_speed_change(self, events):
        keys = pygame.key.get_pressed()
        inc = 0.01
        if keys[pygame.K_RSHIFT]:
            inc = 0.05
        if keys[pygame.K_PERIOD]:
            self.speed += inc
        elif keys[pygame.K_COMMA]:
            self.speed -= inc

        elif keys[pygame.K_SLASH]:
            self.speed = 1

        if self.speed < 0:
            self.speed = 0
    
    def update(self, events, dt):
        for anim in self.camera_anims:
            if anim.finished:
                self.camera_anims.remove(anim)
                self.locked = False
            else:
                self.locked = True

        # KEYBOARD INPUTS - don't care about locked status
        self.handle_panning_keys(dt)
        self.handle_zooming_keys(dt)
        self.handle_speed_change(events)

        # MOUSE INPUTS & ANIMATIONS - locked does matter
        if not self.locked:
            self.handle_panning_mouse()
            self.handle_anim_keys(events)
            self.handle_zooming_mouse(events)

            if self.fixed_center is not None:
                #print(self.fixed_center)
                self.viewport.pan_to(self.fixed_center.x, self.fixed_center.y)

        
