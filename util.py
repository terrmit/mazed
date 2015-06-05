# coding: utf-8
from fractions import Fraction


class Point(object):
    __slots__ = ['x', 'y']

    def __init__(self, x=0, y=0):
        self.x = Fraction(x)
        self.y = Fraction(y)

    def __add__(self, another):
        return Point(self.x + another.x, self.y + another.y)

    def __iadd__(self, another):
        self.x += another.x
        self.y += another.y
        return self

    def __mul__(self, other):
        return Point(self.x * other, self.y * other)

    def __repr__(self):
        return '({x}, {y})'.format(x=self.x, y=self.y)
