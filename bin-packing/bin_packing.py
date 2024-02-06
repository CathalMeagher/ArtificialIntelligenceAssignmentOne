import random
from matplotlib import pyplot as plt


def load_problems():
    bpp_problems = []
    # Problems were split up in to separate files
    for x in range(1, 6):
        problem_array = open('BPP_' + str(x) + '.txt').read().split()
        problem = {
            'number_of_item_weights': problem_array[0],
            'capacity': problem_array[1],
            'items': [],
            'total_item_weight': 0
        }

        for y in range(2, len(problem_array), 2):
            # Add each item into the array x times
            item_weight = [int(problem_array[y])] * int(problem_array[y + 1])
            problem['items'].extend(item_weight)
        problem['total_item_weight'] = sum(problem['items'])
        bpp_problems.append(problem)
    return bpp_problems


pop_size = 50
initial_bins = 50
capacity = 1000
generations = 250

mutation_rate = 0.01
crossover_rate = 0.8

# Capacity is the same for all problems
capacity = 1000


def calculate_fitness(solution, items):
    bins = {}
    # Loop over our solutions, and collect the weight
    # Of each bin
    for idx, bin in enumerate(solution):
        weight = items[idx]
        if bin not in bins:
            bins[bin] = weight
        else:
            bins[bin] += weight

    # If any of the weights of the bins are over the capacity
    # Then add 2 as a penalty
    invalid_solutions = 0
    for weight in bins.values():
        if weight > capacity:
            invalid_solutions += 2

    # Fitness is number of bins used + invalid solutions
    # A lower value here is better
    return len(bins) + invalid_solutions


def calculate_average_population_fitness(population, items):
    fitness = 0
    for solution in population:
        fitness += calculate_fitness(solution, items)
    return fitness / len(population)


def tournament_selection(population, items):
    parents = []
    # Select two parents
    for _ in range(2):
        # Perform tournament selection
        # Randomly select 10 individuals
        individuals = random.sample(population, 10)
        best = individuals[0]
        # Select the individual with the best fitness of the ten selected
        for individual in individuals[1:]:
            # Lower is better
            if calculate_fitness(individual, items) < calculate_fitness(best, items):
                best = individual
        parents.append(best)
    return parents


def crossover(parent_1, parent_2):
    # Perform crossover 80% of the time
    if random.random() < crossover_rate:
        # Select a random point to perform crossover
        # Ensuring we don't select the last point (hence -2)
        crossover_point = random.randint(1, len(parent_1) - 2)
        child_1 = parent_1[:crossover_point] + parent_2[crossover_point:]
        child_2 = parent_2[:crossover_point] + parent_1[crossover_point:]

        return child_1, child_2
    else:
        return parent_1, parent_2


def mutate(individual):
    # Randomly switch the bin an item is using 1% of the time
    for i in range(len(individual)):
        if random.random() < mutation_rate:
            individual[i] = random.randint(1, pop_size)


def create_initial_population(problem_instance):
    population = []
    # Loop over our population pop_size times
    for _ in range(pop_size):
        individual = []
        # Loop over items and assign a random bin to the item
        for _ in problem_instance['items']:
            individual.append(random.randint(0, initial_bins - 1))
        population.append(individual)
    return population


def binpacking_ga(problem):
    items = problem['items']
    # Initialize population
    population = create_initial_population(problem)
    best_solution = population[0]
    generation_average_fitness = []

    for generation in range(generations):
        new_population = []
        # Only loop over half of population as we are selecting two parents
        # And creating two children each time
        # This ensures population size remains constant
        for _ in range(pop_size // 2):
            # Selection, crossover, mutation
            parent_1, parent_2 = tournament_selection(population, items)
            child_1, child_2 = crossover(parent_1, parent_2)
            mutate(child_1)
            mutate(child_2)
            new_population.extend([child_1, child_2])

        population = new_population
        average_fitness = calculate_average_population_fitness(population, items)
        current_best_fitness = calculate_fitness(best_solution, items)
        for individual in population:
            if calculate_fitness(individual, items) < current_best_fitness:
                best_solution = individual
        generation_average_fitness.append(average_fitness)
    return len(set(best_solution)), generation_average_fitness


if __name__ == "__main__":
    plt.figure(figsize=(15, 10))

    bpp_problems = load_problems()
    for idx, problem in enumerate(bpp_problems):
        # Calculate the average fitness of each problem and plot
        capacity = int(problem['capacity'])
        best_solution_num_of_bins, avg_fitness_over_generations = binpacking_ga(problem)
        print(f"Problem {idx+1} solved with bins: {best_solution_num_of_bins}")
        plt.plot(avg_fitness_over_generations, label=f"Problem: {idx + 1}")

    plt.title("Average Population Fitness Over Time")
    plt.xlabel("Number of Generations")
    plt.ylabel("Average Fitness (lower is better)")
    plt.legend()
    plt.grid()
    plt.savefig('problem_four_bins.png')
    plt.show()
