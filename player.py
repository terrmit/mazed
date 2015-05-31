# coding: utf-8
import json
from util import YX


class Player(object):
    def __init__(self, id, maze, position, speed):
        self.id = id
        self.maze = maze
        self.size = YX(*self.maze.shape)
        self.position = position
        self.speed = speed

    def up(self):
        if self.position.y - self.speed > 0:
            self.position.y -= self.speed

    def down(self):
        if self.position.y + self.speed < self.size.y:
            self.position.y += self.speed

    def left(self):
        if self.position.x - self.speed > 0:
            self.position.x -= self.speed

    def right(self):
        if self.position.x + self.speed < self.size.x:
            self.position.x += self.speed

    def to_json(self):
        return json.dumps({
            'id': unicode(self.id),
            'x': self.position.x,
            'y': self.position.y,
        })