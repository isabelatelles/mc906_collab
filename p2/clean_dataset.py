import pandas as pd
import random


def clean_child_wishlist(dataframe, columns, limit):
    new_dataframe = pd.DataFrame()

    index = 0
    for row in dataframe.itertuples(index=False):
        elements_list = list()
        for element in row:
            if len(elements_list) == columns:
                break
            if element < limit:
                elements_list.append(int(element))
        if len(elements_list) != columns:
            elements_list += random.sample(range(limit), columns - len(elements_list))
        new_dataframe = new_dataframe.append(pd.DataFrame([elements_list], index=[index]))
        index += 1

    return new_dataframe


if __name__ == "__main__":
    # 200, 40, 5
    n_children = 300
    n_gift_types = 100
    n_gift_unities = 3

    # 0.1
    wishlist_size = int(0.05*n_gift_types)

    child_wishlist = pd.read_csv('original_dataset/child_wishlist_v2.csv', sep=',', nrows=n_children, index_col=0, header=None)
    gift_goodkids = pd.read_csv('original_dataset/gift_goodkids_v2.csv', sep=',', nrows=n_gift_types, index_col=0, header=None)

    child_wishlist = clean_child_wishlist(child_wishlist, wishlist_size, n_gift_types)
