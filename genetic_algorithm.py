from modeling import *
from random import shuffle, randint, sample, random


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


def calculate_fitness(problem, individual):
    return avg_normalized_happiness(problem, individual)


def selection_by_tournament(problem, population):
    tournament_dimension = randint(2, len(population))
    individuals = sample(population, tournament_dimension)
    scores = [calculate_fitness(problem, individual) for individual in individuals]
    index_selected_individual = scores.index(max(scores))
    selected_individual = individuals[index_selected_individual]

    return selected_individual


if __name__ == '__main__':
    santa_problem = SantaProblem(200, 40)

    population_size = 50
    max_generation = 100
    mutation_rate = 0.02

    best_scores = list()

    population = create_starting_population(santa_problem, population_size)

    for generation in range(max_generation):
        scores = [calculate_fitness(santa_problem, individual) for individual in population]
        best_score = max(scores)
        best_scores.append(best_score)
        print('Generation: ' + str(generation) + ', Best score: ' + str(best_score))

        new_population = [population[scores.index(best_score)]]
        for i in range(population_size - 1):
            parent_1 = selection_by_tournament(santa_problem, population)
            parent_2 = selection_by_tournament(santa_problem, population)
            child = santa_problem.crossover(parent_1, parent_2)
            if random() < mutation_rate:
                child = santa_problem.mutation(child)
            new_population.append(child)
        population = new_population

    print('Final best score: ' + str(max(best_scores) + ', Generation: ' + str(best_scores.index(max(best_scores)))))
