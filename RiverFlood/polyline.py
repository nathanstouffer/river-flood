# A class that represents a polyline. That is, a sequence of points defining connected line segments in the plane

import numpy as np
from vec2 import *


class Polyline:

    def __init__(self, points):
        self.points = np.array(points, dtype=Vec2)

    def __getitem__(self, idx):
        return self.points[idx]

    def num_points(self):
        return len(self.points)

    def is_x_monotone(self):
        prev = self[0]
        for i in range(1, len(self.points)):
            cur = self[i]
            if (cur.x <= prev.x):
                return False
            prev = cur
        return True
