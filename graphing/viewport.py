import math

DEFAULT_WIDTH = 600
DEFAULT_HEIGHT = 600

class Viewport:
    def __init__(self, w=DEFAULT_WIDTH, h=DEFAULT_HEIGHT, scaleX=10, scaleY=10):
        self.width = w
        self.height = h

        self.origin_x = w/2
        self.origin_y = h/2

        self.scale_x = scaleX
        self.scale_y = scaleY

        self.ppu_x = (w/2) / scaleX
        self.ppu_y = (h/2) / scaleY
    
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
        self.ppu_x *= scaleX
        self.ppu_y *= scaleY
        self.scale_x /= scaleX
        self.scale_y /= scaleY

    def set_scale(self, scaleX, scaleY=None):
        if scaleY is None:
            scaleY = scaleX
        self.scale_x, self.scale_y = scaleX, scaleY
        self.ppu_x = self.width / scaleX / 2
        self.ppu_y = self.height / scaleY / 2

    def pan_by(self, dx, dy):
        self.origin_x -= (self.ppu_x) * dx
        self.origin_y += (self.ppu_y) * dy
    
    def pan_to(self, x, y):
        self.origin_x = (self.width/2) + x * self.ppu_x
        self.origin_y = (self.height/2) + y * self.ppu_y
    
    def pan_pixels(self, dx, dy):
        self.origin_x -= dx
        self.origin_y += dy
    
    def status(self):
        print(f"scaleX: {self.scale_x:.10}")
        print(f"scaleY: {self.scale_y:.10}")
        originX, originY = self.screen_to_graph(self.width / 2, self.height / 2)
        print(f"Camera origin: ({originX:.10}, {originY:.10})")

    




