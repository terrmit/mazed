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
from config import conf


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

        for _id, player in self.game.players.items():
            if _id != self.player.id:
                self.write_message(player.to_json())


    def on_message(self, message):
        if message not in conf.DIRECTIONS:
            return

        self.game.process_player_move(self.player.id, message)

        for client in clients:
            client.write_message(self.game.players[self.player.id].to_json())

    def on_close(self):
        clients.remove(self)
        self.game.players.pop(self.player.id, None)


class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('index.html')


class MazeHandler(tornado.web.RequestHandler):
    def get(self):
        maze = Game().maze
        response = {
            'size': conf.MAZE_SIZE,
            'maze': maze,
        }
        self.write(json.dumps(response))


STATIC_PATH = os.path.join(os.path.dirname(__file__), 'static')


application = tornado.web.Application([
    (r'/', IndexHandler),
    (r'/maze', MazeHandler),
    (r'/websocket', WSHandler),
    (r'/static/(.*)', tornado.web.StaticFileHandler, {'path': STATIC_PATH}),
])


if __name__ == '__main__':
    application.listen(int(os.environ.get('PORT', '5000')))
    tornado.ioloop.IOLoop.instance().start()
