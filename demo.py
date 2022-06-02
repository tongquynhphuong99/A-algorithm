# d = {320: 1, 321: 0, 322: 3}
# print(min(d, key=d.get))
# import heapq as heap
# open_list = [(1, 653465), (7, 5765765), (3, 122332252353), (4, 36475868)]
# heap.heapify(open_list)
# print(open_list)
import operator
import heapq as heap
import xmltodict
from haversine import haversine
import time
import numpy as np
from sklearn.neighbors import KDTree

# close_list={4545:34, 3453246:46, 35235:56}
# d = {320: 1, 321: 0, 322: 3}
# d[675]=9

# s = sorted(d.items(), key=operator.itemgetter(1), reverse=False)
# sorted_dict = {k:v for k, v in s}
# print(sorted_dict)
# print(type(sorted_dict))
# a=list(sorted_dict.keys())[0]
# print(a)
# print(sorted_dict)

# myList.append((4545,34))
# print(myList)
# del close_list[35235]
# print(close_list)
# print(myList)
# myList.remove(myList[0])
# print(myList)
d={12:{'parent':2143, 'cost':243}}
d[24] = {"parent":51655, "cost": 0}
print(d[24]['cost'])
a=(2413,586)
print(a[0])

