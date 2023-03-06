# Author: Adarsh Prusty

import _base
import itertools
import random

def targetfunct(*args):
    'Parity function of any number of input variables'
    return args.count(True) % 2 == 1

class GeometricSemanticGeneticProgram:
    def __init__(self, GENERATIONS, POPSIZE) -> None:
        self.GENERATIONS = GENERATIONS
        self.POPSIZE = POPSIZE
        self.TRUNC = 0.5
        self.depth = 4
        self.vars = ['x1', 'x2', 'x3', 'x4', 'x5']
        self.boo = _base.BooleanPopulation()

    def boolean_fitness(self, p):
        # Uses an error value to determine the fitness of the individual
        fit = 0
        somelists = [[True, False] for i in range(5)]
        # generate all possible combinations of inputs from somelists
        for element in itertools.product(*somelists):
            if p(*element) != targetfunct(*element):
                fit = fit + 1
        return fit

    def boolean_crossover(self, p1, p2):
        mask = self.boo.create_boolean_function(self.depth, self.vars)
        offspring = lambda *x: (p1(*x) and mask(*x)) or (p2(*x) and not mask(*x))
        offspring = self.boo.memoize(offspring) # add cache
        offspring.geno = lambda: '(('+ p1.geno() + ' and ' + mask.geno() + ') or (' + p2.geno() + ' and not ' + mask.geno() + '))'
        return offspring

    def boolean_mutation(self, p):
        mintermexpr = ' and '.join([random.choice([x,'not ' + x]) for x in self.vars]) # random minterm expression of n variables
        minterm = eval('lambda ' + ', '.join(vars) + ': ' + mintermexpr) # turn minterm into a function
        if random.random()<0.5:
            offspring = lambda *x: p(*x) or minterm(*x)
            offspring = self.boo.memoize(offspring) # add cache
            offspring.geno = lambda: '(' + p.geno() + ' or ' + mintermexpr + ')' # to reconstruct genotype
        else:
            offspring = lambda *x: p(*x) and not minterm(*x)
            offspring = self.boo.memoize(offspring) # add cache
            offspring.geno = lambda: '(' + p.geno() + ' and not ' + mintermexpr + ')' # to reconstruct genotype
        return offspring

    def boolean_selection(self, p):
        pass

    def main(self):
        'Main function.'
        pop = [self.boo.create_boolean_function(self.depth, self.vars) for _ in range(self.POPSIZE) ] # initialise population
        for gen in range(self.GENERATIONS+1):
            graded_pop = [ (self.boolean_fitness(ind), ind) for ind in pop ] # evaluate population fitness
            sorted_pop = [ ind[1] for ind in sorted(graded_pop)] # sort population on fitness
            print ('gen: ', gen , ' min fit: ', self.boolean_fitness(sorted_pop[0]), ' avg fit: ', sum(ind[0] for ind in graded_pop)/(self.POPSIZE*1.0)) # print stats
            parent_pop = sorted_pop[:int(self.TRUNC*self.POPSIZE)] # selected parents
            if gen == self.GENERATIONS:
                break
            for i in range(self.POPSIZE): # create offspring population
                par = random.sample(parent_pop, 2) # pick two random parents
                pop[i] = self.boolean_mutation(self.boolean_crossover(par[0],par[1])) # create offspring

        print ('Best individual in last population: ')
        #print (sorted_pop[0]).geno() # reconstruct genotype of final solution (WARNING: EXPONENTIALLY LONG IN NUMBER OF GENERATIONS!)
        print ('Query best individual in last population with all True inputs:')
        print (sorted_pop[0](*([True] * 5))) # however querying it to make predictions is quick

gsgp = GeometricSemanticGeneticProgram(10, 10)
gsgp.main()