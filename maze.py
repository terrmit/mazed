# coding: utf-8
import random

from config import conf


class MazeGenerator(object):

    def __init__(self, size):
        self.size = size
        self.chance_down_wall = conf.DOWN_WALL_CHANCE
        self.chance_mid_wall = conf.MID_WALL_CHANCE

    def generate(self):
        groups = []
        self.maze = []
        for i in xrange(self.size):
            self.maze.append(
                [{k: False for k in conf.DIRECTIONS} for j in xrange(self.size)]
            )

        for i in xrange(self.size):
            groups.append(i)
            self.maze[0][i]['up'] = True
            self.maze[self.size - 1][i]['down'] = True
            
        for i in xrange(self.size):
            if i != 0:
                for j in xrange(self.size):
                    self.maze[i][j]['up'] = self.maze[i - 1][j]['down']
                    self.maze[i][j]['down'] = self.maze[i - 1][j]['down']
            self.make_row(self.maze[i], groups)
        self.make_last_row(self.maze[self.size - 1], groups)

    def make_row(self, row, groups):
        row[0]['left'] = True
        row[self.size - 1]['right'] = True
        groups = self.make_mid_walls(row, groups)
        self.make_down_walls(row, groups)

    def make_down_walls(self, row, groups):
        left_side = 0
        for right_side in xrange(self.size - 1):
            if groups[right_side + 1] != groups[left_side] or right_side == self.size - 1:
                self.make_down_wall(row, left_side, right_side)
                left_side = right_side + 1
        self.make_down_wall(row, left_side, right_side + 1)

    def make_mid_walls(self, row, groups):
        if row[0]['down'] == True:
            for i in xrange(self.size):
                if i not in set(groups):
                    groups[0] = i
        row[0]['down'] == False
        
        for i in xrange(1, self.size):
            if row[i]['down'] == True:
                if random.random() < self.chance_mid_wall:
                    for j in xrange(self.size):
                        if j not in set(groups):
                            groups[i] = j
                    row[i]['left'] = True
                    row[i - 1]['right'] = True
                else:
                    groups[i] = groups[i - 1]
            else:
                if groups[i] == groups[i - 1] or random.random() < self.chance_mid_wall:
                    row[i]['left'] = True
                    row[i - 1]['right'] = True
                else:
                  self.unity(groups,groups[i], groups[i - 1])
            row[i]['down'] = False
        
        return groups

    def make_down_wall(self, row, left, right):
        walls = []
        walls.append(False)
        for i in xrange(left, right):
            walls.append(random.random() < self.chance_down_wall)
            
        random.shuffle(walls)
        
        for i in xrange(left, right + 1):
            row[i]['down'] = walls[i - left]

    def make_last_row(self, row, groups):
        row[0]['down'] = True
        for i in xrange(1, self.size):
            row[i]['down'] = True
            if groups[i] != groups[i - 1]:
                row[i]['left'] = False
                row[i - 1]['right'] = False
                self.unity(groups, groups[i], groups[i - 1])

    def unity(self, groups, set1 ,set2):
        for i in xrange(self.size):
            if groups[i] == set2:
                groups[i] = set1
