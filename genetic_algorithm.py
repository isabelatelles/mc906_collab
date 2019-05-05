from modeling import *
import numpy as np

def create_individual(problem):
    individual = np.array(range(problem.n_gift_types))
    for i in range(problem.n_gifts - 1):
        individual = np.append(individual, range(problem.n_gift_types))
    np.random.shuffle(individual)
    return individual
