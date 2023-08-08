from utils.constants import *
from random import choice
from pygame import draw, Rect
from numpy import arange


class Apple:
    def __init__(self):
        self.max_coord = OFFSET + BLOCK_SIZE * MAP_SIZE
        self.coords = [x for x in arange(OFFSET, self.max_coord - BLOCK_SIZE, BLOCK_SIZE)]
        self.position = None

    def generate(self, snake):
        x = choice(self.coords)
        y = choice(self.coords)
        self.position = [x, y]

        if self.position in snake.body:
            self.generate(snake)

    def draw(self, surface):
        rect = Rect(self.position[0], self.position[1], BLOCK_SIZE, BLOCK_SIZE)
        draw.rect(surface, COLOR_RED, rect)
