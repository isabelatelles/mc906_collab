# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load in

import numpy as np  # linear algebra
import pandas as pd  # data processing, CSV file I/O (e.g. pd.read_csv)
import math
from collections import Counter


def lcm(a, b):
    """Compute the lowest common multiple of a and b"""
    # in case of large numbers, using floor division
    return a * b // math.gcd(a, b)


def avg_normalized_happiness(problem, individual):
    ratio_gift_happiness = 2
    ratio_child_happiness = 2

    gift_pref = pd.read_csv('dataset/created_child_wishlist_' + str(problem.n_children) + '_' +
                            str(problem.n_gift_types) + '.csv', header=None).values
    child_pref = pd.read_csv('dataset/created_gift_goodkids_' + str(problem.n_children) + '_' +
                             str(problem.n_gift_types) + '.csv', header=None).values

    # check if number of each gift exceeds problem.n_gift_per_type
    gift_counts = Counter(elem for elem in individual)
    for count in gift_counts.values():
        assert count <= problem.n_gift_per_type

    # check if triplets have the same gift
    for t1 in np.arange(0, problem.n_triplets, 3):
        triplet1 = individual[t1]
        triplet2 = individual[t1 + 1]
        triplet3 = individual[t1 + 2]
        # print(t1, triplet1, triplet2, triplet3)
        assert triplet1 == triplet2 and triplet2 == triplet3

    # check if twins have the same gift
    for t1 in np.arange(problem.n_triplets, problem.n_triplets + problem.n_twins, 2):
        twin1 = individual[t1]
        twin2 = individual[t1 + 1]
        # print(t1)
        assert twin1 == twin2

    max_child_happiness = problem.n_gift_pref * ratio_child_happiness
    max_gift_happiness = problem.n_child_pref * ratio_gift_happiness
    total_child_happiness = 0
    total_gift_happiness = np.zeros(problem.n_gift_types)

    for child_id, gift_id in enumerate(individual):
        # check if child_id and gift_id exist
        assert child_id < problem.n_children
        assert gift_id < problem.n_gift_types
        assert child_id >= 0
        assert gift_id >= 0

        child_happiness = -1
        if np.any(np.where(gift_pref[child_id] == gift_id)):
            child_happiness = (problem.n_gift_pref - np.where(gift_pref[child_id] == gift_id)[0][0])\
                              * ratio_child_happiness

        gift_happiness = -1
        if np.any(np.where(child_pref[gift_id] == child_id)):
            gift_happiness = (problem.n_child_pref - np.where(child_pref[gift_id] == child_id)[0][0])\
                             * ratio_gift_happiness


        total_child_happiness += child_happiness
        total_gift_happiness[gift_id] += gift_happiness

    # print('normalized child happiness=',
    #       float(total_child_happiness) / (float(problem.n_children) * float(max_child_happiness)),
    #       ', normalized gift happiness',
    #       np.mean(total_gift_happiness) / float(max_gift_happiness * problem.n_gift_per_type))

    # to avoid float rounding error
    # find common denominator
    # NOTE: I used this code to experiment different parameters, so it was necessary to get the multiplier
    # Note: You should hard-code the multipler to speed up, now that the parameters are finalized
    denominator1 = problem.n_children * max_child_happiness
    denominator2 = problem.n_gift_per_type * max_gift_happiness * problem.n_gift_types
    common_denom = lcm(denominator1, denominator2)
    multiplier = common_denom / denominator1

    # # usually denom1 > demon2
    return float(math.pow(total_child_happiness * multiplier, 3) + math.pow(np.sum(total_gift_happiness), 3)) / float(
        math.pow(common_denom, 3))
    # return math.pow(float(total_child_happiness)/(float(n_children)*float(max_child_happiness)),2) + math.pow(np.mean(total_gift_happiness) / float(max_gift_happiness*problem.n_gift_per_type),2)
