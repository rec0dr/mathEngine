import math

class GraphObject:
    def __init__(self, drawable, style=None):
        self.drawable = drawable
        self.style = style
        self.visible = True
        self.z_index = 0

    
    def hide(self):
        self.style.visible = False
    
    def show(self):
        self.style.visible = True
        

        