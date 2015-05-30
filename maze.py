# coding: utf-8
import random


class MazeGenerator(object):

    def __init__(self, size=30, limit=100, chance=40):
        self.size = size
        self.limit = limit
        self.chance = chance

    def generate(self):
        maze = []

        for i in range(self.size):
            maze.append([])

            for j in range(self.size):
                maze[i].append({})
                maze[i][j]['up'] = False
                maze[i][j]['down'] = False
                maze[i][j]['left'] = False
                maze[i][j]['right'] = False

        for i in range(self.size):
            if i != 0:
                for j in range(self.size):
                    maze[i][j]['up'] = maze[i - 1][j]['down']
            self.make_row(maze[i], i)

        return maze

    def make_row(self, row, row_number):
        row[0]['left'] = True
        row[self.size - 1]['right'] = True
        groups = self.make_mid_row(row)

        self.make_down_walls(row, groups)

        if row_number != self.size - 1:
            if not row_number:
                for column_number in range(self.size):
                    row[column_number]['up'] = True
        else:
            for column_number in range(self.size):
                row[column_number]['down'] = True

    def make_mid_row(self, row):
        groups = []
        for i in range(self.size):
            groups.append(1)

        self.make_left_walls(row, groups)
        return groups

    def make_down_walls(self, sells, groups):
        left_side = 0
        for right_side in range(self.size):
            if groups[right_side] != groups[left_side] or right_side == self.size - 1:
                self.make_down_wall(sells, left_side, right_side)
                left_side = right_side

    def make_left_walls(self, sells, groups):
        for i in range(1, self.size):
            groups[i] = groups[i - 1]
            if random.randint(0, self.limit) > self.chance:
                sells[i]['left'] = True
                sells[i - 1]['right'] = True
                groups[i] += 1

    def make_down_wall(self, sells, left, right):
        width = right - left
        k = 0
        for i in range(left, right + 1):
            if random.randint(0, self.limit) > self.chance and k < width - 1:
                sells[i]['down'] = True
                k += 1
