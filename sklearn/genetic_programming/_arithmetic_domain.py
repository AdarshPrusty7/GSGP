# Author: Adarsh Prusty

import math
import random
from typing import Callable, Tuple

from _base import ArithmeticPopulation, memoize


class ArithmeticGSGP:
    """A class that implements the Geometric Semantic Genetic Programming algorithm for the Arithmetic domain."""

    def __init__(self, polynomial_degree: int, pop_size: int, generations: int, trunc: float, target_funct: Callable, mutation_step: float = 0.001) -> None:
        """Initializes an instance of the ArithmeticGSGP class.

        Parameters
        ----------
        polynomial_degree : int
            The degree of the polynomial to be generated.
        pop_size : int
            The size of the population.
        generations : int
            The number of generations that the algorithm will run for.
        trunc : float
            The truncation value that is used when selecting the best individuals.
        target_funct : Callable
            The target function that the algorithm will try to approximate.
        mutation_step : float, optional
            The mutation step that is used when mutating the individuals, by default 0.001
        """
        self.polynomial_degree = polynomial_degree
        self.pop_size = pop_size
        self.generations = generations
        self.trunc = trunc
        self.target_funct = target_funct
        self.mutation_step = mutation_step

    def crossover(self, f1: Callable, f2: Callable) -> Callable:
        """Crossover operator. Given f1 and f2, offspring is returned in the format of (f1 * mask) + (f2 * (1 - mask)).

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
        >>> f1 = lambda x: x**2
        >>> f2 = lambda x: x**3
        >>> offspring = real_crossover(f1, f2)
        >>> offspring.genotype()
        '((x**2 * (0.5 + x**2)) + (x**3 * (1 - (0.5 + x**2))))'
        >>> offspring(2)
        0.0
        """
        mask = ArithmeticPopulation().create_arithmetic_function(self.polynomial_degree)
        offspring = lambda x: (f1(x) * mask(x)) + (f2(x) * (1 - mask(x)))
        offspring = memoize(offspring)
        offspring.genotype = lambda: '((' + f1.genotype() + ' * ' + mask.genotype(
        ) + ') + (' + f2.genotype() + ' * (1 - ' + mask.genotype() + ')))'
        return offspring

    def mutation(self, f: Callable) -> Callable:
        """Mutation operator. Given f, offspring is returned in the format of f + mutation_step * (random_arithmetic_1 - random_arithmetic_2).

        Parameters
        ----------
        f : Callable
            The function to be mutated.

        Returns
        -------
        offspring : Callable
            The new function that is the result of the mutation operation on f.

        Examples
        ------
        >>> f = lambda x: x**2
        >>> offspring = real_mutation(f)
        >>> offspring.genotype()
        '(x**2 + 0.001 * ((x + x**2) - (x + 0.5 * x**2)))'
        >>> offspring(2)
        4.002
        """
        mutation_step = 0.001
        random_arithmetic_1 = ArithmeticPopulation().create_arithmetic_function(self.polynomial_degree)
        random_arithmetic_2 = ArithmeticPopulation().create_arithmetic_function(self.polynomial_degree)
        offspring = lambda x : f(x) + mutation_step * \
            (random_arithmetic_1(x) - random_arithmetic_2(x))
        offspring = memoize(offspring)
        offspring.genotype = lambda: '(' + f.genotype() + ' + ' + str(mutation_step) + \
            ' * (' + random_arithmetic_1.genotype() + \
            ' - ' + random_arithmetic_2.genotype() + '))'
        return offspring

    def fitness(self, f: Callable, seed: int) -> float:
        """Fitness function. Given f and a seed, the fitness of f is represented by the Euclidean distance between f and the target function on 20 inputs in [-1, 1].

        Parameters
        ----------
        f : Callable
            The function to be evaluated.
        seed : int
            The seed to be used for the random number generator to ensure that all inputs are the same throughout the running of the GP.

        Returns
        -------
        fitness : float
            The fitness of f.

        Examples
        ------
        >>> f = lambda x: x**2
        >>> real_fitness(f, 0)
        0.0
        >>> # The above is an ideal case where the function is exactly the same as the target function.
        """
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

    def population_evolution(self) -> Tuple[float, Callable]:
        """The population-based evolution loop for the Arithmetic domain. Returns the fittest function in the final population.

        Returns
        -------
        fitness : float

        fittest_function : Callable
            The fittest function in the final population.

        Examples
        ------
        >>> fittest_function = real_population_evolution()[1]
        >>> fittest_function.genotype()
        '(((x**2 * (0.5 + x**2)) + (x**3 * (1 - (0.5 + x**2)))) + 0.001 * ((x + x**2) - (x + 0.5 * x**2)))'
        """
        arith = ArithmeticPopulation()
        population = arith.create_arithmetic_population(self.polynomial_degree, self.pop_size)
        seed = random.randint(0, 10000000)

        for generation in range(self.generations):
            graded_population = [(self.fitness(individual, seed), individual)
                                 for individual in population]
            sorted_population = sorted(graded_population, key=lambda x : x[0])
            # print('GENERATION: ' + str(generation + 1) + ' FITNESS: ' + str(self.real_fitness(
            #    sorted_population[0][1], seed)) + ' AVERAGE FITNESS: ' + str(sum(individual[0] for individual in graded_population) / self.pop_size))
            new_parents = sorted_population[:int(self.trunc*self.pop_size)]
            if generation == self.generations - 1:
                break
            for i in range(self.pop_size):
                parent = random.sample(new_parents, 2)
                population[i] = self.mutation(
                    self.crossover(parent[0][1], parent[1][1]))

        return sorted_population[0][0], sorted_population[0][1]

    def hill_climbing(self) -> Tuple[float, Callable]:
        """Main function for the hill climbing algorithm. Returns the fittest function.

        Returns
        -------
        fittest_function : Callable
            The final fittest function.

        Examples
        ------
        >>> fittest_function = real_hill_climbing()[1]
        >>> fittest_function.genotype()
        '(((x**2 * (0.5 + x**2)) + (x**3 * (1 - (0.5 + x**2)))) + 0.001 * ((x + x**2) - (x + 0.5 * x**2)))'
        """
        seed = random.randint(0, 10000000)
        current = ArithmeticPopulation().create_arithmetic_function(self.polynomial_degree)
        current.fitness = self.fitness(current, seed)
        for _ in range(self.generations + 1):
            offspring = self.mutation(current)
            offspring.fitness = self.fitness(offspring, seed)
            if offspring.fitness < current.fitness:
                current = offspring
        return current.fitness, current
