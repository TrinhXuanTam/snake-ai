from snake.snake import Snake
from snake.apple import Apple
from random import randint
from utils.constants import *
import pygame


class Game:
    def __init__(self):
        self.surface = pygame.display.set_mode((GAME_WINDOW_SIZE, GAME_WINDOW_SIZE))
        self.clock = pygame.time.Clock()
        self.snake = Snake()
        self.apple = Apple()
        self.score = 0
        self.direction = randint(0, 3)
        pygame.display.set_caption("Snake AI")

    def __draw_border__(self):
        self.surface.fill(COLOR_BLACK)
        border = pygame.Rect(OFFSET - 1, OFFSET - 1, MAP_SIZE * BLOCK_SIZE + 2, MAP_SIZE * BLOCK_SIZE + 2)
        pygame.draw.rect(self.surface, COLOR_WHITE, border)

    def __control__(self):
        for event in pygame.event.get():
            keys = pygame.key.get_pressed()
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if keys[pygame.K_UP]:
                self.direction = UP
            elif keys[pygame.K_RIGHT]:
                self.direction = RIGHT
            elif keys[pygame.K_DOWN]:
                self.direction = DOWN
            elif keys[pygame.K_LEFT]:
                self.direction = LEFT

    def start_game(self):
        self.apple.generate(self.snake)
        self.__draw_border__()
        self.surface.fill(COLOR_BLACK, pygame.Rect(OFFSET, OFFSET, BLOCK_SIZE * MAP_SIZE, BLOCK_SIZE * MAP_SIZE))
        while True:
            self.snake.draw(self.surface)
            self.apple.draw(self.surface)
            pygame.display.set_caption("SCORE:" + str(self.score))
            pygame.display.update()
            self.clock.tick(FRAME_RATE)
            pygame.display.update()
            self.__control__()
            self.snake.move(self.direction)
            if self.snake.collision_detected():
                break
            elif self.snake.eat(self.apple):
                self.score += 1
                self.apple.generate(self.snake)
