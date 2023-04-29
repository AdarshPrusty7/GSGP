import itertools
import random
from typing import Callable

from _base import ProgramPopulation, memoize


class ProgramGSGP:
    def __init__(self, nc: int, nv: int, ncl: int, depth: int, pop_size: int, generations: int, trunc: float, target_funct: Callable) -> None:
        """Initializes an instance of the ProgramGSGP class.

        Parameters
        ----------
        nc : int
            1 to nv is the range of values that the variables can take.
        nv : int
            The number of variables that the functions will take as input.
        ncl : int
            1 to ncl is the range of values that the functions can take as output.
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
        self.nc = nc
        self.nv = nv
        self.ncl = ncl
        self.depth = depth
        self.pop_size = pop_size
        self.generations = generations
        self.trunc = trunc
        self.target_funct = target_funct
        self.vars = []

    def create_vars(self) -> None:
        """Creates the variables that the functions will take as input, in the format of x0, x1, x2, ..., xn.

        Examples
        ------
        >>> self.nv = 6
        >>> create_vars()
        >>> self.vars
        ['x0', 'x1', 'x2', 'x3', 'x4', 'x5']
        """
        self.vars = ['x'+str(i) for i in range(self.nc)]

    def program_crossover(self, f1: Callable, f2: Callable) -> Callable:
        """Crossover operator. Given f1 and f2, offspring is returned in the format of (f1 if condr else f2).

        Parameters
        ----------
        f1 : Callable
            A parent function.
        f2 : Callable
            A parent function.

        Returns
        -------
        offspring : Callable
            The offspring of f1 and f2.

        Examples
        ------
        >>> f1 = lambda *x: x0 if True else x1
        >>> f2 = lambda *x: x1 if True else x2
        >>> offspring = program_crossover(f1, f2)
        >>> offspring.genotype()
        '(x0 if True else x1) if True else (x1 if True else x2)'
        """
        condr = random.randint(0, 1)
        offspring = lambda *x: f1(*x) if condr else f2(*x)  # Ternary operator
        offspring = memoize(offspring)
        offspring.genotype = lambda: '(' + f1.genotype() + \
            " if " + str(condr) + " else " + f2.genotype() + ")"
        return offspring

    def program_mutation(self, f: Callable) -> Callable:
        """Mutation operator. Given f, offspring is returned in the format of (outr if condr else f).

        Parameters
        ----------
        f : Callable
            The parent function.

        Returns
        -------
        offspring : Callable
            The offspring of f.

        Examples
        ------
        >>> f = lambda *x: x0 if True else x1
        >>> offspring = program_mutation(f)
        >>> offspring.genotype()
        '2 if True else (x0 if True else x1)'
        """
        # Define condr by making it a condition that is true for only a single random set of inputs
        condr_true = [random.randint(1, self.nc) for _ in range(self.nv)]
        condr_expression = "(1 if " + "[" + ", ".join(
            ["x[" + i[1:] + "]" for i in self.vars]) + "]"  " == " + str(condr_true) + " else 0)"
        condr = eval("lambda *x: " + condr_expression)
        # Define outr, which is a random member of OS
        # OS = {1, 2, ..., ncl}. Built inline for efficiency
        outr = random.choice([i for i in range(1, self.ncl + 1)])
        offspring = lambda *x: outr if condr(*x) else f(*x)
        offspring = memoize(offspring)
        offspring.genotype = lambda: '(' + str(outr) + " if " + \
            condr_expression + " else " + f.genotype() + ")"
        return offspring

    def program_fitness(self, f: Callable, seed: int):
        """_summary_

        Parameters
        ----------
        f : Callable
            The function that will be evaluated.
        seed : int
            The seed that will be used to generate the random inputs.

        Returns
        -------
        fitness : _type_
            The fitness of the function.

        Examples
        ------
        >>> f = lambda *x: x0 if True else x1
        >>> seed = 0
        >>> program_fitness(f, seed)
        0
        >>> # This is an ideal case, where the function is equal to the target function.
        """
        generator = random.Random(seed)
        # Generate list of random Boolean inputs
        fitness = 0
        combination_list = [[generator.randint(1, self.nc), generator.randint(
            1, self.nc), generator.randint(1, self.nc)] for i in range(self.nv)]
        f_output = [f(*element) for element in itertools.product(*combination_list)]
        target_output = [self.target_funct(*element)
                         for element in itertools.product(*combination_list)]
        # Calculate Hamming distance
        for i in range(len(f_output)):
            if f_output[i] != target_output[i]:
                fitness += 1
        return fitness

    def population_evolution(self) -> Callable:
        """The population-based evolution loop. Returns the fittest function in the final population.

        Returns
        -------
        fittest_function : Callable
            The fittest function in the final population.

        Examples
        ------
        >>> pp = ProgramGSGP(3, 3, 2, 3, 100, 2, 0.5, lambda *x: ((args[0] + args[1]) % ncl) + 1)
        >>> pp.create_vars()
        >>> fittest_function = pp.population_evolution()
        >>> fittest_function.genotype()
        '2 if True else (x0 if True else x1)'
        """
        program = ProgramPopulation()
        population = program.create_program_population(
            self.depth, self.vars, self.pop_size)
        seed = random.randint(0, 10000000)
        for generation in range(self.generations):
            graded_population = [(self.program_fitness(
                individual, seed), individual) for individual in population]
            sorted_population = sorted(graded_population, key=lambda x : x[0])
            new_parents = sorted_population[:int(self.trunc*self.pop_size)]
            if generation == self.generations - 1:
                break
            for i in range(self.pop_size):
                parent = random.sample(new_parents, 2)
                population[i] = self.program_mutation(
                    self.program_crossover(parent[0][1], parent[1][1]))
        return sorted_population[0][1]

    def hill_climbing(self) -> Callable:
        """The main function for the hill climbing algorithm. Returns the fittest function.

        Returns
        -------
        fittest_function : Callable
            The fittest function.

        Examples
        ------
        >>> pp = ProgramGSGP(3, 3, 2, 3, 100, 2, 0.5, lambda *x: ((args[0] + args[1]) % ncl) + 1)
        >>> pp.create_vars()
        >>> fittest_function = pp.hill_climbing()
        >>> fittest_function.genotype()
        '2 if True else (x0 if True else x1)'
        """
        seed = random.randint(0, 10000000)
        current = ProgramPopulation().create_program_function(self.depth, self.vars)
        current.fitness = self.program_fitness(current, seed)

        for i in range(self.generations + 1):
            offspring = self.program_mutation(current)
            offspring.fitness = self.program_fitness(offspring, seed)
            if offspring.fitness < current.fitness:
                print("Change current: " + str(current.fitness) + " -> offspring " +
                      str(offspring.fitness) + " | " + str(i) + " generations")
                current = offspring
        return current
