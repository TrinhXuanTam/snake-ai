from genetic_algorithm.individual import Individual
from math import floor, ceil
from utils.constants import *
from random import uniform, randint
from numpy import array, transpose


class GeneticAlgorithm:
    def __init__(self):
        self.population = None
        self.generation = 0

    def random_init(self, size):
        self.population = [Individual() for _ in range(size)]

    def __roulette_wheel_selection__(self, total_fitness):
        spin = uniform(0, total_fitness)
        curr = 0
        index = 0
        while spin > curr and index < POPULATION_SIZE - 1:
            curr += self.population[index].fitness
            index += 1
        return self.population[index]

    def __k_point_crossover__(self, parent1, parent2):
        parent1_weights = parent1.neural_net.weights
        parent2_weights = parent2.neural_net.weights
        parent1_biases = parent1.neural_net.biases
        parent2_biases = parent2.neural_net.biases
        layers_count = len(parent1_weights)
        offspring = Individual()
        offspring_weights = []
        offspring_biases = []

        for i in range(layers_count):
            rows, cols = parent1_weights[i].shape
            random_row = randint(0, rows - 1)
            random_col = randint(0, cols - 1)
            new_layer = []
            for row in range(rows):
                new_row = []
                for col in range(cols):
                    if row <= random_row or (row == random_row and col <= random_col):
                        weight = parent1_weights[i][row][col]
                    else:
                        weight = parent2_weights[i][row][col]
                    new_row.append(weight)
                new_layer.extend([new_row])
            offspring_weights.append(array(new_layer))

            b_rows = parent1_biases[i].shape[0]
            new_bias = []
            random_row = randint(0, b_rows - 1)
            for row in range(b_rows):
                if row < random_row:
                    bias = parent1_biases[i][row]
                else:
                    bias = parent2_biases[i][row]
                new_bias.append(bias)
            offspring_biases.extend([transpose(array(new_bias))])
        offspring.neural_net.weights = offspring_weights
        offspring.neural_net.biases = offspring_biases
        return offspring

    def __mutate__(self, individual):
        layers_count = len(individual.neural_net.weights)
        for i in range(layers_count):
            rows, cols = individual.neural_net.weights[i].shape
            for row in range(rows):
                for col in range(cols):
                    rand = uniform(0, 1)
                    if rand < MUTATION_RATE:
                        individual.neural_net.weights[i][row][col] = uniform(-1, 1)
            b_rows = individual.neural_net.biases[i].shape[0]
            for row in range(b_rows):
                rand = uniform(0, 1)
                if rand < MUTATION_RATE:
                    individual.neural_net.biases[i][row] = uniform(-1, 1)

    def mate(self):
        total_fitness = sum(i.fitness for i in self.population)
        new_population = []
        for _ in range(floor(POPULATION_SIZE * 0.9)):
            parent1 = self.__roulette_wheel_selection__(total_fitness)
            parent2 = self.__roulette_wheel_selection__(total_fitness)
            offspring = self.__k_point_crossover__(parent1, parent2)
            self.__mutate__(offspring)
            new_population.append(offspring)
        new_population.extend(self.population[ceil(floor(len(self.population) * 0.9)):])
        self.population = new_population
        self.generation += 1
