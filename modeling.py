import math
from fitness_function import avg_normalized_happiness

class SantaProblem():
    def __init__(self, n_children, n_gift_types):
        self.n_children = n_children  # n children to give
        self.n_gift_types = n_gift_types  # n types of gifts available
        self.n_gift_quantity = int(n_children/n_gift_types)  # each type of gifts are limited to this quantity
        self.n_gift_pref = int(0.2 * n_gift_types)  # number of gifts a child ranks
        self.n_child_pref = int(0.1 * n_children)  # number of children a gift ranks
        self.n_triplets = math.ceil(0.015 * n_children / 3.) * 3  # 4% of all population, rounded to the closest number
        self.n_twins = math.ceil(0.04 * n_children / 2.) * 2  # 1.5% of all population, rounded to the closest number

    def __repr__(self):
        return "Santa Gifting Problem: {} types of presents for {} children".format(self.n_gift_types, self.n_children)

    def crossover(self, individual_1, individual_2):
        return individual_1

    def mutation(self, individual):
        return individual

    def fitness_function(self, individual):
        return avg_normalized_happiness(self, individual)
