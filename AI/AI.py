from utils.constants import *
from genetic_algorithm.genetic_algorithm import GeneticAlgorithm
from math import floor
from snake.snake import Snake
from snake.apple import Apple
import pygame
import tkinter
import tkinter.filedialog
import pickle


class SnakeAI:
    def __init__(self):
        self.surface = pygame.display.set_mode(
            (GAME_WINDOW_SIZE + NEURAL_NETWORK_WINDOW_SIZE + INFO_WINDOW_SIZE, GAME_WINDOW_SIZE))
        pygame.display.set_caption("Snake AI")
        self.genetic_algorithm = None
        self.save_allowed = False
        self.running = True

    def __draw_border__(self, surface):
        surface.fill(COLOR_BLACK)
        border = pygame.Rect(OFFSET - 1, OFFSET - 1, MAP_SIZE * BLOCK_SIZE + 2, MAP_SIZE * BLOCK_SIZE + 2)
        pygame.draw.rect(surface, COLOR_WHITE, border)
        pygame.draw.line(surface, COLOR_WHITE, (GAME_WINDOW_SIZE, 0), (GAME_WINDOW_SIZE, GAME_WINDOW_SIZE), 1)
        surface.fill(COLOR_BLACK, pygame.Rect(OFFSET, OFFSET, BLOCK_SIZE * MAP_SIZE, BLOCK_SIZE * MAP_SIZE))

    def __draw_text(self, surface, text, size, color, x, y):
        text = pygame.font.Font(FONT, size).render(text, True, color)
        surface.blit(text, (x, y))

    def __update_info__(self, generation, fitness):
        pygame.draw.line(self.surface, COLOR_WHITE, (GAME_WINDOW_SIZE + NEURAL_NETWORK_WINDOW_SIZE, 0), (GAME_WINDOW_SIZE + NEURAL_NETWORK_WINDOW_SIZE, GAME_WINDOW_SIZE), 1)
        s = pygame.Surface((INFO_WINDOW_SIZE - 1, GAME_WINDOW_SIZE))
        self.__draw_text(s, "Info", 40, COLOR_WHITE, (floor(INFO_WINDOW_SIZE / 2) - 40), 20)
        self.__draw_text(s, "Generation: " + str(generation), 15, COLOR_WHITE, 10, 80)
        self.__draw_text(s, "Population size: " + str(POPULATION_SIZE), 15, COLOR_WHITE, 10, 100)
        self.__draw_text(s, "Mutation rate: " + str(MUTATION_RATE), 15, COLOR_WHITE, 10, 120)
        self.__draw_text(s, "Fittest: ", 15, COLOR_WHITE, 10, 140)
        self.__draw_text(s, str(fitness), 13, COLOR_WHITE, 62, 141)
        self.__draw_text(s, "Crossover: 90% K-point", 15, COLOR_WHITE, 10, 180)
        self.__draw_text(s, "Mutation: bit-flip", 15, COLOR_WHITE, 10, 200)
        self.__draw_text(s, "Elitism: 10%", 15, COLOR_WHITE, 10, 220)
        self.__draw_text(s, "Hidden activation: relu", 15, COLOR_WHITE, 10, 240)
        self.__draw_text(s, "Output activation: sigmoid", 15, COLOR_WHITE, 10, 260)
        self.__draw_text(s, "NN architecture: " + str([INPUT_LAYER] + list(HIDDEN_LAYERS) + [OUTPUT_LAYER]), 15, COLOR_WHITE, 10, 280)
        self.__draw_text(s, "Lifespan: " + str(MOVES_LEFT) + " * " + str(MOVES_UPPER_BOUND), 15, COLOR_WHITE, 10, 300)
        self.__draw_text(s, "Map size: " + str(MAP_SIZE), 15, COLOR_WHITE, 10, 320)
        self.__draw_back_button__(s, 66, GAME_WINDOW_SIZE - 40, pygame.Rect(65, GAME_WINDOW_SIZE - 50, 90, 40))
        self.surface.blit(s, (GAME_WINDOW_SIZE + NEURAL_NETWORK_WINDOW_SIZE + 1, 0))

    def __draw_back_button__(self, surface, x, y, rect):
        pygame.draw.rect(surface, COLOR_WHITE, rect)
        self.__draw_text(surface, "BACK", 30, COLOR_BLACK, x, y)
        pygame.display.update()

    def __draw_save_button__(self):
        pygame.draw.rect(self.surface, COLOR_WHITE, pygame.Rect(GAME_WINDOW_SIZE + NEURAL_NETWORK_WINDOW_SIZE + 65, GAME_WINDOW_SIZE - 100, 90, 40))
        self.__draw_text(self.surface, "SAVE", 30, COLOR_BLACK, GAME_WINDOW_SIZE + NEURAL_NETWORK_WINDOW_SIZE + 72, GAME_WINDOW_SIZE - 90)
        pygame.display.update()

    def __remove_save_button__(self):
        pygame.draw.rect(self.surface, COLOR_BLACK, pygame.Rect(GAME_WINDOW_SIZE + NEURAL_NETWORK_WINDOW_SIZE + 65, GAME_WINDOW_SIZE - 200, 90, 140))
        pygame.display.update()

    def __save__(self, x, y):
        tkinter.Tk().withdraw()
        allowed_types = [('Pickle', '.pickle')]
        path = tkinter.filedialog.asksaveasfilename(filetypes=allowed_types, defaultextension=".pickle")
        if path:
            f = open(path, "wb")
            pickle.dump(self.genetic_algorithm, f)
            self.__draw_text(self.surface, "Saved", 30, COLOR_GREEN, x, y - 50)

    def __handle_events__(self):
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                x = GAME_WINDOW_SIZE + NEURAL_NETWORK_WINDOW_SIZE + 65
                y = GAME_WINDOW_SIZE - 50
                if pygame.Rect(x, y, 90, 40).collidepoint(mouse_x, mouse_y):
                    self.running = False
                x = GAME_WINDOW_SIZE + NEURAL_NETWORK_WINDOW_SIZE + 65
                y = GAME_WINDOW_SIZE - 100
                if pygame.Rect(x, y, 90, 40).collidepoint(mouse_x, mouse_y) and self.save_allowed:
                    self.__save__(x, y)

            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

    def replay(self, surface, individual):
        s = pygame.Surface((NEURAL_NETWORK_WINDOW_SIZE + GAME_WINDOW_SIZE, GAME_WINDOW_SIZE))
        individual.snake = Snake()
        individual.apple = Apple()
        self.__draw_border__(s)
        individual.neural_net.init_draw(s)
        individual.apple.generate(individual.snake)
        clock = pygame.time.Clock()
        moves_left = MOVES_LEFT
        score = 1

        while self.running:
            self.__handle_events__()
            individual.snake.draw(s)
            individual.apple.draw(s)
            pygame.display.set_caption("SCORE: " + str(score) + "   MOVES LEFT: " + str(moves_left))
            clock.tick(FRAME_RATE)
            surface.blit(s, (0, 0))
            pygame.display.update()
            individual.move()
            individual.neural_net.draw(s)
            if individual.snake.collision_detected() or moves_left == 0:
                pygame.display.set_caption("Snake AI")
                return
            elif individual.snake.eat(individual.apple):
                score += 1
                individual.apple.generate(individual.snake)
                if moves_left + MOVES_LEFT > MOVES_LEFT * MOVES_UPPER_BOUND:
                    moves_left = MOVES_LEFT * MOVES_UPPER_BOUND
                else:
                    moves_left += MOVES_LEFT
            moves_left -= 1

    def __waiting_screen__(self, snakes_alive):
        vertical_off = floor(GAME_WINDOW_SIZE / 3)
        text = "Processing..."
        s = pygame.Surface((GAME_WINDOW_SIZE + NEURAL_NETWORK_WINDOW_SIZE, GAME_WINDOW_SIZE))
        x = floor((GAME_WINDOW_SIZE + NEURAL_NETWORK_WINDOW_SIZE) / 2) - len(text) * 20
        y = vertical_off
        self.__draw_text(s, "Processing...", 80, COLOR_WHITE, x, y)
        x = floor((GAME_WINDOW_SIZE + NEURAL_NETWORK_WINDOW_SIZE) / 2) - len(text) * 15
        y += vertical_off
        self.__draw_text(s, "Games left: " + str(snakes_alive), 50, COLOR_WHITE, x, y)
        self.surface.blit(s, (0, 0))
        pygame.display.update()

    def process_population(self):
        snakes_alive = POPULATION_SIZE
        for i in range(POPULATION_SIZE):
            self.__handle_events__()
            if not self.running:
                return
            self.genetic_algorithm.population[i].play()
            self.__waiting_screen__(snakes_alive)
            snakes_alive -= 1
        self.__waiting_screen__(snakes_alive)
        self.genetic_algorithm.population.sort(key=lambda x: x.fitness)

        fittest = self.genetic_algorithm.population[POPULATION_SIZE - 1]
        self.__update_info__(self.genetic_algorithm.generation, fittest.fitness)
        self.__draw_save_button__()
        self.save_allowed = True
        self.replay(self.surface, fittest)
        self.save_allowed = False
        self.__remove_save_button__()

    def new(self):
        off = GAME_WINDOW_SIZE + NEURAL_NETWORK_WINDOW_SIZE
        rect = pygame.Rect(off + 65, GAME_WINDOW_SIZE - 50, 90, 40)
        self.__draw_back_button__(self.surface, off + 66, GAME_WINDOW_SIZE - 40, rect)
        self.genetic_algorithm = GeneticAlgorithm()
        self.genetic_algorithm.random_init(POPULATION_SIZE)
        self.process_population()

        while self.running:
            self.genetic_algorithm.mate()
            self.process_population()

    def load(self, genetic_algorithm):
        pop_size = len(genetic_algorithm.population)
        if POPULATION_SIZE < pop_size:
            self.genetic_algorithm = genetic_algorithm
            self.genetic_algorithm.population = genetic_algorithm.population[pop_size - POPULATION_SIZE:]
        elif POPULATION_SIZE > pop_size:
            self.genetic_algorithm = GeneticAlgorithm()
            self.genetic_algorithm.generation = genetic_algorithm.generation
            self.genetic_algorithm.random_init(POPULATION_SIZE - pop_size)
            self.genetic_algorithm.population.extend(genetic_algorithm.population)
        else:
            self.genetic_algorithm = genetic_algorithm

        off = GAME_WINDOW_SIZE + NEURAL_NETWORK_WINDOW_SIZE
        rect = pygame.Rect(off + 65, GAME_WINDOW_SIZE - 50, 90, 40)
        self.__draw_back_button__(self.surface, off + 66, GAME_WINDOW_SIZE - 40, rect)
        self.process_population()
        while self.running:
            self.genetic_algorithm.mate()
            self.process_population()
