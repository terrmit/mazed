# coding: utf-8
import random


class MazeGenerator(object):

    def __init__(self, size=120, limit=100, chance=40):
        self.size = size
        self.limit = limit
        self.chance = chance
        self.maze = []
        self.generate()

    def generate(self):
        for i in xrange(self.size):
            self.maze.append([])

            for j in xrange(self.size):
                self.maze[i].append({})
                self.maze[i][j]['up'] = False
                self.maze[i][j]['down'] = False
                self.maze[i][j]['left'] = False
                self.maze[i][j]['right'] = False

        for i in xrange(self.size):
            if i != 0:
                for j in xrange(self.size):
                    self.maze[i][j]['up'] = self.maze[i - 1][j]['down']
            self.make_row(self.maze[i], i)

    def make_row(self, row, row_number):
        row[0]['left'] = True
        row[self.size - 1]['right'] = True
        groups = self.make_mid_row(row)

        self.make_down_walls(row, groups)

        if row_number != self.size - 1:
            if not row_number:
                for column_number in xrange(self.size):
                    row[column_number]['up'] = True
        else:
            for column_number in xrange(self.size):
                row[column_number]['down'] = True

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
                sells[i]['left'] = True
                sells[i - 1]['right'] = True
                groups[i] += 1

    def make_down_wall(self, sells, left, right):
        width = right - left
        k = 0
        for i in xrange(left, right + 1):
            if random.randint(0, self.limit) > self.chance and k < width - 1:
                sells[i]['down'] = True
                k += 1
