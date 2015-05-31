# coding: utf-8
from __future__ import unicode_literals

import os
import json
import uuid

import tornado.ioloop
import tornado.web
import tornado.websocket

from util import YX
from maze import MazeGenerator, MazeEncoder
from player import Player

clients = []
SIZE = YX(y=60, x=60)
MAZE = MazeGenerator(size=SIZE).maze


class WSHandler(tornado.websocket.WebSocketHandler):
    def open(self):
        self.player = Player(uuid.uuid1(), MAZE, YX(SIZE.y / 2, SIZE.x / 2,), speed=0.5)
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
            'size': len(MAZE),
            'maze': MAZE,
        }
        self.write(json.dumps(response, cls=MazeEncoder))

settings = {
    'static_path': os.path.join(os.path.dirname(__file__), 'static'),
}

application = tornado.web.Application([
    (r'/', IndexHandler),
    (r'/maze', MazeHandler),
    (r'/websocket', WSHandler),
    (r'/static/(.*)', tornado.web.StaticFileHandler, {'path': settings['static_path']}),
])

if __name__ == '__main__':
    application.listen(int(os.environ.get('PORT', '5000')))
    tornado.ioloop.IOLoop.instance().start()
