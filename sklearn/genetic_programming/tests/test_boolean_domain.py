import os
import sys  # isort:skip
sys.path.insert(0, os.path.abspath(os.path.join(
    os.path.dirname(__file__), '..')))  # isort:skip
from _boolean_domain import BooleanGSGP
from typing import Callable, List


class TestBooleanGSGP:
    # Unit tests for the BooleanGSGP class.
    def test_crossover(self):
        # Tests the boolean crossover method
        f1 = lambda x0, x1, x2: x0 and x1
        f1.genotype = lambda: 'x0 and x1'
        f2 = lambda x0, x1, x2: x1 or not x2
        f2.genotype = lambda: 'x1 or not x2'
        for _ in range(30):
            offspring = BooleanGSGP(3, 4, 10, 30, 0.5, f1).crossover(f1, f2)
            assert isinstance(offspring, Callable)
            assert isinstance(offspring.genotype(), str)
            assert isinstance(offspring(True, True, True), bool)
            assert isinstance(offspring(False, False, False), bool)

    def test_mutation(self):
        # Tests the boolean mutation method
        f = lambda x0, x1, x2: x0 and x1
        f.genotype = lambda: 'x0 and x1'
        for _ in range(30):
            offspring = BooleanGSGP(3, 4, 10, 30, 0.5, f).mutation(f)
            assert isinstance(offspring, Callable)
            assert isinstance(offspring.genotype(), str)
            assert isinstance(offspring(True, True, True), bool)
            assert isinstance(offspring(False, False, False), bool)

    def test_fitness(self):
        # Tests the boolean fitness method
        f = lambda x0, x1, x2: x0 and x1
        f.genotype = lambda: 'x0 and x1'
        f2 = lambda x0, x1, x2: x1 or not x2
        f2.genotype = lambda: 'x1 or not x2'
        for _ in range(30):
            fitness_ideal = BooleanGSGP(3, 4, 10, 30, 0.5, f).fitness(f)
            assert isinstance(fitness_ideal, int)
            assert fitness_ideal == 0
            fitness_not_ideal = BooleanGSGP(3, 4, 10, 30, 0.5, f).fitness(f2)
            assert isinstance(fitness_not_ideal, int)
            # Due to the functions we chose, this should always be 4 since inputs are not randomised.
            assert fitness_not_ideal == 4

    # Integration tests for the BooleanGSGP class.
    def test_population_evolution(self):
        # Tests the boolean population_evolution method
        def target_function(*args):
            return args.count(True) % 2 == 1
        for _ in range(10):
            gp = BooleanGSGP(3, 3, 10, 30, 0.5, target_function)
            fittest_function = gp.population_evolution()
            assert isinstance(fittest_function, Callable)
            assert isinstance(fittest_function(True, True, True), bool)
            assert isinstance(fittest_function(False, False, False), bool)
            assert fittest_function(
                True, True, True) == target_function(True, True, True)

    def test_hill_climbing(self):
        # Tests the boolean hill_climbing method.
        def target_function(*args):
            return args.count(True) % 2 == 1
        for _ in range(10):
            gp = BooleanGSGP(3, 3, 10, 100, 0.5, target_function)
            fittest_function = gp.hill_climbing()
            assert isinstance(fittest_function, Callable)
            assert isinstance(fittest_function.genotype(), str)
            assert isinstance(fittest_function(True, True, True), bool)
            assert isinstance(fittest_function(False, False, False), bool)
            assert fittest_function(
                True, True, True) == target_function(True, True, True)
