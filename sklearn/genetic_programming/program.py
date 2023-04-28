from _base import ProgramPopulation, memoize

import random
import itertools

class GeneticProgram:
    def __init__(self, numvars, depth, pop_size, generations, trunc, target_funct) -> None:
        self.numvars = numvars
        self.depth = depth
        self.pop_size = pop_size
        self.generations = generations
        self.trunc = trunc
        self.target_funct = target_funct
        self.vars = []
    
    def program_crossover(self, f1, f2):
        'Crossover operator.'
        condr = random.randint(0, 1)
        offspring = lambda *x: f1(*x) if condr else f2(*x) # Ternary operator
        offspring = memoize(offspring)
        offspring.genotype = lambda: '(' + f1.genotype() + " if " + str(condr) + " else " + f2.genotype() + ")"
        return offspring

    def program_mutation(self, f):
        'Mutation operator.'
        # Define condr by making it a condition that is true for only a single random set of inputs
        condr_true = [random.randint(1, nc) for _ in range(nv)]
        condr_expression = "(1 if " + "[" + ", ".join(["x[" + i[1:] + "]" for i in self.vars]) + "]"  " == " + str(condr_true) + " else 0)"
        condr = eval("lambda *x: " + condr_expression)

        # Define outr, which is a random member of OS
        outr = random.choice(OS)

        offspring = lambda *x: outr if condr(*x) else f(*x)
        offspring = memoize(offspring)
        offspring.genotype = lambda: '(' + str(outr) + " if " + condr_expression + " else " + f.genotype() + ")"
        return offspring

    def program_fitness(self, f, seed):
        'Fitness function.'
        generator = random.Random(seed)
        # Generate list of random Boolean inputs
        fitness = 0
        combination_list = [[generator.randint(1, nc), generator.randint(1, nc), generator.randint(1, nc)] for i in range(self.numvars)]
        f_output = [f(*element) for element in itertools.product(*combination_list)]
        target_output = [self.target_funct(*element) for element in itertools.product(*combination_list)]
        # Calculate Hamming distance
        for i in range(len(f_output)):
            if f_output[i] != target_output[i]:
                fitness += 1
        return fitness

    def program_population_evolution(self):
        """Population Based Evolution"""
        program = ProgramPopulation()
        population = program.create_program_population(self.depth, self.vars, self.pop_size)
        seed = random.randint(0, 10000000)

        for generation in range(self.generations):
            graded_population = [(self.program_fitness(individual, seed), individual) for individual in population]
            sorted_population = sorted(graded_population, key=lambda x : x[0])
            print ('GENERATION: ' + str(generation + 1) + ' |FITNESS: ' + str(self.program_fitness(sorted_population[0][1], seed)) + ' |AVERAGE FITNESS: ' + str(sum(individual[0] for individual in graded_population) / self.pop_size))
            new_parents = sorted_population[:int(self.trunc*self.pop_size)]
            if generation == self.generations - 1:
                print("Hmmm")
                break
            for i in range(self.pop_size):
                parent = random.sample(new_parents, 2)
                population[i] = self.program_mutation(self.program_crossover(parent[0][1], parent[1][1]))

        print ("Best individual in the last population: ")
        #print (sorted_population[0][1].genotype()) # This takes a while
        print ("Query best individual in last population with all True inputs:")
        return sorted_population[0][1](*([True] * self.numvars))
