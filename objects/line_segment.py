class LineSegment:
    def __init__(self, pos1, pos2):
        self.x1, self.y1 = pos1
        self.x2, self.y2 = pos2
    
    def __str__(self):
        return f"({self.x1}, {self.y1}) -> ({self.x2}, {self.y2})"
    