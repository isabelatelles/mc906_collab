import matplotlib.pyplot as plt
import pandas as pd


def main():
    diff_gauss_df = pd.read_csv('exp1/velocities_diff_gauss.csv', names=['vel_left', 'vel_right'], header=None, )
    diff_gauss_df = diff_gauss_df[:410]
    diff_gauss_df.index.name = 'Iterations'

    diff_tri_df = pd.read_csv('exp1/velocities_diff_tri.csv', names=['vel_left', 'vel_right'], header=None)
    diff_tri_df = diff_tri_df[:410]
    diff_tri_df.index.name = 'Iterations'

    fig, (ax, ax2) = plt.subplots(ncols=2)

    diff_tri_df.plot(y=['vel_left', 'vel_right'], ax=ax, use_index=True)
    diff_gauss_df.plot(y=['vel_left', 'vel_right'], ax=ax2, ls="--", use_index=True)

    plt.show()


if __name__ == '__main__':
    main()
