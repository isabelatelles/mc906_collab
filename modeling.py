import math

class SantaProblem():
    def __init__(self, n_children, n_gift_types):
        self.n_children = n_children
        self.n_gift_types = n_gift_types
        self.n_triplets = math.ceil(0.015 * n_children / 3.) * 3
        self.n_twins = math.ceil(0.04 * n_children / 2.) * 2
        self.n_gifts = int(n_children/n_gift_types)

    def __repr__(self):
        return "Santa Gifting Problem: {} types of presents for {} children".format(self.n_gift_types, self.n_children)

    def crossover(individual_1, individual_2):
        return individual_1

    def mutation(individual):
        return individual

    def fitness_function(individual):
        return 1
