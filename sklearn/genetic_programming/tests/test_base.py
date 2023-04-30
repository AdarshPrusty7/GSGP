from typing import Callable, List

from .._base import (ArithmeticPopulation, BooleanPopulation,
                     ProgramPopulation, memoize)

# Tests made to be run with pytest

# UNIT TESTS

def test_memoize():
    def my_func(a: int, b: int) -> int:
        return a  * b
    memoized_func = memoize(my_func)

    # Ensure that calling the memoized function returns the same result atwice
    assert memoized_func(2, 3) == 6
    assert memoized_func(2, 3) == 6

    # Ensure that calling the memoized function with different arguments computes and caches the results correctly
    assert memoized_func(2, 4) == 8
    assert memoized_func(3, 4) == 12


## Boolean Population
class TestBooleanPopulation:
    def test_create_boolean_expression(self):
        depth = 3
        vars = ['x0', 'x1', 'x2', 'x3', 'x4']
        bool = BooleanPopulation()
        for i in range(30):
            expr = bool.create_boolean_expression(depth, vars)
            assert len(expr) > 0
            assert isinstance(expr, str)
    
    def test_create_boolean_function(self):
        depth = 3
        vars = ['x0', 'x1', 'x2', 'x3', 'x4']
        bool = BooleanPopulation()
        for _ in range(30):
            func = bool.create_boolean_function(depth, vars)
            assert len(func.genotype()) > 0
            assert isinstance(func, Callable)
            assert isinstance(func.genotype(), str)
            assert func(True, True, True, True, True) in [True, False]
            assert func(False, False, False, False, False) in [True, False]

    def test_create_boolean_population(self):
        pop_size = 10
        depth = 3
        vars = ['x0', 'x1', 'x2', 'x3', 'x4']
        bool = BooleanPopulation()
        pop = bool.create_boolean_population(depth, vars, pop_size)
        assert len(pop) == pop_size
        assert isinstance(pop, List)
        for p in pop:
            assert isinstance(p, Callable)
            assert isinstance(p.genotype(), str)
            assert p(True, True, True, True, True) in [True, False]
            assert p(False, False, False, False, False) in [True, False]

# Arithmetic Population
class TestArithmeticPopulation:
    def test_create_arithmetic_expression(self):
        polynomial_degree = 3
        arith = ArithmeticPopulation()
        for _ in range(30):
            expr = arith.create_arithmetic_expression(polynomial_degree)
            assert len(expr) > 0
            assert isinstance(expr, str)

    def test_create_arithmetic_function(self):
        polynomial_degree = 3
        arith = ArithmeticPopulation()
        for i in range(30):
            func = arith.create_arithmetic_function(polynomial_degree)
            assert len(func.genotype()) > 0
            assert isinstance(func, Callable)
            assert isinstance(func.genotype(), str)
            assert isinstance(func(-1.0), float)
            assert isinstance(func(1.0), float)

    def test_create_arithmetic_population(self):
        polynomial_degree = 3
        pop_size = 10
        arith = ArithmeticPopulation()
        pop = arith.create_arithmetic_population(polynomial_degree, pop_size)
        assert len(pop) == pop_size
        assert isinstance(pop, List)
        for p in pop:
            assert isinstance(p, Callable)
            assert isinstance(p.genotype(), str)
            assert isinstance(p(-1.0), float)
            assert isinstance(p(1.0), float)

# Program Population
class TestProgramPopulation:
    def test_create_program_expression(self):
        depth = 3
        vars = ['x0', 'x1', 'x2', 'x3', 'x4']
        program = ProgramPopulation()
        for i in range(30):
            expr = program.create_program_expression(depth, vars)
            assert len(expr) > 0
            assert isinstance(expr, str)

    def test_create_program_function(self):
        depth = 3
        vars = ['x0', 'x1', 'x2']
        program = ProgramPopulation()
        for _ in range(30):
            func = program.create_program_function(depth, vars)
            assert len(func.genotype()) > 0
            assert isinstance(func, Callable)
            assert isinstance(func.genotype(), str)
            assert func(1, 2, 3) in [1, 2, 3]

    def test_create_program_population(self):
        depth = 3
        vars = ['x0', 'x1', 'x2']
        pop_size = 10
        program = ProgramPopulation()
        pop = program.create_program_population(depth, vars, pop_size)
        assert len(pop) == pop_size
        assert isinstance(pop, List)
        for p in pop:
            assert isinstance(p, Callable)
            assert isinstance(p.genotype(), str)
            assert p(1, 2, 3) in [1, 2, 3]
