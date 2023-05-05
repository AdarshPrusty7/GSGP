import os
import sys  # isort:skip
sys.path.insert(0, os.path.abspath(os.path.join(
    os.path.dirname(__file__), '..')))  # isort:skip
from _arithmetic_domain import ArithmeticGSGP
from typing import Callable, List


class TestArithmeticGSGP:
    # Unit tests for the ArithmeticGSGP class.
    def test_crossover(self):
        # Tests the real crossover method.
        f1 = lambda x: x**2
        f1.genotype = lambda: 'x**2'
        f2 = lambda x: x**3
        f2.genotype = lambda: 'x**3'
        for _ in range(30):
            offspring = ArithmeticGSGP(3, 10, 30, 0.5, f1).crossover(f1, f2)
            assert isinstance(offspring, Callable)
            assert isinstance(offspring.genotype(), str)
            assert isinstance(offspring(1), float)

    def test_mutation(self):
        # Tests the real mutation method.
        f = lambda x: x**2
        f.genotype = lambda: 'x**2'
        for _ in range(30):
            offspring = ArithmeticGSGP(3, 10, 30, 0.5, f).mutation(f)
            assert isinstance(offspring, Callable)
            assert isinstance(offspring.genotype(), str)
            assert isinstance(offspring(1), float)

    def test_fitness(self):
        # Tests the real fitness method.
        f = lambda x: x**2
        f.genotype = lambda: 'x**2'
        f2 = lambda x: x**3
        f2.genotype = lambda: 'x**3'
        for _ in range(30):
            fitness_ideal = ArithmeticGSGP(3, 10, 30, 0.5, f).fitness(f, 1)
            assert isinstance(fitness_ideal, float)
            assert fitness_ideal == 0.0
            fitness_not_ideal = ArithmeticGSGP(3, 10, 30, 0.5, f).fitness(f2, 1)
            assert isinstance(fitness_not_ideal, float)
            assert fitness_not_ideal > 0.0

    # Integration tests for the ArithmeticGSGP class.
    # We don't test to see if the genotype is a string, because evaluating this takes a while
    def test_population_evolution(self):
        # Tests the real population_evolution method.
        for _ in range(10):
            gp = ArithmeticGSGP(3, 20, 30, 0.5, lambda x: x**2 + 1)
            fittest_function = gp.population_evolution()[1]
            assert isinstance(fittest_function, Callable)
            assert isinstance(fittest_function(1), float)

    def test_hill_climbing(self):
        # Tests the real hill_climber method.
        for _ in range(10):
            gp = ArithmeticGSGP(3, 20, 400, 0.5, lambda x: x**2 + 1)
            fittest_function = gp.hill_climbing()[1]
            assert isinstance(fittest_function, Callable)
            assert isinstance(fittest_function(1), float)
