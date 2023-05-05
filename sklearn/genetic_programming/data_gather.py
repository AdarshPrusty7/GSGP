import csv
import math
import itertools
import random

# This script runs each of the Boolean, Arithmetic and Program genetic programs with different parameters 30 times and records the results in a CSV file.

from _arithmetic_domain import ArithmeticGSGP
from _boolean_domain import BooleanGSGP
from _program_domain import ProgramGSGP


def parity(*args):
    return args.count(True) % 2 == 1

# Multiplexer6 function
def multiplexer6(*args):
    address_bits = args[:2]
    data_bits = args[2:]

    # Calculate the index of the selected data bit.
    index = 0
    for i, bit in enumerate(address_bits):
        index += bit * (2 ** i)

    # Return the selected data bit.
    return data_bits[index]

# Multiplexer11 function
def multiplexer11(*args):
    address_bits = args[:3]
    data_bits = args[3:]

    # Calculate the index of the selected data bit.
    index = 0
    for i, bit in enumerate(address_bits):
        index += bit * (2 ** i)

    # Return the selected data bit.
    return data_bits[index]

# Comparator6 function
def comparator6(*args):
    a = args[:3]
    b = args[3:]
    for i in range(3):
        if a[i] != b[i]:
            return False
    return True

# Comparator8 function
def comparator8(*args):
    a = args[:4]
    b = args[4:]
    for i in range(4):
        if a[i] != b[i]:
            return False
    return True

# Comparator10 function
def comparator10(*args):
    a = args[:5]
    b = args[5:]
    for i in range(5):
        if a[i] != b[i]:
            False
    return True

def true(*args):
    return 1

def random_func(*args):
    return random.randint(0, 1)

######################

def polynomial(x, coefficients):
    """Evaluate polynomial at x given a list of coefficients"""
    return sum(c * x ** i for i, c in enumerate(coefficients))

# Third degree polynomial: f(x) = x^3 - 3x^2 + 4x - 1
f1 = lambda x: polynomial(x, [1, -3, 4, -1])

# Fourth degree polynomial: f(x) = 2x^4 + x^3 - 3x^2 + 4x - 1
f2 = lambda x: polynomial(x, [2, 1, -3, 4, -1])

# Fifth degree polynomial: f(x) = x^5 - x^4 + 2x^3 + 3x^2 - 2x + 1
f3 = lambda x: polynomial(x, [1, -1, 2, 3, -2, 1])

# Sixth degree polynomial: f(x) = x^6 - 2x^5 + 3x^4 + 4x^3 - 5x^2 + 6x - 1
f4 = lambda x: polynomial(x, [1, -2, 3, 4, -5, 6, -1])

# Seventh degree polynomial: f(x) = x^7 + 2x^6 - 3x^5 + 4x^4 - 5x^3 + 6x^2 - 7x + 1
f5 = lambda x: polynomial(x, [1, 2, -3, 4, -5, 6, -7, 1])

# Eighth degree polynomial: f(x) = 2x^8 + x^7 - 2x^6 + 3x^5 - 4x^4 + 5x^3 - 6x^2 + 7x - 1
f6 = lambda x: polynomial(x, [2, 1, -2, 3, -4, 5, -6, 7, -1])

# Ninth degree polynomial: f(x) = x^9 - 4x^8 + 3x^7 - 2x^6 + 5x^5 - 6x^4 + 7x^3 - 8x^2 + 9x - 1
f7 = lambda x: polynomial(x, [1, -4, 3, -2, 5, -6, 7, -8, 9, -1])

# Tenth degree polynomial: f(x) = 2x^10 + x^9 - 3x^8 + 4x^7 - 5x^6 + 6x^5 - 7x^4 + 8x^3 - 9x^2 + 10x - 1
f8 = lambda x: polynomial(x, [2, 1, -3, 4, -5, 6, -7, 8, -9, 10, -1])

######################

def program_function(*args):
    return ((args[0] + args[1]) % k[2]) + 1


######################

