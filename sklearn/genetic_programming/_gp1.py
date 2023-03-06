

import random

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

    def crossover(self, f1, f2):
        'Crossover operator.'
        return f1, f2

    def mutation(self, f):
        'Mutation operator.'
        return f

    def fitness(self, f):
        'Fitness function.'
        return f

    def selection(self, f):
        'Selection operator.'
        return f

    def create_boolean_expression(self, depth):
        'Create a random Boolean expression using recursion.'
        if depth == 1 or random.random() < 1.0 / (2 ** depth - 1):
            return random.choice(self.vars)
        if random.random() < 1.0 / 3:
            return 'not' + ' ' + self.create_boolean_expression(depth - 1)
        pass

    def create_boolean_function(self):
        'Create a random Boolean function.'
        pass

    def create_boolean_population(self):
        'Create initial population of Boolean functions.'
        pass

    def run(self):
        'Run the genetic program.'
        # Create initial population
