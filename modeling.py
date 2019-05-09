import math
from random import randint, choice, shuffle
from collections import Counter


class SantaProblem:
    def __init__(self, n_children, n_gift_types):
        self.n_children = n_children  # n children to give
        self.n_gift_types = n_gift_types  # n types of gifts available
        self.n_gift_per_type = int(n_children/n_gift_types)  # each type of gifts are limited to this quantity
        self.n_gift_pref = int(0.2 * n_gift_types)  # number of gifts a child ranks
        self.n_child_pref = int(0.1 * n_children)  # number of children a gift ranks
        self.n_triplets = math.ceil(0.015 * n_children / 3.) * 3  # 1.5% of all population, rounded to the closest number
        self.n_twins = math.ceil(0.04 * n_children / 2.) * 2  # 4% of all population, rounded to the closest number

    def __repr__(self):
        return "Santa Gifting Problem: {} types of gifts for {} children".format(self.n_gift_types, self.n_children)

    def set_triplets_and_twins(self, individual):
        # Set triplets' gifts
        for t in range(0, self.n_triplets, 3):
            # Count the number of gifts already used by now
            gift_counts = dict()

            # Find a type of gift available to give to the triplets
            for index, value in enumerate(individual[t:]):
                if value not in gift_counts:
                    gift_counts[value] = 3
                    break
                elif self.n_gift_per_type - gift_counts[value] >= 3:
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
            # Find a type of gift available to give to the twins
            for index, value in enumerate(individual[t:]):
                if value not in gift_counts:
                    gift_counts[value] = 2
                    break
                elif self.n_gift_per_type - gift_counts[value] >= 2:
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
        # Set the single point index to make the crossover
        single_point_index = self.n_children//2

        # Copy the first part of the individual 1
        new_individual = individual_1[:single_point_index].copy()

        # Count the remaining gifts to be distributed
        counter = [0] * self.n_gift_types
        for c in individual_1[single_point_index:]:
            counter[c] = counter[c] + 1

        # Copy as many gifts from the 2nd part of individual 2 as possible
        empty_index = []
        for i in range(single_point_index, self.n_children):
            if counter[individual_2[i]] > 0:
                new_individual.append(individual_2[i])
                counter[individual_2[i]] = counter[individual_2[i]] - 1
            else:
                new_individual.append(None)
                empty_index.append(i)

        empty_index.reverse()

        # Fill the empty index with available gifts
        for c in individual_1[single_point_index:]:
            if counter[c] > 0:
                new_individual[empty_index.pop()] = c
                counter[c] = counter[c] - 1

        return new_individual

    def mutation(self, individual):
        i = randint(0, self.n_children - 1)

        not_only_child = None
        # Select any index if i is not a triplet/twin, otherwise select an index out of the range of the triplets/twins
        if i >= self.n_triplets + self.n_twins:
            j = choice(list(range(0, i)) + list(range(i + 1, self.n_children)))
            # j = choice(list(range(self.n_triplets + self.n_twins, self.n_children)))
            if j < self.n_triplets + self.n_twins:
                not_only_child = j
            else:
                # Swap gifts between children since they are not twins or triplets
                individual[i], individual[j] = individual[j], individual[i]
        else:
            not_only_child = i

        if not_only_child:
            # Find the gifts that are available to swap
            gift_counts = Counter(elem for elem in individual[self.n_triplets + self.n_twins:]).most_common()
            available_gifts = [count[0] for count in gift_counts if (not_only_child < self.n_triplets and count[1] > 2)
                              or (not_only_child < self.n_triplets + self.n_twins and count[1] > 1)]

            # Find the indexes of each child that currently receives each available gift
            children_of_gifts = dict()
            for gift in available_gifts:
                children_of_gifts[gift] = [index + self.n_triplets + self.n_twins for index, value in
                                           enumerate(individual[self.n_triplets + self.n_twins:]) if value == gift]

            # Choose a gift randomly and then the available children to swap its gifts
            gift_chosen = choice(available_gifts)
            available_children = children_of_gifts[gift_chosen]
            shuffle(available_children)

            if not_only_child < self.n_triplets:
                if not_only_child % 3 == 0:
                    min_index = not_only_child
                    max_index = not_only_child + 3
                elif not_only_child - 1 % 3 == 0:
                    min_index = not_only_child - 1
                    max_index = not_only_child + 2
                else:
                    min_index = not_only_child - 2
                    max_index = not_only_child + 1
            elif not_only_child < self.n_triplets + self.n_twins:
                if (not_only_child - self.n_triplets) % 2 == 0:
                    min_index = not_only_child
                    max_index = not_only_child + 2
                else:
                    min_index = not_only_child - 1
                    max_index = not_only_child + 1

            # Swap triplets/twins gifts with the gift of the available children
            k = 0
            for index in range(min_index, max_index):
                individual[index], individual[available_children[k]] = individual[available_children[k]],\
                                                                       individual[index]
                k += 1

        return individual
