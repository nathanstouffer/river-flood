# A class that represents a river composed of a north shoreline, south shoreline, and polygon islands in the middle

from enum import Enum
from polyline import *
from polygon import *


class EventType(Enum):
    UPPER_SHORE = 0
    LOWER_SHORE = 1
    BEG_ISLAND = 2
    END_ISLAND = 3
    UPPER_ISLAND = 4
    LOWER_ISLAND = 5


class Event:

    # container is an alias to the containing geometry (polyline or polygon) of this event point
    # idx is the index of this point on the container
    def __init__(self, eventType, x, container, idx):
        self.eventType = eventType
        self.x = x
        self.container = container
        self.idx = idx

    def __lt__(self, other):
        return self.x < other.x


class River:

    def __init__(self, north, south, islands):
        self.north = Polyline(north)
        self.south = Polyline(south)
        islandsList = []
        for island in islands:
            islandsList.append(Polygon(island))
        self.islands = np.array(islandsList, dtype=Polygon)
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

        # TODO (stouff) check that islands are all ordered counter-clockwise
        # TODO (stouff) check that islands are all inside the shorelines

        # check that no event points have the same x-coordinate
        used = set()
        for event in self.events():
            if (event.x in used):
                return False
            used.add(event.x)

        # passed all checks, we can return True
        return True

    # we expect t to be in [0, 1]
    def width(self, t):
        if (t < 0.0 or t > 1.0):
            raise AssertionError("t is outside [0, 1]")

        north = self.north
        south = self.south

        if (t == 0.0):
            return north[0].y - south[0].y
        elif (t == 1.0):
            return north[-1].y - south[-1].y

        # compute the x value that we wish to know the width at
        query_x = t * (north[-1] - north[0]).x

        north_m = north[0].slope_to(north[1])
        south_m = south[0].slope_to(south[1])
        m = north_m - south_m
        x_0 = north[0].x
        y_0 = north[0].y - south[0].y
        for event in self.sorted_events():
            if (event.x > query_x):  # iterate over events until we have the line with the correct domain
                break
            else:
                x = event.x
                container = event.container
                i = event.idx

                # compute the new value for y_0
                y_0 = m * (x - x_0) + y_0
                x_0 = x
                # compute the new value for m
                if (event.eventType == EventType.UPPER_SHORE):
                    prev_seg_m = container[i - 1].slope_to(container[i])
                    next_seg_m = container[i].slope_to(container[(i + 1) % container.num_points()])
                    m = m - prev_seg_m + next_seg_m
                elif (event.eventType == EventType.LOWER_SHORE):
                    prev_seg_m = container[i - 1].slope_to(container[i])
                    next_seg_m = container[i].slope_to(container[(i + 1) % container.num_points()])
                    m = m + prev_seg_m - next_seg_m
                elif (event.eventType == EventType.BEG_ISLAND):
                    upper_m = container[i].slope_to(container[i - 1])
                    lower_m = container[i].slope_to(container[(i + 1) % container.num_points()])
                    m = m - upper_m + lower_m
                elif (event.eventType == EventType.END_ISLAND):
                    upper_m = container[i].slope_to(container[(i + 1) % container.num_points()])
                    lower_m = container[i].slope_to(container[i - 1])
                    m = m + upper_m - lower_m
                elif (event.eventType == EventType.UPPER_ISLAND):
                    prev_seg_m = container[(i + 1) % container.num_points()].slope_to(container[i])
                    next_seg_m = container[i].slope_to(container[i - 1])
                    m = m + prev_seg_m - next_seg_m
                elif (event.eventType == EventType.LOWER_ISLAND):
                    prev_seg_m = container[i - 1].slope_to(container[i])
                    next_seg_m = container[i].slope_to(container[(i + 1) % container.num_points()])
                    m = m - prev_seg_m + next_seg_m

        return m * (query_x - x_0) + y_0

    def min_width(self):
        # TODO (stouff) implement this method
        return 0

    # method that returns the number of event points to be used on the sweep line
    # the beginning/end of the shore line are not event points and are handled differently
    def num_events(self):
        count = 0  # start with 0 event points
        count += self.north.num_points() - 2  # add number of events for north shore line (exclude beginning/end)
        count += self.south.num_points() - 2  # add number of events for south shore line (exclude beginning/end)
        for island in self.islands:  # for each island, add the number of points defining the polygon
            count += island.num_points()
        return count

    # method that returns an array of event points to be used in the sweep line algorithm
    def events(self):
        events = np.empty(self.num_events(), dtype=Event)

        idx = 0
        # add events from the north shore
        north = self.north
        for i in range(1, north.num_points() - 1):
            events[idx] = Event(EventType.UPPER_SHORE, north[i].x, north, i)
            idx +=1

        # add events from the south shore
        south = self.south
        for i in range(1, south.num_points() - 1):
            events[idx] = Event(EventType.LOWER_SHORE, south[i].x, south, i)
            idx += 1

        # add events from each island
        for island in self.islands:
            for i in range(0, island.num_points()):
                prev = island[i - 1]
                point = island[i]
                next = island[(i + 1) % island.num_points()]

                eventType = EventType.BEG_ISLAND
                if (point.x < prev.x and point.x < next.x):
                    eventType = EventType.BEG_ISLAND
                elif (point.x > prev.x and point.x > next.x):
                    eventType = EventType.END_ISLAND
                elif (point.x < prev.x and point.x > next.x):
                    eventType = EventType.UPPER_ISLAND
                elif (point.x > prev.x and point.x < next.x):
                    eventType = EventType.LOWER_ISLAND

                events[idx] = Event(eventType, point.x, island, i)
                idx += 1

        return events

    # method that returns a sorted array of event points
    def sorted_events(self):
        events = self.events()
        events.sort(kind='heapsort')
        return events
