import random
import matplotlib.pyplot as plt
import numpy as np


# Common functions for problems 1,2,3
def mutate(child, mutation_rate):
    new_child = ''
    for x in child:
        if random.uniform(0, 1) < mutation_rate:
            new_child += '1' if x == '0' else '0'
        else:
            new_child += x
    return child


def crossover(parent_1, parent_2, crossover_rate, n_bits):
    if random.uniform(0, 1) < crossover_rate:
        crossover_point = random.randint(0, n_bits - 2)
        child_1 = parent_1[:crossover_point] + parent_2[crossover_point:]
        child_2 = parent_2[:crossover_point] + parent_1[crossover_point:]

        return child_1, child_2
    else:
        return parent_1, parent_2


def tournament_selection(population, tournament_size, fitness):
    tournament = random.sample(population, tournament_size)
    best = tournament[0]
    for x in range(1, tournament_size):
        if fitness(tournament[x]) > fitness(best):
            best = tournament[x]
    return best


def generate_bit_string(n_bits):
    bit_string = ""
    for _ in range(0, n_bits):
        bit_string += str(random.randint(0, 1))
    return bit_string


def pop_fitness(population, fitness):
    size = len(population)
    fitness_sum = 0
    for x in range(size):
        fitness_sum += fitness(population[x])
    return fitness_sum / size


def plot_generation_fitness(generation_fitness):
    plt.plot(np.array(generation_fitness), marker='.')
    plt.title("Average population fitness over time")
    plt.xlabel("Number of generations")
    plt.ylabel("Fitness")
    plt.show()


def one_max_ga(fitness, n_bits, n_init_pop, generations, tournament_size, crossover_rate, mutation_rate):
    pop = [generate_bit_string(n_bits) for _ in range(0, n_init_pop)]
    generation_fitness = [pop_fitness(pop, fitness)]

    for generation in range(generations):
        parents = [tournament_selection(pop, tournament_size, fitness) for _ in range(n_init_pop)]

        children = []
        for x in range(0, len(parents), 2):
            parent_1 = parents[x]
            parent_2 = parents[x + 1]

            child1, child2 = crossover(parent_1, parent_2, crossover_rate, n_bits)
            children.append(child1)
            children.append(child2)
        generation_fitness.append(pop_fitness(children, fitness))
        pop = [mutate(child, mutation_rate) for child in children]
    return pop, generation_fitness
