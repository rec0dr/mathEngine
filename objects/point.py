class Point:
    def __init__(self, pos):
        self.x, self.y = pos
    
    def __str__(self):
        return "({self.x}, {self.y})"