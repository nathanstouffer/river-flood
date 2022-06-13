# A python file to create a river and make some queries

import numpy as np
from inspect import signature
import river as riv
import read

EPS = 0.00000001

def equals(x, y, eps = 0.0):
    return abs(x - y) < eps

def rectangle_test():
    north, south, islands = read.readFromFile("../rivers/rectangle.riv")
    river = riv.River(north, south, islands)
    for t in np.linspace(0, 1, 100):
        if (not equals(river.width(t), 5.0, EPS)):
            return False
    return True


def rectangle_one_hole_test():
    north, south, islands = read.readFromFile("../rivers/rectangle-one-hole.riv")
    river = riv.River(north, south, islands)
    for t in np.linspace(0, 1, 100):
        if (t <= 0.3):
            if (not equals(river.width(t), 5, EPS)):
                return False
        if (t > 3.0 and t < 4.0):
            if (not equals(river.width(t), -2.666666666 * (t - 3.0) + 5, EPS)):
                return False
        if (t >= 4.0 and t <= 6.0):
            if (not equals(river.width(t), 2.33333333333, EPS)):
                return False
        if (t > 6.0 and t < 7.0):
            if (not equals(river.width(t), 2.666666666 * (t - 6.0) + 2.33333333333, EPS)):
                return False
        if (t >= 7.0):
            if (not equals(river.width(t), 5.0, EPS)):
                return False
    return True


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    tests = [ rectangle_test, rectangle_one_hole_test ]

    for test in tests:
        result = test()
        if (result == True):
            print("\033[92mPassed {0}".format(test.__name__))
        else:
            print("\033[91mFailed {0}".format(test.__name__))