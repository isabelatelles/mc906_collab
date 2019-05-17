from modeling import *
from plot import *
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
    return problem.fitness_function.avg_normalized_happiness(individual)


def selection_by_tournament(population, scores):
    tournament_dimension = randint(2, len(population))
    index_individuals = sample(list(range(len(scores))), tournament_dimension)
    scores_individuals = [scores[index] for index in index_individuals]
    index_selected_individual = index_individuals[scores_individuals.index(max(scores_individuals))]
    selected_individual = population[index_selected_individual]

    return selected_individual


if __name__ == '__main__':
    santa_problem = SantaProblem(200, 40)

    population_size = 70
    max_generation = 1000
    mutation_rate = 0.65

    best_scores = list()
    avg_scores = list()
    worst_scores = list()

    best_individuals = list()

    population = create_starting_population(santa_problem, population_size)

    for generation in range(max_generation):
        scores = [calculate_fitness(santa_problem, individual) for individual in population]
        best_score = max(scores)
        best_individuals.append(population[scores.index(best_score)])
        best_scores.append(best_score)
        avg_scores.append(sum(scores)/len(scores))
        worst_scores.append(min(scores))
        with open("output.txt", "a") as f:
            print('Generation: ' + str(generation) + ', Best score: ' + str(best_score), file=f)

        new_population = [population[scores.index(best_score)]]
        for i in range(population_size//2 - 1):
            parent_1 = selection_by_tournament(population, scores)
            parent_2 = selection_by_tournament(population, scores)
            child_1 = santa_problem.crossover(parent_1, parent_2)
            child_2 = santa_problem.crossover(parent_2, parent_1)
            if random() < mutation_rate:
                child_1 = santa_problem.mutation(child_1)
            new_population.append(child_1)
            if random() < mutation_rate:
                child_2 = santa_problem.mutation(child_2)
            new_population.append(child_2)
        population = new_population

    with open("output.txt", "a") as f:
        print('Final best score: ' + str(max(best_scores)) + ', Generation: ' +
              str(best_scores.index(max(best_scores))), file=f)

    with open("best_ind.txt", "w") as f:
        f.write(str(best_individuals[best_scores.index(max(best_scores))]))
    plot(worst_scores, avg_scores, best_scores, max_generation)
