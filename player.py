# coding: utf-8
import json

from config import conf


class Player(object):
    def __init__(self, id, position):
        self.id = id
        self.position = position
        self.speed = conf.PLAYER_SPEED

        size = conf.MAZE_SIZE
        self.area = [[False for i in range(size)] for j in range(size)]

    def move(self, delta):
        self.position += delta
        self.discover_area()

    def discover_area(self):
        x = int(round(self.position.x))
        y = int(round(self.position.y))
        self.area[x][y] = True

    def to_json(self):
        return json.dumps({
            'id': unicode(self.id),
            'x': self.position.x + 0.5,
            'y': self.position.y + 0.5,
            'area': self.area,
        })
