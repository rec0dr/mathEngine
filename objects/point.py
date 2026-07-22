class Point:
    def __init__(self, pos):
        self.x, self.y = pos
    
    def update(self, dt):
        pass
    
    def __str__(self):
        return "({self.x}, {self.y})"