from anim.animation import Animation

class AnimationManager:
    def __init__(self):
        self.animations = []

    def add(self, *animations: Animation):
        for animation in animations:
            self.animations.append(animation)

    def remove(self, *animations: Animation):
        for animation in animations:
            self.animations.remove(animation)
    
    def clear(self):
        self.animations.clear()

    def update(self, dt):
        for animation in self.animations[:]:
            animation.update(dt)
            if animation.finished:
                self.animations.remove(animation)
    
    def __iter__(self):
        return iter(self.animations)

    def __len__(self):
        return len(self.animations)
    
    def __getitem__(self, index):
        return self.animations[index]
    
    @property
    def active(self):
        return len(self.animations) > 0