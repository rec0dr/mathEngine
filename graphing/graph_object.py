import math
from styles.style import Style
class GraphObject:
    def __init__(self, drawable, style=None):
        self.drawable = drawable
        self.style = style
        self.z_index = 0

        