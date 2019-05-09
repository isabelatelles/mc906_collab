import matplotlib.pyplot as plt

def plot(worst_scores, avg_scores, best_scores, max_generation):
    plt.plot(range(max_generation), worst_scores, "r-", range(max_generation),
                avg_scores, "b-", range(max_generation), best_scores, "g-")
    plt.ylabel("Scores")
    plt.xlabel("Generation")
    plt.show()