# create csv file called data.csv if it does not already exist
with open('data.csv', 'w', newline='') as file:
    # create writer
    writer = csv.writer(file)
    # headers: Target Function, Run Number, Best Fitness
    writer.writerow(["Domain", "Method", "Num of Vars", "Target Function", "Run Number", "Best Fitness"])

    # PARITY FUNCTIONS
    for n in range(7,8):
        target_funct = parity
        for i in range(30):
            pop_size = max(10, int(math.sqrt(n**2)))
            bp = BooleanGSGP(n, 3, pop_size, int((2*n)*2**n/(pop_size))*2, 0.5, target_funct)
            funct = bp.population_evolution()
            writer.writerow(["Boolean", "Population", n, target_funct.__name__, i, funct[0]])
            #now we run hill climbing on the same function
            nbp = BooleanGSGP(n, 4, pop_size, int((2*n)*2**n/(pop_size))*10, 0.5, target_funct)
            new_funct = nbp.hill_climbing()
            # write to csv file
            writer.writerow(["Boolean", "Hill Climbing", n, target_funct.__name__, i, new_funct[0]])
            print(i, n, target_funct.__name__)     
            
    
    """# COMPARATOR FUNCTIONS
    n = 6
    for i in range(30):
        target_function = comparator6
        pop_size = max(10, int(math.sqrt(n**2)))
        bp = BooleanGSGP(n, 3, pop_size, int((2*n)*2**n/(pop_size))*2, 0.5, target_function)
        funct = bp.population_evolution()
        # write to csv file
        writer.writerow(["Boolean", "Population", n, target_function.__name__, i, funct[0]])
        #now we run hill climbing on the same function
        nbp = BooleanGSGP(n, 4, pop_size, int((2*n)*2**n/(pop_size))*10, 0.5, target_function)
        new_funct = nbp.hill_climbing()
        # write to csv file
        writer.writerow(["Boolean", "Hill Climbing", n, target_function.__name__, i, new_funct[0]])
        print(i, n, target_function.__name__)

    n = 8
    for i in range(30):
        target_function = comparator8
        pop_size = max(10, int(math.sqrt(n**2)))
        bp = BooleanGSGP(n, 3, pop_size, int((2*n)*2**n/(pop_size))*2, 0.5, target_function)
        funct = bp.population_evolution()
        # write to csv file
        writer.writerow(["Boolean", "Population", n, target_function.__name__, i, funct[0]])
        #now we run hill climbing on the same function
        nbp = BooleanGSGP(n, 4, pop_size, int((2*n)*2**n/(pop_size))*10, 0.5, target_function)
        new_funct = nbp.hill_climbing()
        # write to csv file
        writer.writerow(["Boolean", "Hill Climbing", n, target_function.__name__, i, new_funct[0]])
        print(i, n, target_function.__name__)

    n = 10
    for i in range(30):
        target_function = comparator10
        pop_size = max(10, int(math.sqrt(n**2)))
        bp = BooleanGSGP(n, 3, pop_size, int((2*n)*2**n/(pop_size))*2, 0.5, target_function)
        funct = bp.population_evolution()
        # write to csv file
        writer.writerow(["Boolean", "Population", n, target_function.__name__, i, funct[0]])
        #now we run hill climbing on the same function
        nbp = BooleanGSGP(n, 4, pop_size, int((2*n)*2**n/(pop_size))*10, 0.5, target_function)
        new_funct = nbp.hill_climbing()
        # write to csv file
        writer.writerow(["Boolean", "Hill Climbing", n, target_function.__name__, i, new_funct[0]])
        print(i, n, target_function.__name__)

    # MULTIPLEXER FUNCTIONS
    n = 6
    for i in range(30):
        target_function = multiplexer6
        pop_size = max(10, int(math.sqrt(n**2)))
        bp = BooleanGSGP(n, 3, pop_size, int((2*n)*2**n/(pop_size))*2, 0.5, target_function)
        funct = bp.population_evolution()
        # write to csv file
        writer.writerow(["Boolean", "Population", n, target_function.__name__, i, funct[0]])
        #now we run hill climbing on the same function
        nbp = BooleanGSGP(n, 4, pop_size, int((2*n)*2**n/(pop_size))*10, 0.5, target_function)
        new_funct = nbp.hill_climbing()
        # write to csv file
        writer.writerow(["Boolean", "Hill Climbing", n, target_function.__name__, i, new_funct[0]])
        print(i, n, target_function.__name__)

    n = 11
    for i in range(30):
        target_function = multiplexer11
        pop_size = max(10, int(math.sqrt(n**2)))
        bp = BooleanGSGP(n, 3, pop_size, int((2*n)*2**n/(pop_size)), 0.5, target_function)
        funct = bp.population_evolution()
        # write to csv file
        writer.writerow(["Boolean", "Population", n, target_function.__name__, i, funct[0]])
        #now we run hill climbing on the same function
        nbp = BooleanGSGP(n, 4, pop_size, int((2*n)*2**n/(pop_size)), 0.5, target_function)
        new_funct = nbp.hill_climbing()
        # write to csv file
        writer.writerow(["Boolean", "Hill Climbing", n, target_function.__name__, i, new_funct[0]])
        print(i, n, target_function.__name__)

    # RANDOM FUNCTIONS
    for n in range(5, 12):
        target_funct = random_func
        for i in range(30):
            pop_size = max(10, int(math.sqrt(n**2)))
            bp = BooleanGSGP(n, 3, pop_size, int((2*n)*2**n/(pop_size)), 0.5, target_funct)
            funct = bp.population_evolution()
            writer.writerow(["Boolean", "Population", n, target_funct.__name__, i, funct[0]])
            #now we run hill climbing on the same function
            nbp = BooleanGSGP(n, 4, pop_size, int((2*n)*2**n/(pop_size)), 0.5, target_funct)
            new_funct = nbp.hill_climbing()
            # write to csv file
            writer.writerow(["Boolean", "Hill Climbing", n, target_funct.__name__, i, new_funct[0]])
            print(i, n, target_funct.__name__)

    # TRUE FUNCTIONS
    for n in range(5, 9):
        target_funct = true
        for i in range(30):
            pop_size = max(10, int(math.sqrt(n**2)))
            bp = BooleanGSGP(n, 3, pop_size, int((2*n)*2**n/(pop_size))*2, 0.5, target_funct)
            funct = bp.population_evolution()
            writer.writerow(["Boolean", "Population", n, target_funct.__name__, i, funct[0]])
            #now we run hill climbing on the same function
            nbp = BooleanGSGP(n, 4, pop_size, int((2*n)*2**n/(pop_size))*10, 0.5, target_funct)
            new_funct = nbp.hill_climbing()
            # write to csv file
            writer.writerow(["Boolean", "Hill Climbing", n, target_funct.__name__, i, new_funct[0]])
            print(i, n, target_funct.__name__)

    # ARITHMETIC FUNCTIONS
    for k in range(3, 11):
        target_funct = [f1, f2, f3, f4, f5, f6, f7, f8][k-3]
        for i in range(30):
            pop_size = 20
            ap = ArithmeticGSGP(k, pop_size, int(500*k/(pop_size)), 0.5, target_funct)
            funct = ap.population_evolution()
            writer.writerow(["Arithmetic", "Population", k, target_funct.__name__, i, funct[0]])
            #now we run hill climbing on the same function
            nap = ArithmeticGSGP(k, pop_size, int(500*k/(pop_size)), 0.5, target_funct)
            new_funct = nap.hill_climbing()
            # write to csv file
            writer.writerow(["Arithmetic", "Hill Climbing", k, target_funct.__name__, i, new_funct[0]])
            print(i, k, target_funct.__name__)

    # CLASIFIERS
    nc = [3, 4]
    nv = [3, 4]
    ncl = [2, 4, 8]

    combinations = itertools.product(nc, nv, ncl)
    combinations = list(map(list, combinations))
    for l, k in enumerate(combinations):
        target_funct = program_function
        for i in range(30):
            pop_size = max(10, int(math.sqrt(k[0]**k[1])))
            budget = 2* k[2] * k[1] * (k[0] ** k[1])
            cp = ProgramGSGP(k[0], k[1], k[2], 4, pop_size, int(budget/(pop_size)), 0.5, target_funct)
            funct = cp.population_evolution()
            writer.writerow(["Classifier", "Population", l, target_funct.__name__, i, funct[0]])
            #now we run hill climbing on the same function
            ncp = ProgramGSGP(k[0], k[1], k[2], 4, pop_size, int(budget/(pop_size))*10, 0.5, target_funct)
            new_funct = ncp.hill_climbing()
            # write to csv file
            writer.writerow(["Classifier", "Hill Climbing", l, target_funct.__name__, i, new_funct[0]])
            print(i, l, target_funct.__name__)"""
