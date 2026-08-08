class Curve:
    def __init__(self):
        pass
    
    def point(self, t):
        """Return the graph coordinate (x, y) at time t."""
        raise NotImplementedError

    def parameter_interval(self, renderer):
        """Return the parameter interval of the function (domain)."""
        raise NotImplementedError

    def inverse(self, tMin, tMax):
        """Return the inverse of the function."""
        raise NotImplementedError

    def derivative(self):
        """Return the derivative of the function."""
        raise NotImplementedError
    