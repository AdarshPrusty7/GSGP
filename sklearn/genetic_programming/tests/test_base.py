
import pytest
import sys

from genetic_programming import _base




# We seperate these tests into individual unit tests and whole population tests.
# UNIT TESTS
## Boolean Population
def test_boolean_population():
    bool = BooleanPopulation()
    pop_bool = bool.create_boolean_population(4, ['x0', 'x1', 'x2', 'x3'], 5)
    assert len(pop_bool) == 5
    assert all([len(p.genotype()) == 4 for p in pop_bool])





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

test_boolean_population()