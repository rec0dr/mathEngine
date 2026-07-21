from .graph_object import GraphObject

class GraphManager:
    def __init__(self):
        self.graph_objects: list[GraphObject] = []
    
    def add(self, *objects: GraphObject):
        for obj in objects:
            self.graph_objects.append(obj)
    
    def remove(self, *objects: GraphObject):
        for obj in objects:
            self.graph_objects.remove(obj)
    
    def clear(self):
        self.graph_objects.clear()

    def __iter__(self):
        return iter(self.graph_objects)

    def __len__(self):
        return len(self.graph_objects)
    
    def __getitem__(self, index):
        return self.graph_objects[index]