# coding: utf-8
from __future__ import unicode_literals

import os
import json
import uuid

import tornado.ioloop
import tornado.web
import tornado.websocket


clients = []
WIDTH = 600;
HEIGHT = 600;


class Player(object):
    dx = 5
    dy = 5

    def __init__(self, _id, x, y):
        self.id = _id
        self.x = x
        self.y = y

    def up(self):
        if self.y - self.dy > 0:
            self.y -= self.dy;

    def down(self):
        if self.y + self.dy < HEIGHT:
            self.y += self.dy;

    def left(self):
        if self.x - self.dx > 0:
            self.x -= self.dx

    def right(self):
        if self.x + self.dx < WIDTH:
            self.x += self.dx

    def to_json(self):
        return json.dumps({
            'id': unicode(self.id),
            'x': self.x,
            'y': self.y,
        })


class Hello(tornado.websocket.WebSocketHandler):

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


class Main(tornado.web.RequestHandler):
    def get(self):
        self.render('index.html')


class Maze(tornado.web.RequestHandler):

    def get(self):
        from maze import MazeGenerator
        m = MazeGenerator().generate()

        response = {
            'size': len(m),
            'maze': m,
        }
        self.write(json.dumps(response))


settings = {
    'static_path': os.path.join(os.path.dirname(__file__), 'static'),
}


application = tornado.web.Application([
    (r'/', Main),
    (r'/maze', Maze),
    (r'/websocket', Hello),
    (r'/static/(.*)', tornado.web.StaticFileHandler, {'path': settings['static_path']}),
])


if __name__ == '__main__':
    application.listen(int(os.environ.get('PORT', '5000')))
    tornado.ioloop.IOLoop.instance().start()
