# class to represent a line in R^2

class Line:

    def __init__(self, m, b):
        self.m = m
        self.b = b

    def at(self, x):
        return self.m * x + self.b