import numpy as np
import matplotlib.pyplot as plt
import random
import math
def calculate_distance(point1, point2):
    x1, y1 = point1
    x2, y2 = point2
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
def d(point1, point2, point3):
    x1, y1 = point1
    x2, y2 = point2
    x3, y3 = point3
    distance12 = calculate_distance(point1, point2)
    distance13 = calculate_distance(point1, point3)
    if distance12 == 0 or distance13 == 0:
        return 1
    value = ((x2 - x1) * (x3 - x2) + (y2 - y1) * (y3 - y2)) / (distance12 * distance13)
    value = np.clip(value, -1, 1)
    a = 3.14 - np.arccos(value)
    return a
def fitness(path):
    total_distance = 0
    # path_length = sum([calculate_distance(path[i], path[i + 1]) for i in range(len(path) - 1)])
    # print(f)
    for i in range(len(path) - 1):
        path_length = sum([calculate_distance(path[i], path[i + 1]) for i in range(len(path) - 1)])
        if path_length == 0:
            smooth = 0
        else:
            smooth = sum([d(path[i], path[i + 1], path[i + 2]) for i in range(len(path) - 2)]) / path_length
        total_distance += path_length * smooth
    fit = total_distance
    return (1 / fit)

def genetic_algorithm(population_size, num_generations, crossover_probability, mutation_probability):
    # Initialize the population

    population = np.random.randint(10, size=(population_size,10,2))
    best_fitness_values = []
    avg_fitness_values = []
    # Evolve the population
    for generation in range(num_generations):
        # Calculate the fitness of each individual
        fitness_values = np.array([fitness(individual) for individual in population])
        best_fitness = np.max(fitness_values)
        best_fitness_values.append(best_fitness)
        avg_fitness = np.mean(fitness_values)
        avg_fitness_values.append(avg_fitness)
        # Select the parents for crossover
        parents = population[np.random.choice(population_size, size=population_size-1, replace=True, p=fitness_values/fitness_values.sum())]
        # Perform crossover
        children = []
        for i in range(0, population_size - 1, 2):
            if np.random.rand() < crossover_probability:
                crossover_point = np.random.randint(1, 9)
                child1 = np.concatenate((parents[i, :crossover_point, :], parents[i + 1, crossover_point:, :]), axis=0)
                child2 = np.concatenate((parents[i + 1, :crossover_point, :], parents[i, crossover_point:, :]), axis=0)
            else:
                child1 = parents[i]
                child2 = parents[i + 1]
            children.append(child1)
            children.append(child2)
        children = np.array(children)
        # Perform mutation
        for i in range(population_size - 1):
            if np.random.rand() < mutation_probability:
                mutation_point = np.random.randint(10)
                children[i, mutation_point, :] = np.random.randint(10, size=2)
        # Replace the least fit individual with the most fit individual from the previous generation
        population[np.argmin(fitness_values)] = population[np.argmax(fitness_values)]
        # Replace the population with the children
        population[:population_size - 1, :, :] = children

    return best_fitness_values, avg_fitness_values

best_fitness_values, avg_fitness_values = genetic_algorithm(5, 10, 0.2, 0.1)
plt.plot(best_fitness_values, label='Best Fitness')
plt.plot(avg_fitness_values, label='Average Fitness')
plt.legend()
plt.title('Fitness vs Avg Fitness')
plt.xlabel('Generation')
plt.ylabel('Fitness Value')
plt.show()


