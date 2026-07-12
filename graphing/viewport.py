import math

class Viewport:
    def __init__(self):
        self.width = 1200
        self.height = 800

        self.origin_x = 600
        self.origin_y = 400

        self.ppu_x = 60
        self.ppu_y = 40

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
        self.origin_x += (self.ppu_x) * dx
        self.origin_y -= (self.ppu_y) * dy
    
    




