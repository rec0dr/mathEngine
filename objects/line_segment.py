class LineSegment:
    def __init__(self, pos1, pos2):
        self.x1, self.y1 = pos1
        self.x2, self.y2 = pos2

    @property
    def pos1(self):
        return (self.x1, self.y1)

    @pos1.setter
    def pos1(self, tuple):
        self.x1 = tuple[0]
        self.y1 = tuple[1]

    @property
    def pos2(self):
        return (self.x2, self.y2)

    @pos2.setter
    def pos2(self, tuple):
        self.x2 = tuple[0]
        self.y2 = tuple[1]
    
    def update(self, dt):
        pass
    
    def __str__(self):
        return f"({self.x1}, {self.y1}) -> ({self.x2}, {self.y2})"
    