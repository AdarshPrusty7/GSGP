# Author: Adarsh Prusty

import itertools
import random
from typing import Callable, Tuple

from _base import BooleanPopulation, memoize


class BooleanGSGP:
    """A class that implements the Geometric Semantic Genetic Programming algorithm for the Boolean domain."""

    def __init__(self, numvars: int, depth: int, pop_size: int, generations: int, trunc: float, target_funct: Callable) -> None:
        """Initializes an instance of the BooleanGSGP class.

        Parameters
        ----------
        numvars : int
            The number of variables that the functions will take as input.
        depth : int
            The maximum depth of the functions.
        pop_size : int
            The size of the population.
        generations : int
            The number of generations that the algorithm will run for.
        trunc : float
            The truncation value that is used when selecting the best individuals.
        target_funct : Callable
            The target function that the algorithm will try to approximate.
        """
        self.numvars = numvars
        self.depth = depth
        self.pop_size = pop_size
        self.generations = generations
        self.trunc = trunc
        self.target_funct = target_funct
        self.vars = None
        self.__create_vars()

    def __create_vars(self) -> None:
        """Creates the variables that the functions will take as input, in the format of x0, x1, x2, ..., xn.

        Examples
        ------
        >>> self.numvars = 6
        >>> __create_vars()
        >>> self.vars
        ['x0', 'x1', 'x2', 'x3', 'x4', 'x5']
        """
        self.vars = ['x'+str(i) for i in range(self.numvars)]

    #### BOOLEAN ####
    def crossover(self, f1: Callable, f2: Callable) -> Callable:
        """Crossover operator. Given f1 and f2, offspring is returned in the format of ((f1 and mask) or (f2 and not mask)).

        Parameters
        ----------
        f1 : Callable
            A parent function.
        f2 : Callable
            A parent function.

        Returns
        -------
        offspring : Callable
            The new function that is the result of the crossover operation on f1 and f2.

        Examples
        ------
        >>> f1 = lambda x: x
        >>> f2 = lambda x: not x
        >>> offspring = boolean_crossover(f1, f2)
        >>> offspring.genotype()
        '(x and (not x)) or ((not x) and not (not x))'
        """
        mask = BooleanPopulation().create_boolean_function(self.depth, self.vars)
        offspring = lambda *x: (f1(*x) and mask(*x)) or (f2(*x) and not mask(*x))
        offspring = memoize(offspring)
        offspring.genotype = lambda: '((' + f1.genotype() + ' and ' + mask.genotype(
        ) + ') or (' + f2.genotype() + ' and not ' + mask.genotype() + '))'
        return offspring

    def mutation(self, f: Callable) -> Callable:
        """The mutation operator. Given f, offspring is returned in the format of (f or minterm) or (f and not minterm).

        Parameters
        ----------
        f : Callable
            The parent function.

        Returns
        -------
        offspring : Callable
            The new function that is the result of the mutation operation on f.

        Examples
        ------
        >>> f = lambda x: x
        >>> offspring = boolean_mutation(f)
        >>> offspring.genotype()
        '(x or (not x)) or (x and not (not x))'
        """
        mintermexpr = ' and '.join([random.choice([x, 'not ' + x]) for x in self.vars])
        minterm = eval('lambda ' + ', '.join(self.vars) + ': ' + mintermexpr)
        if random.random() < 0.5:
            offspring = lambda *x : f(*x) or minterm(*x)
            offspring = memoize(offspring)
            offspring.genotype = lambda: '(' + f.genotype() + ' or ' + mintermexpr + ')'
        else:
            offspring = lambda *x: f(*x) and not minterm(*x)
            offspring = memoize(offspring)
            offspring.genotype = lambda: '(' + f.genotype() + \
                ' and not ' + mintermexpr + ')'
        return offspring

    def fitness(self, f: Callable) -> int:
        """The fitness function. Given f, the hamming distance of f and the target function is returned.

        Parameters
        ----------
        f : Callable
            The function that will be evaluated.

        Returns
        -------
        fitness : int
            The hamming distance of f and the target function.

        Examples
        ------
        >>> self.target_funct = lambda x: x
        >>> f = lambda x: x
        >>> self.boolean_fitness(f)
        0
        >>> # The fitness is 0 because f and the target function are the same.
        """
        fitness = 0
        combination_list = [[True, False] for i in range(self.numvars)]
        for element in itertools.product(*combination_list):
            if f(*element) != self.target_funct(*element):
                fitness += 1
        return fitness

    def population_evolution(self) -> Tuple[int, Callable]:
        """The population-based evolution loop for the Boolean domain. Returns the fittest function in the final population.


        Returns
        -------
        fitness : int

        fittest_function : Callable
            The fittest function in the final population.

        Examples
        ------
        >>> bp = BooleanGSGP(6, 6, 100, 1, 0.5, lambda x: x)
        >>> fittest_function = bp.population_evolution()[1]
        >>> fittest_function.genotype()
        '(x0 and (not x1)) or ((not x0) and x1)'
        """
        bool = BooleanPopulation()
        population = bool.create_boolean_population(
            self.depth, self.vars, self.pop_size)
        for generation in range(self.generations):
            graded_population = [(self.fitness(individual), individual)
                                 for individual in population]
            # sorted population by its fitness
            sorted_population = sorted(graded_population, key=lambda x : x[0])
            new_parents = sorted_population[:int(self.trunc*self.pop_size)]
            if sorted_population[0][0] == 0:
                break
            if generation == self.generations - 1:
                break
            for i in range(self.pop_size):
                parent = random.sample(new_parents, 2)  # picks two random parents
                population[i] = self.mutation(
                    self.crossover(parent[0][1], parent[1][1]))
        return sorted_population[0][0], sorted_population[0][1]

    def hill_climbing(self) -> Tuple[int, Callable]:
        """The main function for the hill climbing algorithm. Returns the fittest function.

        Returns
        -------
        fitness : int

        fittest_function : Callable
            The fittest function.

        Examples
        ------
        >>> bp = BooleanGSGP(6, 6, 100, 1, 0.5, lambda x: x)
        >>> fittest_function = bp.hill_climbing()[1]
        >>> fittest_function.genotype()
        '(x0 and (not x1)) or ((not x0) and x1)'
        """
        current = BooleanPopulation().create_boolean_function(self.depth, self.vars)
        current.fitness = self.fitness(current)
        for _ in range(self.generations + 1):
            offspring = self.mutation(current)
            offspring.fitness = self.fitness(offspring)
            if offspring.fitness < current.fitness:
                current = offspring
            if current.fitness == 0:
                break            
        return current.fitness, current
