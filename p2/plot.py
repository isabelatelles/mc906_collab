import matplotlib.pyplot as plt


def plot(worst_scores, avg_scores, best_scores, max_generation):
    plt.plot(range(max_generation), best_scores, "g-", label = "Best")
    plt.plot(range(max_generation), avg_scores, "b-", label = "Average")
    plt.plot(range(max_generation), worst_scores, "r-", label = "Worst")
    plt.ylabel("Scores")
    plt.xlabel("Generation")
    plt.legend(loc='upper left')
    plt.savefig('graph.png')
