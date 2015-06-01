# coding: utf-8
import random
import json
import numpy as np
from copy import copy

from util import *


class MazeNode(object):
    __slots__ = ['up', 'down', 'left', 'right']

    def __init__(self):
        self.up, self.down, self.left, self.right = False, False, False, False

    def __getitem__(self, key):
        if key == -1:
            return self.up
        if key == 1:
            return self.down
        if key == -2:
            return self.left
        if key == 2:
            return self.right

    def __setitem__(self, key, value):
        if key == -1:
            self.up = value
            return
        if key == 1:
            self.down = value
            return
        if key == -2:
            self.left = value
            return
        if key == 2:
            self.right = value
            return


class Maze(np.ndarray):
    def __init__(self, *args, **kwargs):
        super(Maze, self).__init__(args, kwargs)
        self.rectangle = Rectangle(YX(), YX(*self.shape))

    def get_new_position(self, position, direction):

        tmp_direction = copy(direction)
        new_position = copy(position)

        dim = 1 if direction.y != 0 else 2

        if position[dim + 1] != int(position[dim + 1]):
            # we can't change direction in intermediate position
            return new_position

        if position[dim] != int(position[dim]):
            # move player to the nearest absolute position
            if tmp_direction[dim] > 0:
                distance_to_abs = round_up(position[dim]) - position[dim]
            else:
                distance_to_abs = position[dim] - round_down(position[dim])
            if abs(tmp_direction[dim]) > distance_to_abs:
                tmp_direction[dim] = sign(tmp_direction[dim]) * (abs(tmp_direction[dim]) - distance_to_abs)
                new_position[dim] += sign(tmp_direction[dim]) * distance_to_abs
            else:
                new_position[dim] += tmp_direction[dim]
                return new_position

        unit_direction = dim * sign(tmp_direction[dim])
        for i in xrange(0, round_down(abs(tmp_direction[dim])) + 1):
            i *= sign(tmp_direction[dim])
            # do we hit a wall?
            if (    dim == 1 and self[new_position.y + i][new_position.x][unit_direction]    ) or \
                (   dim == 2 and self[new_position.y][new_position.x + i][unit_direction]    ):
                new_position[dim] += i
                return new_position

        new_position[dim] += tmp_direction[dim]

        return new_position


class MazeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, MazeNode):
            return [obj.up, obj.down, obj.left, obj.right]
        elif isinstance(obj, Maze):
            return obj.tolist()
        else:
            return json.JSONEncoder.default(self, obj)


class MazeGenerator(object):

    def __init__(self, size, limit=100, chance=40):
        self.size = size.x
        self.limit = limit
        self.chance = chance
        self.maze = Maze((size.x, size.y), dtype=object)
        self.maze.flat = [MazeNode() for _ in self.maze.flat]
        self.generate()

    def generate(self):
        for i in xrange(self.size):
            if i != 0:
                for j in xrange(self.size):
                    self.maze[i][j].up = self.maze[i - 1][j].down
            self.make_row(self.maze[i], i)

    def make_row(self, row, row_number):
        row[0].left = True
        row[self.size - 1].right = True
        groups = self.make_mid_row(row)

        self.make_down_walls(row, groups)

        if row_number != self.size - 1:
            if not row_number:
                for column_number in xrange(self.size):
                    row[column_number].up = True
        else:
            for column_number in xrange(self.size):
                row[column_number].down = True

    def make_mid_row(self, row):
        groups = []
        for i in xrange(self.size):
            groups.append(1)

        self.make_left_walls(row, groups)
        return groups

    def make_down_walls(self, sells, groups):
        left_side = 0
        for right_side in xrange(self.size):
            if groups[right_side] != groups[left_side] or right_side == self.size - 1:
                self.make_down_wall(sells, left_side, right_side)
                left_side = right_side

    def make_left_walls(self, sells, groups):
        for i in xrange(1, self.size):
            groups[i] = groups[i - 1]
            if random.randint(0, self.limit) > self.chance:
                sells[i].left = True
                sells[i - 1].right = True
                groups[i] += 1

    def make_down_wall(self, sells, left, right):
        width = right - left
        k = 0
        for i in xrange(left, right + 1):
            if random.randint(0, self.limit) > self.chance and k < width - 1:
                sells[i].down = True
                k += 1
