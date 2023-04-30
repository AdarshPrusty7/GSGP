def program_target_funct(*args):
    return ((args[0] + args[1]) % 2) + 1

"""
nc, nv, ncl = 3, 3, 4
IS = [i for i in range(1, nc + 1)]
OS = [i for i in range(1, ncl + 1)]
program_gp = GeneticProgram(nc, 4, 100, 25, 0.5, program_target_funct)
program_gp.create_vars()
program_gp.program_population_evolution()

print("END OF PROGRAM")"""