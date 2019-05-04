from pandas import DataFrame
from numpy import arange, random

n_children = 200
n_triplets = int(0.015 * n_children)
n_twins = int(0.04 * n_children)

n_gift_types = 40
n_gift_unities = 3

wishlist_size = int(0.2 * n_gift_types)
goodkids_size = int(0.1 * n_children)

child_wishlist = random.randint(low=0, high=n_gift_types, size=(n_children, wishlist_size))
df_child_whishlist = DataFrame(data=child_wishlist, index=arange(n_children))
df_child_whishlist.to_csv(index=False, header=False, path_or_buf="created_child_whishlist_"
                            + str(n_children) + "_" + str(n_gift_types) + ".csv")

gift_goodkids = random.randint(low=0, high=n_children, size=(n_gift_types, goodkids_size))
df_gift_goodkids = DataFrame(data=gift_goodkids, index=arange(n_gift_types))
df_gift_goodkids.to_csv(index=False, header=False, path_or_buf="created_gift_goodkids_"
                            + str(n_children) + "_" + str(n_gift_types) + ".csv")
