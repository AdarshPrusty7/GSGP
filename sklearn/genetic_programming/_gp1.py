
# Author: Adarsh Prusty

import random
from _base import *

# Boolean Non-Semantic Genetic Operators
class GeneticProgram:
    def __init__(self, numvars, depth, pop_size, generations, trunc, target_output) -> None:
        self.numvars = numvars
        self.depth = depth
        self.pop_size = pop_size
        self.generations = generations
        self.trunc = trunc
        self.target_output = target_output
        self.vars = []
        pass

    def create_vars(self):
        self.vars = ['x'+str(i) for i in range(self.numvars)]

    def boolean_crossover(self, f1, f2):
        'Crossover operator.'
        mask = BooleanPopulation().create_boolean_function(self.depth, self.vars)
        offspring = lambda *x: (p1(*x) and mask(*x)) or (p2(*x) and not mask(*x))
        offspring = memoize(offspring)
        offspring.genotype = lambda: '(('+ f1.genotype(), 'and', mask.genotype() + ') or (' + f2.genotype(), 'and not', mask.genotype() + '))'
        return offspring

    def mutation(self, f):
        'Mutation operator.'

        if random.random() < 0.5:
            pass
        return f

    def fitness(self, f):
        'Fitness function.'
        return f

    def selection(self, f):
        'Selection operator.'
        return f

    def population_evolution(self):
        """Population Based Evolution"""
        population = self.population

        for i in range(self.GENERATIONS):
            graded_population = [(self.fitness(individual), individual) for individual in population]
            selected_population = self.selection(graded_population)
            crossover_population = self.crossover(selected_population)
            mutated_population = self.mutation(crossover_population)
            population = mutated_population

        graded_population = [(self.fitness(individual), individual) for individual in population]
        graded_population.sort(key=lambda x: x[0])
        all_true_individual = graded_population[0](*([True] * self.NUMVARS))
        return graded_population[0], all_true_individual

    def hill_climbing(self):
        pass

    def run(self):
        'Run the genetic program.'
        # Create initial population

