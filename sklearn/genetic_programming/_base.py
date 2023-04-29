# Author: Adarsh Prusty

import random
from typing import Any, Callable, List, Tuple


def memoize(f: Callable) -> Callable:
    """A decorater function that caches the results of a given function f.

    Parameters
    ----------
    f : Callable
        The function to be memoised.

    Returns
    -------
    decorated_function : Callable
        A decorated version of the function that caches its results.
    """
    f.cache = {}  # Creates an empty cache for the function f.

    def decorated_function(*args: Tuple[Any]) -> Any:
        """A decorated version of the function f that caches it's results.

        Parameters
        ----------
        *args : tuple
            The arguments to be passed to the function f.

        Returns
        -------
        result : any
            The result of the function f with the given arguments.
        """
        if args in f.cache:  # if the result is already in the cache, return it
            return f.cache[args]
        else:  # otherwise, compute the result and cache it
            f.cache[args] = f(*args)
            return f.cache[args]
    return decorated_function


class BooleanPopulation:
    """A class that is used to create a population of Boolean functions."""

    def __create_boolean_expression(self, depth: int, vars: List[str]) -> str:
        """Create a random Boolean expression using recursion.

        Parameters
        ----------
        depth : int
            The depth of the recursion tree.
        vars : List[str]
            A list of variables used to construct the expression.

        Returns
        -------
        expression : str
            The randomly generated Boolean expression.

        Examples
        ------
        >>> bp = BooleanPopulation()
        >>> bp.create_boolean_expression(2, ['x1', 'x2'])
        '(x1 and x2) or (x1 and x2)'
        """
        if depth == 1 or random.random() < 1.0 / (2 ** depth - 1):
            return random.choice(vars)
        if random.random() < 1.0 / 3:
            return 'not' + ' ' + self.create_boolean_expression(depth - 1, vars)
        else:
            return '(' + self.create_boolean_expression(depth - 1, vars) + ' ' + random.choice(
                ['and', 'or']) + ' ' + self.create_boolean_expression(depth - 1, vars) + ')'

    def create_boolean_function(self, depth: int, vars: List[str]) -> Callable:
        """Create a random Boolean function.

        Parameters
        ----------
        depth : int
            The depth of the recursion tree.
        vars : List[str]
            A list of variables used to construct the expression.

        Returns
        -------
        boolean_function : Callable
            The randonly generated Boolean function.

        Examples
        ------
        >>> bp = BooleanPopulation()
        >>> bf = bp.create_boolean_function(2, ['x1', 'x2'])
        >>> bf(True, False)
        False
        """
        expression = self.create_boolean_expression(depth, vars)
        # create function of n input variables
        boolean_function = eval('lambda ' + ', '.join(vars) + ': ' + expression)
        boolean_function = memoize(boolean_function)  # add cache to the function
        boolean_function.genotype = lambda: expression  # store genotype within function
        return boolean_function

    def create_boolean_population(self, depth: int, vars: List[str], population_size: int) -> List[Callable]:
        """Create a population of random Boolean functions.

        Parameters
        ----------
        depth : int
            The depth of the recursion tree.
        vars : List[str]
            A list of variables used to construct the expression.
        population_size : int
            The size of the population.

        Returns
        -------
        population : List[Callable]
            The population of randomly generated Boolean functions.

        Examples
        ------
        >>> bp = BooleanPopulation()
        >>> population = bp.create_boolean_population(2, ['x1', 'x2'], 10)
        >>> population[0](True, False)
        False
        """
        return [self.create_boolean_function(depth, vars) for _ in range(population_size)]


