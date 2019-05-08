import math
from random import randint, choice
from fitness_function import avg_normalized_happiness
from collections import Counter


class SantaProblem:
    def __init__(self, n_children, n_gift_types):
        self.n_children = n_children  # n children to give
        self.n_gift_types = n_gift_types  # n types of gifts available
        self.n_gift_quantity = int(n_children/n_gift_types)  # each type of gifts are limited to this quantity
        self.n_gift_pref = int(0.2 * n_gift_types)  # number of gifts a child ranks
        self.n_child_pref = int(0.1 * n_children)  # number of children a gift ranks
        self.n_triplets = math.ceil(0.015 * n_children / 3.) * 3  # 1.5% of all population, rounded to the closest number
        self.n_twins = math.ceil(0.04 * n_children / 2.) * 2  # 4% of all population, rounded to the closest number

    def __repr__(self):
        return "Santa Gifting Problem: {} types of gifts for {} children".format(self.n_gift_types, self.n_children)

    def set_triplets_and_twins(self, individual):
        # Set triplets' gifts
        for t in range(0, self.n_triplets, 3):
            gift_counts = dict()
            for index, value in enumerate(individual[t:]):
                if value not in gift_counts:
                    gift_counts[value] = 3
                    break
                elif self.n_gift_quantity - gift_counts[value] >= 3:
                    gift_counts[value] += 3
                    break

            index += t
            if individual[t] != value:
                index = individual[index + 1:].index(value) + index + 1
                individual[index], individual[t] = individual[t], value
            if individual[t + 1] != value:
                index = individual[index + 1:].index(value) + index + 1
                individual[index], individual[t + 1] = individual[t + 1], value
            else:
                index += 1
            if individual[t + 2] != value:
                index = individual[index + 1:].index(value) + index + 1
                individual[index], individual[t + 2] = individual[t + 2], value

        # Set twins' gifts
        for t in range(self.n_triplets, self.n_triplets + self.n_twins, 2):
            for index, value in enumerate(individual[t:]):
                if value not in gift_counts:
                    gift_counts[value] = 2
                    break
                elif self.n_gift_quantity - gift_counts[value] >= 2:
                    gift_counts[value] += 2
                    break

            index += t
            if individual[t] != value:
                index = individual[index + 1:].index(value) + index + 1
                individual[index], individual[t] = individual[t], value
            if individual[t + 1] != value:
                index = individual[index + 1:].index(value) + index + 1
                individual[index], individual[t + 1] = individual[t + 1], value

        return individual

    def check_triplets(self, individual):
        for t1 in range(0, self.n_triplets, 3):
            triplet1 = individual[t1]
            triplet2 = individual[t1 + 1]
            triplet3 = individual[t1 + 2]
            if triplet1 != triplet2 or triplet2 != triplet3:
                return False

        return True

    def check_twins(self, individual):
        for t1 in range(self.n_triplets, self.n_triplets + self.n_twins, 2):
            twin1 = individual[t1]
            twin2 = individual[t1 + 1]
            if twin1 != twin2:
                return False

        return True

    def crossover(self, individual_1, individual_2):
        return individual_1

    def mutation(self, individual):
        first = True
        while first or self.check_triplets(individual) is False or self.check_twins(individual) is False:
            i = randint(0, self.n_children)
            j = choice(list(range(0, i)) + list(range(i + 1, self.n_children)))
            individual[i], individual[j] = individual[j], individual[i]
            first = False

        return individual

    def fitness_function(self, individual):
        return avg_normalized_happiness(self, individual)
