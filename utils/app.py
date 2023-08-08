from utils.game import Game
from utils.constants import *
from AI.AI import SnakeAI
import pygame
import tkinter
import tkinter.filedialog
import pickle


class App:
    def __init__(self):
        pygame.init()
        self.surface = pygame.display.set_mode((700, 500))
        pygame.display.set_caption("Snake AI")

    def __render_menu__(self):
        pygame.display.set_caption("Snake AI")
        self.surface = pygame.display.set_mode((700, 500))
        self.surface.fill(COLOR_BLACK)
        play_button = pygame.Rect(250, 150, 200, 50)
        evolve_button = pygame.Rect(250, 250, 200, 50)
        quit_button = pygame.Rect(250, 350, 200, 50)
        self.__draw_text__(self.surface, "Snake AI", 80, COLOR_WHITE, 180, 30)
        pygame.draw.rect(self.surface, COLOR_WHITE, play_button)
        pygame.draw.rect(self.surface, COLOR_WHITE, evolve_button)
        pygame.draw.rect(self.surface, COLOR_WHITE, quit_button)
        self.__draw_text__(self.surface, "Play", 30, COLOR_BLACK, 315, 160)
        self.__draw_text__(self.surface, "Evolve ANN", 30, COLOR_BLACK, 265, 260)
        self.__draw_text__(self.surface, "Quit", 30, COLOR_BLACK, 315, 360)
        return play_button, evolve_button, quit_button

    def __draw_text__(self, surface, text, size, color, x, y):
        text = pygame.font.Font(FONT, size).render(text, True, color)
        surface.blit(text, (x, y))

    def __load__(self):
        tkinter.Tk().withdraw()
        allowed_types = [('Pickle', '.pickle')]
        path = tkinter.filedialog.askopenfilename(filetypes=allowed_types, defaultextension=".pickle")
        if path:
            f = open(path, "rb")
            population = pickle.load(f)
            SnakeAI().load(population)
            self.surface = pygame.display.set_mode((700, 500))
            self.__render_evolve__()

    def __render_play__(self):
        self.surface.fill(COLOR_BLACK)
        pygame.display.set_caption("Snake AI")
        play_game = pygame.Rect(250, 150, 200, 50)
        ai_play = pygame.Rect(250, 250, 200, 50)
        back_button = pygame.Rect(250, 350, 200, 50)
        pygame.draw.rect(self.surface, COLOR_WHITE, play_game)
        pygame.draw.rect(self.surface, COLOR_WHITE, ai_play)
        pygame.draw.rect(self.surface, COLOR_WHITE, back_button)
        self.__draw_text__(self.surface, "Play", 80, COLOR_WHITE, 265, 30)
        self.__draw_text__(self.surface, "Play Game", 30, COLOR_BLACK, 275, 160)
        self.__draw_text__(self.surface, "Play AI", 30, COLOR_BLACK, 305, 260)
        self.__draw_text__(self.surface, "Back", 30, COLOR_BLACK, 315, 360)
        pygame.display.update()
        return play_game, ai_play, back_button

    def __ai_play__(self):
        tkinter.Tk().withdraw()
        allowed_types = [('Pickle', '.pickle')]
        path = tkinter.filedialog.askopenfilename(filetypes=allowed_types, defaultextension=".pickle")
        self.surface = pygame.display.set_mode((700, 500))
        if path:
            f = open(path, "rb")
            GA = pickle.load(f)
            AI = SnakeAI()
            AI.genetic_algorithm = GA
            size = len(GA.population)
            AI.__update_info__(AI.genetic_algorithm.generation, GA.population[size - 1].fitness)
            AI.replay(self.surface, GA.population[size - 1])

    def __play__(self):
        play_game, ai_play, back_button = self.__render_play__()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    if play_game.collidepoint(mouse_x, mouse_y):
                        Game().start_game()
                        self.surface = pygame.display.set_mode((700, 500))
                        pygame.display.set_caption("Snake AI")
                        self.__render_play__()
                    elif ai_play.collidepoint(mouse_x, mouse_y):
                        self.__ai_play__()
                        self.surface = pygame.display.set_mode((700, 500))
                        pygame.display.set_caption("Snake AI")
                        self.__render_play__()
                    elif back_button.collidepoint(mouse_x, mouse_y):
                        self.__render_menu__()
                        return

    def __render_evolve__(self):
        self.surface.fill(COLOR_BLACK)
        pygame.display.set_caption("Snake AI")
        new_button = pygame.Rect(250, 150, 200, 50)
        load_button = pygame.Rect(250, 250, 200, 50)
        back_button = pygame.Rect(250, 350, 200, 50)
        pygame.draw.rect(self.surface, COLOR_WHITE, new_button)
        pygame.draw.rect(self.surface, COLOR_WHITE, load_button)
        pygame.draw.rect(self.surface, COLOR_WHITE, back_button)
        self.__draw_text__(self.surface, "Evolve ANN", 80, COLOR_WHITE, 140, 30)
        self.__draw_text__(self.surface, "New", 30, COLOR_BLACK, 320, 160)
        self.__draw_text__(self.surface, "Load", 30, COLOR_BLACK, 315, 260)
        self.__draw_text__(self.surface, "Back", 30, COLOR_BLACK, 315, 360)
        pygame.display.update()
        return new_button, load_button, back_button

    def __evolve_ANN__(self):
        new_button, load_button, back_button = self.__render_evolve__()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    if new_button.collidepoint(mouse_x, mouse_y):
                        SnakeAI().new()
                        self.surface = pygame.display.set_mode((700, 500))
                        self.__render_evolve__()
                    elif load_button.collidepoint(mouse_x, mouse_y):
                        self.__load__()
                    elif back_button.collidepoint(mouse_x, mouse_y):
                        self.__render_menu__()
                        return

    def __main_menu__(self):
        play_button, evolve_button, quit_button = self.__render_menu__()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    if play_button.collidepoint(mouse_x, mouse_y):
                        self.__play__()
                    elif evolve_button.collidepoint(mouse_x, mouse_y):
                        self.__evolve_ANN__()
                    elif quit_button.collidepoint(mouse_x, mouse_y):
                        pygame.quit()
                        quit()
            pygame.display.update()

    def start(self):
        self.__main_menu__()
