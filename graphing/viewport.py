import math

DEFAULT_WIDTH = 600
DEFAULT_HEIGHT = 600

class Viewport:
    def __init__(self, w=DEFAULT_WIDTH, h=DEFAULT_HEIGHT, scaleX=10, scaleY=10):
        self.width = w
        self.height = h

        self.center_x = 0
        self.center_y = 0

        self.scale_x = scaleX
        self.scale_y = scaleY
    
    @property
    def origin_x(self):
        return self.width / 2 - self.center_x * self.ppu_x
    
    @property
    def origin_y(self):
        return self.height / 2 + self.center_y * self.ppu_y

    @property
    def ppu_x(self):
        return (self.width / 2) / self.scale_x
    @property
    def ppu_y(self):
        return (self.height / 2) / self.scale_y
    
    def ui_scale(self, s):
        """Scale any distance assuming it is only correct when the screen's dimensions are defaulted."""
        return int(s * (self.width / DEFAULT_WIDTH))

    def graph_to_screen(self,x,y):
        screen_x = self.origin_x + self.ppu_x * x
        screen_y = self.origin_y - self.ppu_y * y
        return (screen_x, screen_y)
    
    def screen_to_graph(self,x,y):
        graph_x = (x - self.origin_x) / self.ppu_x
        graph_y = (self.origin_y - y) / self.ppu_y
        return (graph_x, graph_y)
    
    def zoom_by(self, scaleX, scaleY=None):
        if scaleY is None:
            scaleY = scaleX
        self.scale_x /= scaleX
        self.scale_y /= scaleY

    def set_scale(self, scaleX, scaleY=None):
        if scaleY is None:
            scaleY = scaleX
        self.scale_x, self.scale_y = scaleX, scaleY

    def pan_by(self, dx, dy):
        self.center_x += dx
        self.center_y += dy
    
    def pan_to(self, x, y):
        self.center_x = x
        self.center_y = y
    
    def pan_pixels(self, dx, dy):
        self.center_x += (dx / self.ppu_x)
        self.center_y -= (dy / self.ppu_y)
    
    def status(self):
        print(f"scaleX: {self.scale_x:.10}")
        print(f"scaleY: {self.scale_y:.10}")
        originX, originY = self.screen_to_graph(self.width / 2, self.height / 2)
        print(f"Camera origin: ({originX:.10}, {originY:.10})")

    




