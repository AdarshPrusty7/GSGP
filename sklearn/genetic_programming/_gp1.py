
# Author: Adarsh Prusty

from _base import *

import itertools
import math
import random


# Boolean Non-Semantic Genetic Operators
class GeneticProgram:
    def __init__(self, numvars, depth, pop_size, generations, trunc, target_funct) -> None:
        self.numvars = numvars
        self.depth = depth
        self.pop_size = pop_size
        self.generations = generations
        self.trunc = trunc
        self.target_funct = target_funct
        self.vars = []
        pass

    def create_vars(self):
        self.vars = ['x'+str(i) for i in range(self.numvars)]

    #### BOOLEAN ####
    def boolean_crossover(self, f1, f2):
        'Crossover operator.'
        mask = BooleanPopulation().create_boolean_function(self.depth, self.vars)
        offspring = lambda *x: (f1(*x) and mask(*x)) or (f2(*x) and not mask(*x))
        offspring = memoize(offspring)
        offspring.genotype = lambda: '(('+ f1.genotype() + ' and ' + mask.genotype() + ') or (' + f2.genotype() + ' and not ' + mask.genotype() + '))'
        return offspring

    def boolean_mutation(self, f):
        'Mutation operator.'
        mintermexpr = ' and '.join([random.choice([x,'not ' + x]) for x in self.vars]) 
        minterm = eval('lambda ' + ', '.join(self.vars) + ': ' + mintermexpr)
        if random.random() < 0.5:
            offspring = lambda *x : f(*x) or minterm(*x)
            offspring = memoize(offspring)
            offspring.genotype = lambda: '(' + f.genotype() + ' or ' + mintermexpr + ')'
        else:
            offspring = lambda *x: f(*x) and not minterm(*x)
            offspring = memoize(offspring)
            offspring.genotype = lambda: '(' + f.genotype() + ' and not ' + mintermexpr + ')'
        return offspring

    def boolean_fitness(self, f):
        'Fitness function.'
        fitness = 0
        combination_list = [[True, False] for i in range(self.numvars)]
        for element in itertools.product(*combination_list):
            if f(*element) != self.target_funct(*element):
                fitness += 1
        return fitness

    def boolean_population_evolution(self):
        """Population Based Evolution"""
        bool = BooleanPopulation()
        population = bool.create_boolean_population(self.depth, self.vars, self.pop_size)

        for generation in range(self.generations):
            graded_population = [(self.boolean_fitness(individual), individual) for individual in population]
            sorted_population = sorted(graded_population, key=lambda x : x[0]) # sorted population by its fitness
            print ('GENERATION: ' + str(generation + 1) + ' FITNESS: ' + str(self.boolean_fitness(sorted_population[0][1])) + ' AVERAGE FITNESS: ' + str(sum(individual[0] for individual in graded_population) / self.pop_size))
            new_parents = sorted_population[:int(self.trunc*self.pop_size)]
            if generation == self.generations - 1:
                print("Hmmm")
                break
            for i in range(self.pop_size):
                parent = random.sample(new_parents, 2) # picks two random parents
                population[i] = self.boolean_mutation(self.boolean_crossover(parent[0][1], parent[1][1]))
        
        print ("Best individual in the last population: ")
        #print (sorted_population[0][1].genotype()) # This takes a while
        print ("Query best individual in last population with all True inputs:")
        print (sorted_population[0][1](*([True] * self.numvars)))

    #### REAL ####
    def real_crossover(self, f1, f2):
        'Crossover operator.'
        mask = ArithmeticPopulation().create_arithmetic_function(self.depth, self.vars)
        offspring = lambda *x: (f1(*x) * mask(*x)) + (f2(*x) + (1 - mask(*x)))
        offspring = memoize(offspring)
        offspring.genotype = lambda: '(('+ f1.genotype() + ' and ' + mask.genotype() + ') or (' + f2.genotype() + ' and not ' + mask.genotype() + '))'
        return offspring

    def real_mutation(self, f):
        'Mutation operator.'
        mutation_step = random.random()
        random_arithmetic_1 = ArithmeticPopulation().create_arithmetic_function(self.depth, self.vars)
        random_arithmetic_2 = ArithmeticPopulation().create_arithmetic_function(self.depth, self.vars)
        offspring = lambda *x : f(*x) + mutation_step * (random_arithmetic_1(*x) - random_arithmetic_2(*x))
        offspring = memoize(offspring)
        offspring.genotype = lambda: '(' + f.genotype() + ' + ' + str(mutation_step) + ' * (' + random_arithmetic_1.genotype() + ' - ' + random_arithmetic_2.genotype() + '))'
        return offspring
    
    def real_fitness(self, f, seed):
        'Fitness function.'
        generator = random.Random(seed)
        fitness = 0
        # Generate a list
        combination_list = [[random.random(), random.random()] for i in range(self.numvars)]
        for element in itertools.product(*combination_list):
            if f(*element) != self.target_funct(*element):
                fitness += 1
        return fitness

    def real_population_evolution(self):
        """Population Based Evolution"""
        arith = ArithmeticPopulation()
        population = arith.create_arithmetic_population(self.depth, self.vars, self.pop_size)
        seed = random.randint(0, 10000000)

        for generation in range(self.generations):
            graded_population = [(self.real_fitness(individual, seed), individual) for individual in population]
            sorted_population = sorted(graded_population, key=lambda x : x[0])
            print ('GENERATION: ' + str(generation + 1) + ' FITNESS: ' + str(self.real_fitness(sorted_population[0][1], seed)) + ' AVERAGE FITNESS: ' + str(sum(individual[0] for individual in graded_population) / self.pop_size))
            new_parents = sorted_population[:int(self.trunc*self.pop_size)]
            if generation == self.generations - 1:
                print("Hmmm")
                break
            for i in range(self.pop_size):
                parent = random.sample(new_parents, 2)
                population[i] = self.real_mutation(self.real_crossover(parent[0][1], parent[1][1]))

        print ("Best individual in the last population: ")
        #print (sorted_population[0][1].genotype()) # This takes a while
        print ("Query best individual in last population with all True inputs:")
        return sorted_population[0][1](*([True] * self.numvars))

    #### PROGRAM ####


    def hill_climbing(self):
        pass

    def run(self):
        'Run the genetic program.'
        # Create initial population
        pass



def target_funct(*args):
    return args.count(True) % 2 == 1

def arith_target_funct(*args):
    return sum(args)*2

gp = GeneticProgram(5, 4, 20, 30, 0.5, target_funct)
gp.create_vars()
gp.boolean_population_evolution()

print("END OF BOOLEAN")

arith_gp  = GeneticProgram(5, 4, 20, 30, 0.5, arith_target_funct)
arith_gp.create_vars()
arith_gp.real_population_evolution()