# Author: Adarsh Prusty

from _base import BooleanPopulation, memoize

import itertools
import math
import random

from inspect import getfullargspec


# Boolean Semantic Genetic Operators
class GeneticProgram:
    def __init__(self, numvars, depth, pop_size, generations, trunc, target_funct) -> None:
        self.numvars = numvars
        self.depth = depth
        self.pop_size = pop_size
        self.generations = generations
        self.trunc = trunc
        self.target_funct = target_funct
        self.vars = []

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

    


    def hill_climbing(self):
        pass

    def run(self):
        'Run the genetic program.'
        # Create initial population
        pass



def target_funct(*args):
    """Parity Function Test"""
    return args.count(True) % 2 == 1

def arith_target_funct(arg):
    return arg**2 + 1

def program_target_funct(*args):
    return ((args[0] + args[1]) % ncl) + 1

"""gp = GeneticProgram(5, 4, 20, 30, 0.5, target_funct)
gp.create_vars()
gp.boolean_population_evolution()

print("END OF BOOLEAN")"""

arith_gp  = GeneticProgram(1, 4, 100, 30, 0.5, arith_target_funct)
arith_gp.create_vars()
print(arith_gp.real_population_evolution(), arith_target_funct(0))

print("END OF ARITHMETIC")

"""nc, nv, ncl = 3, 3, 4
IS = [i for i in range(1, nc + 1)]
OS = [i for i in range(1, ncl + 1)]
program_gp = GeneticProgram(nc, 4, 100, 25, 0.5, program_target_funct)
program_gp.create_vars()
program_gp.program_population_evolution()

print("END OF PROGRAM")"""

