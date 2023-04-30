import pytest
import sys




# We seperate these tests into individual unit tests and whole population tests.
# UNIT TESTS
## Boolean Population

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



"""vars = ['x0', 'x1', 'x2', 'x3', 'x4', 'x5']

bool = BooleanPopulation()
pop_bool = bool.create_boolean_population(4, vars, 5)
print([p.genotype() for p in pop_bool])

arith = ArithmeticPopulation()
pop_arith = arith.create_arithmetic_population(5)
print([p.genotype() for p in pop_arith])

prog = ProgramPopulation()
pop_prog = prog.create_program_population(4, vars, 5)
print([p.genotype() for p in pop_prog])
"""