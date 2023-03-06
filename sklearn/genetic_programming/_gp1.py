
# Author: Adarsh Prusty

class GeneticProgram:
    def __init__(self, input_data, output_data, GENERATIONS=10, POPULATION_SIZE=100, NUMVARS) -> None:
        self.input_data = input_data
        self.output_data = output_data
        self.population = []
        self.GENERATIONS = GENERATIONS
        self.POPULATION_SIZE = POPULATION_SIZE
        self.NUMVARS = NUMVARS

    def fitness(self, individual):
        """Fitness function"""
        fitness = 0
        for i in range(len(self.input_data)):
            if individual(self.input_data[i]) == self.output_data[i]:
                fitness += 1
        return fitness

    def selection(self, population):
        """Roulette Wheel Selection"""

    def crossover(self, population):
        pass

    def mutation(self, population):
        pass

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

