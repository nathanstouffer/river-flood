# A class that represents a simple polygon. That is, a sequence of points defining a polygon without holes that does
# not intersect itself

import numpy as np
from vec2 import *


class Polygon:

    def __init__(self, points):
        self.points = np.array(points, dtype=Vec2)

    def __getitem__(self, idx):
        return self.points[idx]

    def num_points(self):
        return len(self.points)

    def is_x_monotone(self):
        # TODO (stouff) implement this method
        return True
