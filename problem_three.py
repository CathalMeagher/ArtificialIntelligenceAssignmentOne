from Functions import pop_fitness, generate_bit_string, tournament_selection, crossover, mutate, plot_generation_fitness

n_bits = 30
n_init_pop = 1000

mutation_rate = 0.01
crossover_rate = 0.8

tournament_size = 10
generations = 200


def deceptive_fitness(bit_string):
    if '1' not in bit_string:
        return 2 * len(bit_string)
    return bit_string.count('1')


def one_max_ga():
    pop = [generate_bit_string(n_bits) for _ in range(0, n_init_pop)]
    generation_fitness = [pop_fitness(pop, deceptive_fitness)]

    for generation in range(generations):
        parents = [tournament_selection(pop, tournament_size, deceptive_fitness) for _ in range(n_init_pop)]

        children = []
        for x in range(0, len(parents), 2):
            parent_1 = parents[x]
            parent_2 = parents[x + 1]

            child1, child2 = crossover(parent_1, parent_2, crossover_rate, n_bits)
            children.append(child1)
            children.append(child2)
        generation_fitness.append(pop_fitness(children, deceptive_fitness))
        pop = [mutate(child, mutation_rate) for child in children]
    return pop, generation_fitness


pop, generation_fitness = one_max_ga()
plot_generation_fitness(generation_fitness)
