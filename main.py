# coding: utf-8
from __future__ import unicode_literals

import os
import json
import uuid

import tornado.ioloop
import tornado.web
import tornado.websocket

from maze import MazeGenerator

clients = []
WIDTH = 120  # blocks count
HEIGHT = 120

class Player(object):
    speed = 0.5

    def __init__(self, _id, x, y):
        self.id = _id
        self.x = x
        self.y = y

    def up(self):
        if self.y - self.speed > 0:
            self.y -= self.speed

    def down(self):
        if self.y + self.speed < HEIGHT:
            self.y += self.speed

    def left(self):
        if self.x - self.speed > 0:
            self.x -= self.speed

    def right(self):
        if self.x + self.speed < WIDTH:
            self.x += self.speed

    def to_json(self):
        return json.dumps({
            'id': unicode(self.id),
            'x': self.x,
            'y': self.y,
        })


class WSHandler(tornado.websocket.WebSocketHandler):
    def open(self):
        self.player = Player(uuid.uuid1(), WIDTH / 2, HEIGHT / 2)
        clients.append(self)
        for client in clients:
            client.write_message(self.player.to_json())

    def on_message(self, message):
        getattr(self.player, message)()
        for client in clients:
            client.write_message(self.player.to_json())

    def on_close(self):
        clients.remove(self)


class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('index.html')


class MazeHandler(tornado.web.RequestHandler):
    def get(self):
        response = {
            'size': len(mazeGenerator.maze),
            'maze': mazeGenerator.maze,
        }
        self.write(json.dumps(response))

settings = {
    'static_path': os.path.join(os.path.dirname(__file__), 'static'),
}

mazeGenerator = MazeGenerator(size=WIDTH)

application = tornado.web.Application([
    (r'/', IndexHandler),
    (r'/maze', MazeHandler),
    (r'/websocket', WSHandler),
    (r'/static/(.*)', tornado.web.StaticFileHandler, {'path': settings['static_path']}),
])

if __name__ == '__main__':
    application.listen(int(os.environ.get('PORT', '5000')))
    tornado.ioloop.IOLoop.instance().start()
