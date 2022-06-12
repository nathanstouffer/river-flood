# a class defining a Vec2 to store two floating point numbers in (x,y) \in R^2

class Vec2:

    def __init__(self, x = 0.0, y = 0.0):
        self.x = float(x)
        self.y = float(y)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __add__(self, other):
        x = self.x + other.x
        y = self.y + other.y
        return Vec2(x, y)

    def __sub__(self, other):
        return self + (other * -1.0)

    def __mul__(self, scalar):
        return Vec2(scalar * self.x, scalar * self.y)

    def dot(self, other):
        return self.x * other.x + self.y + other.y

    def __str__(self):
        return "({0}, {1})".format(self.x, self.y)