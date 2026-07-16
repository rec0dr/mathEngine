class Animation:
    def __init__(self, start=0, end=1, duration=1):
        self.start = start
        self.end = end
        self.duration = duration

        self.elapsed = 0
        self.value = start
        self.finished = False
    
    def update(self, dt):
        if self.finished:
            return

        self.elapsed += dt
        
        t = min(self.elapsed / self.duration, 1)

        self.value = self.start + t * (self.end - self.start)

        if t == 1:
            self.finished = True