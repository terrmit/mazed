# coding: utf-8
from util import Point
from maze import MazeGenerator
from config import conf


class Game(object):

    _instance = None

    VECTOR_MAP = {
        'up': Point(0, -1),
        'down': Point(0, 1),
        'left': Point(-1, 0),
        'right': Point(1, 0),
    }

    # Game must be Singleton
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(Game, cls).__new__(cls, *args, **kwargs)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return

        self.size = conf.MAZE_SIZE
        self.maze = self._get_maze()
        self.players = {}
        self._initialized = True

    def _get_maze(self):
        mg = MazeGenerator(self.size)
        mg.generate()
        return mg.maze

    def is_wall_on_way(self, position, delta):
        cell = self.maze[int(position.y)][int(position.x)]
        return (
            delta.x > 0 and cell['right'] or
            delta.x < 0 and cell['left'] or
            delta.y > 0 and cell['down'] or
            delta.y < 0 and cell['up']
        )

    def _get_delta(self, player, direction):
        return self.VECTOR_MAP.get(direction) * player.speed

    def process_player_move(self, player_id, direction):
        player = self.players.get(player_id)
        delta = self._get_delta(player, direction)

        if (delta.x and player.position.x.denominator != 1 or
                delta.y and player.position.y.denominator != 1 or
                player.position.x.denominator == 1 and 
                player.position.y.denominator == 1 and
                not self.is_wall_on_way(player.position, delta)):
            
            player.move(delta)
