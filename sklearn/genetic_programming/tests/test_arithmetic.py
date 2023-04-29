
def arith_target_funct(arg):
    return arg**2 + 1


arith_gp  = GeneticProgram(1, 4, 100, 30, 0.5, arith_target_funct)
arith_gp.create_vars()
print(arith_gp.real_population_evolution(), arith_target_funct(0))

print("END OF ARITHMETIC")
