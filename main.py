# coding: utf-8
from __future__ import unicode_literals

import os
import json
import uuid

import tornado.ioloop
import tornado.web
import tornado.websocket

from util import XY
from maze import MazeGenerator
from player import Player

clients = []
SIZE = XY(x=60, y=60)


class WSHandler(tornado.websocket.WebSocketHandler):
    def open(self):
        self.player = Player(uuid.uuid1(), SIZE, XY(SIZE.x / 2, SIZE.y / 2), speed=0.5)
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

mazeGenerator = MazeGenerator(size=SIZE.x)

application = tornado.web.Application([
    (r'/', IndexHandler),
    (r'/maze', MazeHandler),
    (r'/websocket', WSHandler),
    (r'/static/(.*)', tornado.web.StaticFileHandler, {'path': settings['static_path']}),
])

if __name__ == '__main__':
    application.listen(int(os.environ.get('PORT', '5000')))
    tornado.ioloop.IOLoop.instance().start()
