# A class that represents a river composed of a north shoreline, south shoreline, and polygon islands in the middle

from polyline import *
from polygon import *


class River:

    def __init__(self, north, south, islands):
        self.north = Polyline(north)
        self.south = Polyline(south)
        islandsList = []
        for island in islands:
            islandsList = Polygon(island)
        self.islands = np.array(islandsList)
        if (not self.is_valid()):
            raise AssertionError("river configuration is not valid")

    def is_valid(self):
        # check that each shoreline is x-monotone
        if (not self.north.is_x_monotone()):
            return False
        if (not self.south.is_x_monotone()):
            return False

        # check that the shorelines start/end at the same x coordinates
        if (self.north[0].x != self.south[0].x):
            return False
        if (self.north[-1].x != self.south[-1].x):
            return False

        # check that the north shoreline is above the south shoreline at the beginning
        if (self.north[0].y <= self.south[0].y):
            return False

        # TODO (stouff) check that shorelines do not cross

        # check that each polygon defining an island is x-monotone
        for island in self.islands:
            if (not island.is_x_monotone()):
                return False

        # TODO (stouff) check that no event points have the same x-coordinate
        # TODO (stouff) check that islands are all inside the shorelines

        # passed all checks, we can return True
        return True

    # we expect t to be in [0, 1]
    def width(self, t):
        if (t < 0.0 or t > 1.0):
            raise AssertionError("t is outside [0, 1]")

        if (t == 0.0):
            return self.north[0].y - self.south[0].y
        elif (t == 1.0):
            return self.north[-1].y - self.south[-1].y

        # TODO (stouff) implement this method

        return 0

    def min_width(self):
        # TODO (stouff) implement this method
        return 0

    # method that returns the number of event points to be used on the sweep line
    def num_events(self):
        count = 0                                   # start with 0 event points
        count += self.north.num_points() - 1        # add number of events for north shore line (exclude beginning -- it is implicit)
        count += self.south.num_points() - 2        # add number of events for south shore line (exclude beginning/end -- we double counted the end)
        for island in self.islands:                 # for each island, add the number of points defining the polygon
            count += island.num_points()

    # method that returns an array of event points to be used in the sweep line algorithm
    def events(self):
        # TODO (stouff) implement this method
        pass

    # method that returns a sorted array of event points
    def sorted_events(self):
        # TODO (stouff) implement this method
        pass
