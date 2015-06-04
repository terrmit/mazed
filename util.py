# coding: utf-8

class YX(object):
    __slots__ = ['x', 'y']

    def __init__(self, y=0, x=0):
        self.y = y
        self.x = x

    def __add__(self, another):
        return YX(self.y + another.y, self.x + another.x)

    def __iadd__(self, another):
        self.y += another.y
        self.x += another.x
        return self

    def __getitem__(self, key):
        if key in (1, 3):  # 3 is for cycle
            return self.y
        return self.x

    def __setitem__(self, key, value):
        if key in (1, 3):  # 3 is for cycle
            self.y = value
        else:
            self.x = value

    def __mul__(self, other):
        return YX(self.y * other, self.x * other)



# 0: x1, y1 ........
# 1: ...............
# 2: .........x2, y2
class Rectangle(object):
    __slots__ = ['point1', 'point2']

    def __init__(self, point1, point2):
        self.point1 = point1
        self.point2 = point2
        if self.point1.x >= self.point2.x:
            self.point1.x, self.point2.x = self.point2.x, self.point1.x
        if self.point1.y >= self.point2.y:
            self.point1.y, self.point2.y = self.point2.y, self.point1.y

    def includes_point(self, point):
        return self.point1.x <= point.x <= self.point2.x and self.point1.y <= point.y <= self.point2.y

    def includes_circle(self, point, radius=0.5):
        return (self.point1.x + radius) <= point.x <= (self.point2.x - radius) and \
               (self.point1.y + radius) <= point.y <= (self.point2.y - radius)


def round_up(floating_point):
    return round(floating_point + 0.5)


def round_down(floating_point):
    return int(floating_point)

from math import copysign
sign = lambda x: copysign(1, x)
