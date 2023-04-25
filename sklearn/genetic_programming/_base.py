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
    def create_boolean_expression(self, depth, vars):
        'Create a random Boolean expression using recursion.'
        if depth == 1 or random.random() < 1.0 / (2 ** depth - 1):
            return random.choice(vars)
        if random.random() < 1.0 / 3:
            return 'not' + ' ' + self.create_boolean_expression(depth - 1, vars)
        else:
            return '(' + self.create_boolean_expression(depth - 1, vars) + ' ' + random.choice(
                ['and', 'or']) + ' ' + self.create_boolean_expression(depth - 1, vars) + ')'

    def create_boolean_function(self, depth, vars):
        'Create a random Boolean function.'
        expression = self.create_boolean_expression(depth, vars)
        boolean_function = eval('lambda ' + ', '.join(vars) + ': ' + expression)  # create function of n input variables
        boolean_function = memoize(boolean_function)  # add cache to the function
        boolean_function.genotype = lambda: expression  # store genotype within function
        return boolean_function

    def create_boolean_population(self, depth, vars, population_size):
        'Create population of Boolean functions.d'
        return [self.create_boolean_function(depth, vars) for _ in range(population_size)]

class ArithmeticPopulation:
    def __create_arithmetic_expression(self):
        'Create a univariate polynomial expression from 3 to 10 degrees'
        expression = ''
        for i in range(3):
            # generate real number between -1 and 1
            expression += str(str(random.uniform(-1, 1)) + ' * x ** ' + str(i) + str(random.choice([' + ',' - ' ])))
        return expression[:-3]

    def create_arithmetic_function(self):
        'Create a random arithmetic function.'
        expression = self.__create_arithmetic_expression()
        arithmetic_function = eval('lambda x'  + ': ' + expression)  # create function of n input variables
        arithmetic_function = memoize(arithmetic_function)  # add cache to the function
        arithmetic_function.genotype = lambda: expression  # store genotype within function
        return arithmetic_function

    def create_arithmetic_population(self, population_size):
        'Create population of arithmetic functions.'
        return [self.create_arithmetic_function() for _ in range(population_size)]


class ProgramPopulation:
    def __create_program_expression(self, depth, vars):
        'Create a random program expression using recursion.'
        if depth == 1 or random.random() < 1.0 / (2 ** depth - 1):
            return random.choice(vars)
        else:
            return '(' + self.__create_program_expression(depth - 1, vars) + ' if ' + self.__create_program_expression(depth - 1, vars) + ' else ' + self.__create_program_expression(depth - 1, vars) + ')'

    def __create_program_function(self, depth, vars):
        'Create a random program function.'
        expression = self.__create_program_expression(depth, vars)
        program_function = eval('lambda ' + ', '.join(vars) + ': ' + expression)  # create function of n input variables
        program_function = memoize(program_function)  # add cache to the function
        program_function.genotype = lambda: expression  # store genotype within function
        return program_function

    def create_program_population(self, depth, vars, population_size):
        'Create population of program functions.'
        return [self.__create_program_function(depth, vars) for _ in range(population_size)]



vars = ['x0', 'x1', 'x2', 'x3', 'x4', 'x5']

bool = BooleanPopulation()
pop_bool = bool.create_boolean_population(4, vars, 5)
print([p.genotype() for p in pop_bool])

arith = ArithmeticPopulation()
pop_arith = arith.create_arithmetic_population(5)
print([p.genotype() for p in pop_arith])

prog = ProgramPopulation()
pop_prog = prog.create_program_population(4, vars, 5)
print([p.genotype() for p in pop_prog])


