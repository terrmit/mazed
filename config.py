# cofing: utf-8
from fractions import Fraction


class Config(object):
    DIRECTIONS = ('up', 'down', 'left', 'right')
    MAZE_SIZE = 40
    PLAYER_SPEED = Fraction(1, 1)
    MID_WALL_CHANCE = 0.3
    DOWN_WALL_CHANCE = 0.7


conf = Config
