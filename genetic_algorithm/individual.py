from snake.snake import Snake
from AI.neural_network import NeuralNetwork
from snake.apple import Apple
from operator import sub
from utils.constants import *


class Individual:
    def __init__(self):
        self.neural_net = NeuralNetwork()
        self.snake = Snake()
        self.apple = Apple()
        self.fitness = 0

    def __look_for_apple__(self, vision):
        vision.extend([0] * 8)
        diff = list(map(sub, self.apple.position, self.snake.head))
        if diff[0] == 0 and diff[1] < 0:
            vision[0] = 1
        elif abs(diff[0]) == abs(diff[1]) and diff[0] > 0 and diff[1] < 0:
            vision[1] = 1
        elif diff[1] == 0 and diff[0] > 0:
            vision[2] = 1
        elif abs(diff[0]) == abs(diff[1]) and diff[0] > 0 and diff[1] > 0:
            vision[3] = 1
        elif diff[0] == 0 and diff[1] > 0:
            vision[4] = 1
        elif abs(diff[0]) == abs(diff[1]) and diff[0] < 0 and diff[1] > 0:
            vision[5] = 1
        elif diff[1] == 0 and diff[0] < 0:
            vision[6] = 1
        elif abs(diff[0]) == abs(diff[1]) and diff[0] < 0 and diff[1] < 0:
            vision[7] = 1

    def __check_wall__(self, x, y, vision):
        distance = 0
        curr = list(self.snake.head)
        while True:
            y_wall = curr[1] >= BLOCK_SIZE * MAP_SIZE + OFFSET or curr[1] < OFFSET
            x_wall = curr[0] >= BLOCK_SIZE * MAP_SIZE + OFFSET or curr[0] < OFFSET
            if x_wall or y_wall:
                vision.append(1 / distance)
                return
            curr[0] += x * BLOCK_SIZE
            curr[1] += y * BLOCK_SIZE
            distance += 1

    def __look_for_wall__(self, vision):
        if self.snake.direction != DOWN:
            self.__check_wall__(0, -1, vision)
        else:
            vision.append(0)

        self.__check_wall__(1, -1, vision)

        if self.snake.direction != LEFT:
            self.__check_wall__(1, 0, vision)
        else:
            vision.append(0)

        self.__check_wall__(1, 1, vision)

        if self.snake.direction != UP:
            self.__check_wall__(0, 1, vision)
        else:
            vision.append(0)

        self.__check_wall__(-1, 1, vision)

        if self.snake.direction != RIGHT:
            self.__check_wall__(-1, 0, vision)
        else:
            vision.append(0)
        self.__check_wall__(-1, -1, vision)

    def __check_body__(self, x, y, vision):
        distance = 1
        curr = list(self.snake.head)
        curr[0] += x * BLOCK_SIZE
        curr[1] += y * BLOCK_SIZE
        while True:
            y_wall = curr[1] >= BLOCK_SIZE * MAP_SIZE + OFFSET or curr[1] < OFFSET
            x_wall = curr[0] >= BLOCK_SIZE * MAP_SIZE + OFFSET or curr[0] < OFFSET
            if x_wall or y_wall:
                vision.append(0)
                return
            elif curr in self.snake.body:
                vision.append(1 / distance)
                return
            curr[0] += x * BLOCK_SIZE
            curr[1] += y * BLOCK_SIZE
            distance += 1

    def __look_for_body__(self, vision):
        if self.snake.direction != DOWN:
            self.__check_body__(0, -1, vision)
        else:
            vision.append(0)
        self.__check_body__(1, -1, vision)
        if self.snake.direction != LEFT:
            self.__check_body__(1, 0, vision)
        else:
            vision.append(0)
        self.__check_body__(1, 1, vision)
        if self.snake.direction != UP:
            self.__check_body__(0, 1, vision)
        else:
            vision.append(0)
        self.__check_body__(-1, 1, vision)
        if self.snake.direction != RIGHT:
            self.__check_body__(-1, 0, vision)
        else:
            vision.append(0)
        self.__check_body__(-1, -1, vision)

    def look(self, vision):
        self.__look_for_apple__(vision)
        self.__look_for_wall__(vision)
        self.__look_for_body__(vision)

    def move(self):
        vision = []
        self.look(vision)
        res = list(self.neural_net.feed(vision))
        direction = res.index(max(res))
        self.snake.move(direction)

    def play(self):
        score = 1
        moves_left = MOVES_LEFT
        time_alive = 0
        self.apple.generate(self.snake)
        while True:
            if self.snake.collision_detected() or moves_left == 0:
                self.fitness = (time_alive ** 2) * score
                return
            elif self.snake.eat(self.apple):
                score += 1
                if moves_left + MOVES_LEFT > MOVES_LEFT * MOVES_UPPER_BOUND:
                    moves_left = MOVES_LEFT * MOVES_UPPER_BOUND
                else:
                    moves_left += MOVES_LEFT
                self.apple.generate(self.snake)
            self.move()
            moves_left -= 1
            time_alive += 1
