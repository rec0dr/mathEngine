class Point:
    def __init__(self, pos):
        self.x, self.y = pos

    @property
    def pos(self):
        return (self.x, self.y)

    @pos.setter
    def pos(self, tuple):
        self.x, self.y = tuple
    
    def update(self, dt):
        pass
    
    def __str__(self):
        return "({self.x}, {self.y})"