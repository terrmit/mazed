# coding: utf-8
import json
from util import YX


class Player(object):
    def __init__(self, id, maze, position, speed):
        self.id = id
        self.maze = maze
        self.position = position
        self.speed = speed

    def move(self, direction):
        self.position = self.maze.get_new_position(self.position, direction)

    def up(self):
        self.move(YX(y=-self.speed))

    def down(self):
        self.move(YX(y=self.speed))

    def left(self):
        self.move(YX(x=-self.speed))

    def right(self):
        self.move(YX(x=self.speed))

    def to_json(self):
        return json.dumps({
            'id': unicode(self.id),
            'x': self.position.x + 0.5,
            'y': self.position.y + 0.5,
        })