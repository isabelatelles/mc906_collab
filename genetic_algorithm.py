from modeling import *
from random import shuffle


def create_individual(problem):
    individual = list(range(problem.n_gift_types))

    for i in range(problem.n_gift_quantity - 1):
        individual += list(range(problem.n_gift_types))

    shuffle(individual)
    individual = problem.set_triplets_and_twins(individual)

    return individual


def create_starting_population(size):
    starting_population = list()

    for i in range(size):
        starting_population.append(create_individual(p))

    return starting_population


p = SantaProblem(200, 40)

population_size = 50
starting_population = create_starting_population(population_size)