class ArithmeticPopulation:
    """A class that is used to create a population of Arithmetic functions."""

    def __create_arithmetic_expression(self, polynomial_degree: int) -> str:
        """Create a random arithmetic expression using recursion.

        Parameters
        ----------
        polynomial_degree : int
            The degree of the polynomial to be constructed.

        Returns
        -------
        expression : str
            The generated polynomial expression, using [+, -] as operators and [x] as the variable.

        Examples
        ------
        >>> ap = ArithmeticPopulation()
        >>> ap.__create_arithmetic_expression(3)
        '0.5 * x ** 0 + 0.5 * x ** 1 + 0.5 * x ** 2'        
        """
        expression = ''
        for i in range(polynomial_degree):
            # generate real number between -1 and 1
            expression += str(random.uniform(-1, 1)) + ' * x ** ' + \
                              str(i) + str(random.choice([' + ', ' - ']))
        return expression[:-3]

    def create_arithmetic_function(self, polynomial_degree: int) -> Callable:
        """Create a random arithmetic function.

        Parameters
        ----------
        polynomial_degree : int
            The degree of the polynomial to be constructed.

        Returns
        -------
        arithmetic_function : Callable
            The generated arithmetic function.

        Examples
        ------
        >>> ap = ArithmeticPopulation()
        >>> af = ap.create_arithmetic_function(3)
        >>> af(2)
        2.0
        """
        expression = self.__create_arithmetic_expression(polynomial_degree)
        # create function of n input variables
        arithmetic_function = eval('lambda x: ' + expression)
        arithmetic_function = memoize(arithmetic_function)  # add cache to the function
        arithmetic_function.genotype = lambda: expression  # store genotype within function
        return arithmetic_function

    def create_arithmetic_population(self, polynomial_degree: int, population_size: int) -> List[Callable]:
        """Create a population of random arithmetic functions.

        Parameters
        ----------
        polynomial_degree : int
            The degree of the polynomial to be constructed.
        population_size : int
            The size of the population.

        Returns
        -------
        population : List[Callable]
            The population of randomly generated arithmetic functions.

        Examples
        ------
        >>> ap = ArithmeticPopulation()
        >>> population = ap.create_arithmetic_population(3, 10)
        >>> population[0](2)
        2.0
        """
        return [self.create_arithmetic_function(polynomial_degree) for _ in range(polynomial_degree, population_size)]


class ProgramPopulation:
    """A class to create a population of random programs."""

    def __create_program_expression(self, depth: int, vars: List[str]) -> str:
        """Create a random program expression using recursion.

        Parameters
        ----------
        depth : int
            The depth of the recursion tree.
        vars : List[str]
            The list of variables used to construct the expression.

        Returns
        -------
        expression : str
            The generated program expression.

        Examples
        ------
        >>> pp = ProgramPopulation()
        >>> pp.__create_program_expression(2, ['x1', 'x2'])
        'x1 if 0 else x2'
        """
        if depth == 1 or random.random() < 1.0 / (2 ** depth - 1):
            return random.choice(vars)
        else:
            return '(' + self.__create_program_expression(depth - 1, vars) + ' if ' + random.choice(['0', '1']) + ' else ' + self.__create_program_expression(depth - 1, vars) + ')'

    def create_program_function(self, depth: int, vars: List[str]) -> Callable:
        """Create a random program function.

        Parameters
        ----------
        depth : int
            The depth of the recursion tree.
        vars : List[str]
            The list of variables used to construct the expression.

        Returns
        -------
        program_function : Callable
            The generated program function.

        Examples
        ------
        >>> pp = ProgramPopulation()
        >>> pf = pp.__create_program_function(2, ['x1', 'x2'])
        >>> pf(1, 2, 3)
        2
        """
        expression = self.__create_program_expression(depth, vars)
        # create function of n input variables
        program_function = eval('lambda ' + ', '.join(vars) + ': ' + expression)
        program_function = memoize(program_function)  # add cache to the function
        program_function.genotype = lambda: expression  # store genotype within function
        return program_function

    def create_program_population(self, depth: int, vars: List[str], population_size: int) -> List[Callable]:
        """Create a population of random program functions.

        Parameters
        ----------
        depth : int
            The depth of the recursion tree.
        vars : List[str]
            The list of variables used to construct the expression.
        population_size : int
            The size of the population.

        Returns
        -------
        population : List[Callable]
            The population of randomly generated program functions.

        Examples
        ------
        >>> pp = ProgramPopulation()
        >>> population = pp.create_program_population(2, ['x1', 'x2'], 10)
        >>> population[0](1, 2)
        2
        """
        return [self.create_program_function(depth, vars) for _ in range(population_size)]
