from Functions import  one_max_ga

n_bits = 30
n_init_pop = 100

mutation_rate = 0.01
crossover_rate = 0.8

tournament_size = 5
generations = 50


def fitness(bit_string):
    return bit_string.count('1')


one_max_ga(fitness, n_bits, n_init_pop, generations, tournament_size, crossover_rate, mutation_rate)

