from abc import ABC, abstractmethod

class Measurement(ABC):
    def __init__(self, value):
        self.value = value

    @abstractmethod
    def to_pixels(self, viewport):
        pass


class Pixels(Measurement):
    def to_pixels(self, viewport):
        return self.value


class GraphUnits(Measurement):
    def to_pixels(self, viewport):
        return self.value * viewport.ppu_x