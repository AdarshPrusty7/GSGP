import csv

# This script runs each of the Boolean, Arithmetic and Program genetic programs with different parameters 30 times and records the results in a CSV file.

from _arithmetic_domain import ArithmeticGSGP
from _boolean_domain import BooleanGSGP
from _program_domain import ProgramGSGP


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



for _ in range(1):
    gp = BooleanGSGP(6, 3, 10, 30, 0.5, multiplexer6)
    fittest_function = gp.population_evolution()
    print(fittest_function(True, True, True, False, False, True))
    print(multiplexer6(True, True, True, False, False, True))


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
    count = 0
    for i in range(6):
        if a[i] != b[i+6]:
            count += 1
    return count

# Comparator8 function
def comparator8(*args):
    count = 0
    for i in range(8):
        if a[i] != b[i+8]:
            count += 1
    return count

# Comparator10 function
def comparator10(*args):
    count = 0
    for i in range(10):
        if a[i] != b[i+10]:
            count += 1
    return count

def true(*args):
    return 1

def random(*args):
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

# create csv file
with open('data.csv', 'w', newline='') as file:
    # create writer
    writer = csv.writer(file)


 # we want to test each function 30 times and record the results in data.csv
    for i in range(30):
        