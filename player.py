# coding: utf-8
import json


class Player(object):
    def __init__(self, id, position, speed=0.5):
        self.id = id
        self.position = position
        self.speed = speed

    def to_json(self):
        return json.dumps({
            'id': unicode(self.id),
            'x': self.position.x + 0.5,
            'y': self.position.y + 0.5,
        })