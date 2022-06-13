# A function to read in the definition of a river from a file

from vec2 import *

def readFromFile(filename):
    north = []
    south = []
    islands = []

    f = open(filename, 'r')

    sequence = north                    # this is intended to be an alias
    for line in f:
        if (line[0] != "#"):            # only process uncommented lines
            # identify what sequence we will add this point to
            stripped = line.rstrip()
            if (len(stripped) != 0):     # only process non-empty liness
                if (stripped == "north"):
                    sequence = north        # intentionally an alias
                elif (stripped == "south"):
                    sequence = south        # intentionally an alias
                elif (stripped == "island"):
                    sequence = []
                    islands.append(sequence)
                else:
                    split = stripped.split(" ")
                    sequence.append(Vec2(split[0], split[1]))

    f.close()

    return north, south, islands