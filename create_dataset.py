from pandas import DataFrame
from numpy import arange, random
import math

n_children = 200
triplets = math.ceil(0.015 * n_children / 3.) * 3
twins = math.ceil(0.04 * n_children / 2.) * 2

n_gift_type = 40

n_gift_pref = int(0.2 * n_gift_type)
n_child_pref = int(0.1 * n_children)

child_wishlist = random.randint(low=0, high=n_gift_type, size=(n_children, n_gift_pref))
df_child_wishlist = DataFrame(data=child_wishlist, index=arange(n_children))
df_child_wishlist.to_csv(index=False, header=False, path_or_buf="created_child_wishlist_"
                            + str(n_children) + "_" + str(n_gift_type) + ".csv")

gift_goodkids = random.randint(low=0, high=n_children, size=(n_gift_type, n_child_pref))
df_gift_goodkids = DataFrame(data=gift_goodkids, index=arange(n_gift_type))
df_gift_goodkids.to_csv(index=False, header=False, path_or_buf="created_gift_goodkids_"
                            + str(n_children) + "_" + str(n_gift_type) + ".csv")
