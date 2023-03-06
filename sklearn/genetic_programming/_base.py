
import random

def memoize(f):
    'Add a cache memory to the input function.'
    f.cache = {}
    def decorated_function(*args):
        if args in f.cache:
            return f.cache[args]
        else:
            f.cache[args] = f(*args)
            return f.cache[args]
    return decorated_function

class BooleanPopulation:
    def __init__(self):
        self.population = []

    def __create_boolean_expression(self, depth, vars):
        'Create a random Boolean expression using recursion.'
        if depth == 1 or random.random() < 1.0 / (2 ** depth - 1):
            return random.choice(vars)
        if random.random() < 1.0 / 3:
            return 'not' + ' ' + self.__create_boolean_expression(depth - 1, vars)
        else:
            return '(' + self.__create_boolean_expression(depth - 1, vars) + ' ' + random.choice(['and', 'or']) + ' ' + self.__create_boolean_expression(depth - 1, vars) + ')'

    def create_boolean_function(self, depth, vars):
        'Create a random Boolean function.'
        expression = self.__create_boolean_expression(depth, vars)
        boolean_function = eval('lambda ' + ', '.join(vars) + ': ' + expression)  # create function of n input variables
        boolean_function = memoize(boolean_function)  # add cache to the function
        boolean_function.genotype = lambda: expression  # store genotype within function
        return boolean_function

    def create_boolean_population(self, depth, vars, population_size):
        'Create population of Boolean functions.d'
        self.population = [self.create_boolean_function(depth, vars) for _ in range(population_size)]

    def get_boolean_population(self):
        'Return population of Boolean functions.'
        return self.population

class ArithmeticPopulation:
    def __init__(self):
        self.population = []

    def __create_arithmetic_expression(self, depth, vars):
        'Create a random arithmetic expression using recursion.'
        if depth == 1 or random.random() < 1.0 / (2 ** depth - 1):
            return random.choice(vars)
        pass



    def __create_arithmetic_function(self, depth, vars):
        'Create a random arithmetic function.'
        pass

    def create_arithmetic_population(self, depth, vars, population_size):
        'Create population of arithmetic functions.'
        pass

    def get_arithmetic_population(self):
        'Return population of arithmetic functions.'
        pass


class ProgramPopulation:
    def __init__(self):
        self.population = []

    def __create_program_expression(self, depth, vars):
        'Create a random program expression using recursion.'
        if depth == 1 or random.random() < 1.0 / (2 ** depth - 1):
            return random.choice(vars)
            

    def __create_program_function(self, depth, vars):
        'Create a random program function.'
        pass

    def create_program_population(self, depth, vars, population_size):
        'Create population of program functions.'
        pass

    def get_program_population(self):
        'Return population of program functions.'
        pass


boolean = BooleanPopulation()
boolean.create_boolean_population(4, ['x1', 'x2', 'x3', 'x4', 'x5'], 5)
print(boolean.get_boolean_population()[0].genotype())
print([x.genotype() for x in boolean.get_boolean_population()])