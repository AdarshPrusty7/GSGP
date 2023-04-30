import os
import sys #isort:skip
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))) #isort:skip
from typing import Callable, List

from _program_domain import ProgramGSGP


class TestProgramGSGP:
    # Unit tests for the ProgramGSGP class.
    def test_crossover(self):
        # Tests the program crossover method.
        f1 = lambda x0, x1, x2: x0 if 1 else x1
        f1.genotype = lambda: '(x0 if 1 else x1)'
        f2 = lambda x0, x1, x2: x0 if 0 else x2
        f2.genotype = lambda: '(x0 if 0 else x2)'
        nc, nv, ncl = 3, 3, 4
        for _ in range(30):
            offspring = ProgramGSGP(nc, nv, ncl, 3, 10, 30, 0.5, f1).crossover(f1, f2)
            assert isinstance(offspring, Callable)
            assert isinstance(offspring.genotype(), str)
            assert offspring(1, 2, 3) in [1, 2, 3, 4]
            assert offspring(1, 2, 1) in [1, 2, 3, 4]

    def test_mutation(self):
        # Tests the program mutation method.
        f = lambda x0, x1, x2: x0 if 1 else x1
        f.genotype = lambda: '(x0 if 1 else x1)'
        nc, nv, ncl = 3, 3, 4
        for _ in range(30):
            offspring = ProgramGSGP(nc, nv, ncl, 3, 10, 30, 0.5, f).mutation(f)
            assert isinstance(offspring, Callable)
            assert isinstance(offspring.genotype(), str)
            assert offspring(1, 2, 3) in [1, 2, 3, 4]
            assert offspring(1, 2, 1) in [1, 2, 3, 4]

    def test_fitness(self):
        # Tests the program fitness method.
        f = lambda x0, x1, x2: x0 if 1 else x1
        f.genotype = lambda: '(x0 if 1 else x1)'
        f2 = lambda x0, x1, x2: x0 if 0 else x2
        f2.genotype = lambda: '(x0 if 0 else x2)'
        nc, nv, ncl = 3, 3, 4
        for _ in range(30):
            fitness_ideal = ProgramGSGP(nc, nv, ncl, 3, 10, 30, 0.5, f).fitness(f, 1)
            assert isinstance(fitness_ideal, int)
            assert fitness_ideal == 0
            fitness_not_ideal = ProgramGSGP(
                nc, nv, ncl, 3, 10, 30, 0.5, f).fitness(f2, 1)
            assert isinstance(fitness_not_ideal, int)
            # Due to the functions we chose and the fitness function, the fitness of f2 is always 24, with this seed.
            # In general it is not 24, but it is greater than 0.
            assert fitness_not_ideal == 24

    # Integration tests
    # We don't test to see if the genotype is a string, because evaluating this takes a while
    def test_population_evolution(self):
        # Tests the program population_evolution method.
        nc, nv, ncl = 3, 3, 2

        def target_function(*args):
            return ((args[0] + args[1]) % ncl) + 1
        for _ in range(2):
            gp = ProgramGSGP(nc, nv, ncl, 4, 10, 30, 0.5, target_function)
            fittest_function = gp.population_evolution()
            assert isinstance(fittest_function, Callable)
            assert fittest_function(1, 2, 3) in [1, 2]

        nc, nv, ncl = 3, 3, 4
        for _ in range(2):
            gp = ProgramGSGP(nc, nv, ncl, 4, 100, 60, 0.5, target_function)
            fittest_function = gp.population_evolution()
            assert isinstance(fittest_function, Callable)
            assert fittest_function(1, 2, 3) in [1, 2, 3, 4]

        nc, nv, ncl = 3, 3, 8
        for _ in range(2):
            gp = ProgramGSGP(nc, nv, ncl, 4, 100, 120, 0.5, target_function)
            fittest_function = gp.population_evolution()
            assert isinstance(fittest_function, Callable)
            assert fittest_function(1, 2, 3) in [1, 2, 3, 4, 5, 6, 7, 8]
