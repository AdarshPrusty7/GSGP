
from _base import ArithmeticPopulation, memoize

import random
import math


class GeneticProgram:
    def __init__(self, numvars, depth, pop_size, generations, trunc, target_funct) -> None:
        self.numvars = numvars
        self.depth = depth
        self.pop_size = pop_size
        self.generations = generations
        self.trunc = trunc
        self.target_funct = target_funct
        self.vars = []
        
    def real_crossover(self, f1, f2):
        'Crossover operator.'
        mask = ArithmeticPopulation().create_arithmetic_function()
        offspring = lambda x: (f1(x) * mask(x)) + (f2(x) * (1 - mask(x)))
        offspring = memoize(offspring)
        offspring.genotype = lambda: '(('+ f1.genotype() + ' * ' + mask.genotype() + ') + (' + f2.genotype() + ' * (1 - ' + mask.genotype() + ')))'
        return offspring

    def real_mutation(self, f):
        'Mutation operator.'
        mutation_step = 0.001
        random_arithmetic_1 = ArithmeticPopulation().create_arithmetic_function()
        random_arithmetic_2 = ArithmeticPopulation().create_arithmetic_function()
        offspring = lambda x : f(x) + mutation_step * (random_arithmetic_1(x) - random_arithmetic_2(x))
        offspring = memoize(offspring)
        offspring.genotype = lambda: '(' + f.genotype() + ' + ' + str(mutation_step) + ' * (' + random_arithmetic_1.genotype() + ' - ' + random_arithmetic_2.genotype() + '))'
        return offspring
    
    def real_fitness(self, f, seed):
        'Fitness function.'
        generator = random.Random(seed)
        fitness = 0
        # Euclidean distance to output vector of target function on 20 inputs in [-1, 1]
        input_list = [generator.uniform(-1, 1) for i in range(20)]
        f_output = [f(i) for i in input_list]
        target_output = [self.target_funct(i) for i in input_list]
        # Calculate Euclidean distance
        for i in range(len(f_output)):
            fitness += (f_output[i] - target_output[i])**2
        return math.sqrt(fitness)

    def real_population_evolution(self):
        """Population Based Evolution"""
        arith = ArithmeticPopulation()
        population = arith.create_arithmetic_population(self.pop_size)
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
        print ("Query best individual in last population with one input:")
        print (sorted_population[0][1](0.5), self.target_funct(0.5))
        print (sorted_population[0][1](0.75), self.target_funct(0.75))
        print (sorted_population[0][1](0.25), self.target_funct(0.25))
        
        print (sorted_population[0][1](-0.25), self.target_funct(-0.25))
        print (sorted_population[0][1](-0.5), self.target_funct(-0.5))
        print (sorted_population[0][1](-0.75), self.target_funct(-0.75))

        return sorted_population[0][1](0)