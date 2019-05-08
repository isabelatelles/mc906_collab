from modeling import *
from random import shuffle, randint, sample


def create_individual(problem):
    individual = list(range(problem.n_gift_types))

    for i in range(problem.n_gift_per_type - 1):
        individual += list(range(problem.n_gift_types))

    shuffle(individual)
    individual = problem.set_triplets_and_twins(individual)

    return individual


def create_starting_population(problem, size):
    starting_population = list()

    for i in range(size):
        starting_population.append(create_individual(problem))

    return starting_population


def selection_by_tournament(problem, population):
    tournament_dimension = randint(0, len(population))
    individuals = sample(population, tournament_dimension)
    scores = [problem.calculate_fitness(individual) for individual in individuals]
    index_selected_individual = scores.index(max(scores))
    selected_individual = individuals[index_selected_individual]

    return selected_individual


p = SantaProblem(200, 40)

population_size = 50
starting_population = create_starting_population(p, population_size)