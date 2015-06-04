# coding: utf-8
from __future__ import unicode_literals

import os
import json
import uuid

import tornado.ioloop
import tornado.web
import tornado.websocket

from util import Point
from game import Game
from player import Player


clients = []


class WSHandler(tornado.websocket.WebSocketHandler):
    def open(self):
        self.game = Game()
        x = y = self.game.size / 2
        self.player = Player(uuid.uuid1(), Point(x, y))
        self.game.players[self.player.id] = self.player
        clients.append(self)
        for client in clients:
            client.write_message(self.player.to_json())

    def on_message(self, message):
        if message not in ('up', 'down', 'left', 'right'):
            return
        self.game.process_player_move(self.player.id, message)
        for client in clients:
            client.write_message(self.game.players[self.player.id].to_json())

    def on_close(self):
        clients.remove(self)


class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('index.html')


class MazeHandler(tornado.web.RequestHandler):
    def get(self):
        maze = Game().maze
        response = {
            'size': len(maze),
            'maze': maze,
        }
        self.write(json.dumps(response))


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
