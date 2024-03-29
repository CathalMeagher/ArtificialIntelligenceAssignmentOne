from Functions import generate_bit_string, one_max_ga, plot_generation_fitness

n_bits = 30
n_init_pop = 1000

mutation_rate = 0.01
crossover_rate = 0.8

tournament_size = 10
generations = 50

target_string = generate_bit_string(n_bits)


def fitness(bit_string):
    count = 0
    for x in range(n_bits):
        if bit_string[x] == target_string[x]:
            count += 1
    return count


pop, generation_fitness = one_max_ga(fitness, n_bits, n_init_pop, generations, tournament_size, crossover_rate, mutation_rate)
plot_generation_fitness(generation_fitness)

