import Vector

class Segment(object):
    def __init__(self, x0, y0, z0, x1, y1, z1):
        self.vector = Vector(x1-x0, y1-y0, z1-z0)

    def Length(self):
        return self.vector.Magnitude()