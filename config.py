# cofing: utf-8
from fractions import Fraction


class Config(object):
    DIRECTIONS = ('up', 'down', 'left', 'right')
    MAZE_SIZE = 40
    PLAYER_SPEED = Fraction(1, 5)
    WALL_CHANCE = 0.4


conf = Config
