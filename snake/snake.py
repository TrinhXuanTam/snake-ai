from utils.constants import *
from pygame import draw, Rect, Surface
from random import randint
from math import ceil


class Snake:
    def __init__(self):
        start = OFFSET + BLOCK_SIZE * ceil(MAP_SIZE / 2)
        self.head = [start, start]
        self.body = [list(self.head)]
        self.direction = randint(0, 3)

    def move(self, direction):
        if direction != (self.direction + 2) % 4:
            self.direction = direction

        if self.direction == UP:
            self.head[1] -= BLOCK_SIZE
        elif self.direction == RIGHT:
            self.head[0] += BLOCK_SIZE
        elif self.direction == DOWN:
            self.head[1] += BLOCK_SIZE
        elif self.direction == LEFT:
            self.head[0] -= BLOCK_SIZE
        self.body.insert(0, list(self.head))

    def draw(self, surface):
        s = Surface((MAP_SIZE * BLOCK_SIZE, MAP_SIZE * BLOCK_SIZE))
        for x in self.body:
            rect = Rect(x[0] - OFFSET, x[1] - OFFSET, BLOCK_SIZE, BLOCK_SIZE)
            draw.rect(s, COLOR_WHITE, rect)
        surface.blit(s, (OFFSET, OFFSET))

    def eat(self, apple):
        if apple.position == self.head:
            return True

        self.body.pop()
        return False

    def collision_detected(self):
        y_wall = self.head[1] >= BLOCK_SIZE * MAP_SIZE + OFFSET or self.head[1] < OFFSET
        x_wall = self.head[0] >= BLOCK_SIZE * MAP_SIZE + OFFSET or self.head[0] < OFFSET
        return x_wall or y_wall or self.head in self.body[1:]
