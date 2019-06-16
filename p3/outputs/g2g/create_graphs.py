import glob
import re
import pandas as pd
import numpy as np
from statistics import mean
import matplotlib.pyplot as plt

vel_rx_dict = {
'centroid':
  re.compile(r'.*velocities_(?P<initial>.*[^_])_(?P<goal>.*[^_])_centroid.csv'),
'bisector':
  re.compile(r'.*velocities_(?P<initial>.*[^_])_(?P<goal>.*[^_])_bisector.csv'),
'mom': re.compile(r'.*velocities_(?P<initial>.*[^_])_(?P<goal>.*[^_])_mom.csv'),
'som': re.compile(r'.*velocities_(?P<initial>.*[^_])_(?P<goal>.*[^_])_som.csv'),
'lom': re.compile(r'.*velocities_(?P<initial>.*[^_])_(?P<goal>.*[^_])_lom.csv')
}

pos_rx_dict = {
'centroid':
   re.compile(r'.*positions_(?P<initial>.*[^_])_(?P<goal>.*[^_])_centroid.csv'),
'bisector':
   re.compile(r'.*positions_(?P<initial>.*[^_])_(?P<goal>.*[^_])_bisector.csv'),
'mom': re.compile(r'.*positions_(?P<initial>.*[^_])_(?P<goal>.*[^_])_mom.csv'),
'som': re.compile(r'.*positions_(?P<initial>.*[^_])_(?P<goal>.*[^_])_som.csv'),
'lom': re.compile(r'.*positions_(?P<initial>.*[^_])_(?P<goal>.*[^_])_lom.csv')
}

def _parse_line(line, rx_dict):
    """
    Do a regex search against all defined regexes and
    return the key and match result of the first matching regex

    """

    for key, rx in rx_dict.items():
        matches = rx.findall(line)
        if matches:
            return key, matches
    # if there are no matches
    return None, None

def _get_csvs(csv_filenames, rx_dict):
    for csv in csv_filenames:
        key, matches = _parse_line(csv, rx_dict)
        if key == 'centroid':
            centroid = pd.read_csv(csv, header=None)
        elif key == 'bisector':
            bisector = pd.read_csv(csv, header=None)
        elif key == 'mom':
            mom = pd.read_csv(csv, header=None)
        elif key == 'som':
            som = pd.read_csv(csv, header=None)
        elif key == 'lom':
            lom = pd.read_csv(csv, header=None)

    return centroid, bisector, mom, som, lom

def _get_exp_id(csv_filenames, rx_dict):
    key, matches = _parse_line(csv_filenames[0], rx_dict)

    return matches[0][0], matches[0][1]

def _calc_dist_to_goal(csv, goal):
    x, y = re.findall("-*\d+\.*-*\d*", goal)
    x = float(x)
    y = float(y)
    distances = []
    for line in csv.values:
        distance = ((x - line[0])**2 + (y - line[1])**2)**(1/2)
        distances.append(distance)

    return distances

def plot_distance_graph(filename, initial, goal, c, b, m, s, l):
    plt.plot(range(len(c)), c, label = "centroid")
    plt.plot(range(len(b)), b, label = "bisector")
    plt.plot(range(len(m)), m, label = "mom")
    plt.plot(range(len(s)), s, label = "som")
    plt.plot(range(len(l)), l, label = "lom")
    plt.ylabel("Distance to goal")
    plt.xlabel("Iteration")
    plt.legend(loc='upper right')
    plt.suptitle("Distance to the goal by iteration - Initial: {} - Goal: {}"\
                                                        .format(initial, goal))
    plt.savefig(filename + '.png')
    plt.show()

def plot_velocities_graph(filename, initial, goal, c, b, m, s, l):
    plt.scatter(c[:][0], c[:][1], c="g", label = "centroid")
    plt.scatter(b[:][0], b[:][1], c="r", label = "bisector")
    plt.scatter(m[:][0], m[:][1], c="b", label = "mom")
    plt.scatter(s[:][0], s[:][1], c="y", label = "som")
    plt.scatter(l[:][0], l[:][1], c="m", label = "lom")
    plt.legend(loc='upper right')
    plt.suptitle("Path to the goal - Initial: {} - Goal: {}"\
                                                        .format(initial, goal))
    plt.savefig(filename + '.png')
    plt.show()

def plot_velocities_graph(filename, initial, goal, positive, negative):
    ind = np.arange(len(positive))  # the x locations for the groups
    width = 0.35  # the width of the bars

    fig, ax = plt.subplots()
    rects1 = ax.bar(ind - width/2, positive, width, color='r', label='Positive')
    rects2 = ax.bar(ind + width/2, negative, width, color='b', label='Negative')

    # Add some text for labels, title and custom x-axis tick labels, etc.
    ax.set_ylabel('Velocities')
    ax.set_title('Velocities mean by defuzzification method')
    ax.set_xticks(ind)
    ax.set_xticklabels(('centroid', 'bisector', 'mom', 'som', 'lom'))
    ax.legend(loc='upper left')

    def autolabel(rects, xpos='center'):
        """
        Attach a text label above each bar in *rects*, displaying its height.

        *xpos* indicates which side to place the text w.r.t. the center of
        the bar. It can be one of the following {'center', 'right', 'left'}.
        """

        ha = {'center': 'center', 'right': 'left', 'left': 'right'}
        offset = {'center': 0, 'right': 1, 'left': -1}

        for rect in rects:
            height = rect.get_height()
            ax.annotate('{0:.2f}'.format(height),
                        xy=(rect.get_x() + rect.get_width() / 2, height),
                        xytext=(offset[xpos]*2, 2),  # use 3 points offset
                        textcoords="offset points",  # in both directions
                        ha=ha[xpos], va='bottom')

    autolabel(rects1, "left")
    autolabel(rects2, "right")

    fig.tight_layout()

    plt.savefig(filename + '.png')
    plt.show()

def create_position_graphs(experiment):
    positions_csv_filenames = glob.glob(experiment + "/positions*")
    initial, goal = _get_exp_id(positions_csv_filenames, pos_rx_dict)
    centroid, bisector, mom, som, lom = _get_csvs(positions_csv_filenames,
                                                                    pos_rx_dict)

    c_distances = _calc_dist_to_goal(centroid, goal)
    b_distances = _calc_dist_to_goal(bisector, goal)
    m_distances = _calc_dist_to_goal(mom, goal)
    s_distances = _calc_dist_to_goal(som, goal)
    l_distances = _calc_dist_to_goal(lom, goal)

    plot_distance_graph(experiment + "/distance_to_goal", initial, goal,
            c_distances, b_distances, m_distances, s_distances, l_distances)

def _get_velocities_mean(csv):
    negative = []
    positive = []
    for l in csv.values:
        for v in l:
            if v > 0:
                positive.append(v)
            else:
                negative.append(v)

    return abs(mean(negative)), mean(positive)

def create_velocity_graphs(experiment):
    velocities_csv_filenames = glob.glob(experiment + "/velocities*")
    initial, goal = _get_exp_id(velocities_csv_filenames, vel_rx_dict)
    csvs = _get_csvs(velocities_csv_filenames, vel_rx_dict)
    negative = []
    positive = []
    for csv in csvs:
        n, p = _get_velocities_mean(csv)
        negative.append(n)
        positive.append(p)
    plot_velocities_graph(experiment + "/velocities_mean", initial, goal,
                                                            positive, negative)

def main():
    experiments = glob.glob("exp*")
    for experiment in experiments:
        create_position_graphs(experiment)
        create_velocity_graphs(experiment)

if __name__ == '__main__':
    main()
