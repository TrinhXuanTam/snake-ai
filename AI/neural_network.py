from numpy import exp, transpose, random, dot, array, maximum, tanh, max
from utils.constants import *
from pygame import gfxdraw, Surface, SRCALPHA, font
from math import floor


def sigmoid(x):
    return 1.0 / (1.0 + exp(-x))


def relu(x):
    return maximum(0, x)


def activation(x):
    return relu(x)


class NeuralNetwork:
    def __init__(self):
        self.weights = []
        self.biases = []
        self.node_activation = []
        self.node_coords = []
        self.architecture = [INPUT_LAYER] + list(HIDDEN_LAYERS) + [OUTPUT_LAYER]
        self.__randomize()

    def __randomize(self):
        for i in range(len(self.architecture) - 1):
            self.weights.append(random.uniform(-1, 1, size=(self.architecture[i + 1], self.architecture[i])))
            self.biases.append(transpose(random.uniform(-1, 1, size=self.architecture[i + 1])))

    def feed(self, x):
        input = array(x)
        output = None
        self.node_activation = []
        self.node_activation.append(list(input))
        length = len(self.weights)
        for i in range(length - 1):
            output = activation(dot(self.weights[i], input) + self.biases[i])
            input = output
            self.node_activation.append(list(output))

        output = sigmoid(dot(self.weights[length - 1], input) + self.biases[length - 1])
        self.node_activation.append(list(output))
        return output

    def draw(self, surface):
        s = Surface((NEURAL_NETWORK_WINDOW_SIZE, NEURAL_NETWORK_WINDOW_SIZE), SRCALPHA, 32)
        for i in range(len(self.node_coords)):
            for j in range(len(self.node_coords[i])):
                intensity = tanh(self.node_activation[i][j]) * 255
                color = tuple([intensity] * 3 + [255]) if intensity > 0 else COLOR_BLACK
                gfxdraw.filled_circle(s, self.node_coords[i][j][0] - GAME_WINDOW_SIZE, self.node_coords[i][j][1],
                                      NODE_SIZE, color)
                gfxdraw.aacircle(s, self.node_coords[i][j][0] - GAME_WINDOW_SIZE, self.node_coords[i][j][1], NODE_SIZE,
                                 COLOR_WHITE)

        last = len(self.node_activation) - 1
        chosen = self.node_activation[last].index(max(self.node_activation[last]))
        coord = self.node_coords[last][chosen]
        gfxdraw.filled_circle(s, coord[0] - GAME_WINDOW_SIZE, coord[1], NODE_SIZE, COLOR_GREEN)
        gfxdraw.aacircle(s, coord[0] - GAME_WINDOW_SIZE, coord[1], NODE_SIZE, COLOR_WHITE)
        surface.blit(s, (GAME_WINDOW_SIZE, 0))

    def __create_text(self, text, size):
        text = font.Font(FONT, size).render(text, True, COLOR_WHITE)
        return text

    def init_draw(self, surface):
        horizontal_spacing = NEURAL_NETWORK_WINDOW_SIZE / (1 + len(self.architecture))
        horizontal_off = 0

        self.node_coords = []

        for i in range(len(self.architecture)):
            horizontal_off = floor(horizontal_off + horizontal_spacing)
            vertical_off = floor((GAME_WINDOW_SIZE - self.architecture[i] * NODE_SPACING) / 2)
            layer = []
            for _ in range(self.architecture[i]):
                layer.extend([[GAME_WINDOW_SIZE + horizontal_off, vertical_off]])
                vertical_off += NODE_SPACING

            self.node_coords.extend([layer])

        for i in range(len(self.node_coords) - 1):
            for j in range(len(self.node_coords[i])):
                for k in range(len(self.node_coords[i + 1])):
                    intensity = sigmoid(self.weights[i][k][j]) * 255
                    color = tuple([intensity] * 4)
                    gfxdraw.line(surface, self.node_coords[i][j][0], self.node_coords[i][j][1],
                                 self.node_coords[i + 1][k][0],
                                 self.node_coords[i + 1][k][1], color)
                gfxdraw.filled_circle(surface, self.node_coords[i][j][0], self.node_coords[i][j][1], NODE_SIZE,
                                      COLOR_BLACK)
                gfxdraw.aacircle(surface, self.node_coords[i][j][0], self.node_coords[i][j][1], NODE_SIZE, COLOR_WHITE)

        text = ["UP", "RIGHT", "DOWN", "LEFT"]
        last = len(self.node_coords) - 1
        for i in range(len(self.node_coords[last])):
            t = self.__create_text(text[i], FONT_SIZE)
            gfxdraw.filled_circle(surface, self.node_coords[last][i][0], self.node_coords[last][i][1], NODE_SIZE,
                                  COLOR_BLACK)
            gfxdraw.aacircle(surface, self.node_coords[last][i][0], self.node_coords[last][i][1], NODE_SIZE,
                             COLOR_WHITE)
            surface.blit(t, (self.node_coords[last][i][0] + NODE_SPACING, self.node_coords[last][i][1] - 5))
