import math

class Viewport:
    def __init__(self, w, h):
        self.width = w
        self.height = h

        self.origin_x = w/2
        self.origin_y = h/2

        self.ppu_x = w/20
        self.ppu_y = h/20

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

    def set_scale(self, scaleX, scaleY=None):
        if scaleY is None:
            scaleY = scaleX
        self.ppu_x = self.width / scaleX / 2
        self.ppu_y = self.height / scaleY / 2

    def pan_by(self, dx, dy):
        self.origin_x -= (self.ppu_x) * dx
        self.origin_y += (self.ppu_y) * dy
    
    def pan_pixels(self, dx, dy, sensitivity=10):
        self.origin_x -= dx / self.ppu_x * sensitivity
        self.origin_y += dy / self.ppu_y * sensitivity
    




