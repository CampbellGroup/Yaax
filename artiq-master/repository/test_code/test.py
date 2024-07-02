
import numpy as np

h = np.array([1,2,3])
hempt = np.full((10 - h.size), np.nan)

holder = np.concatenate((h,hempt), axis =0 )

print(holder)

"""
a = np.array([1, 2])
b = np.array([5, 6])


print(np.concatenate((a, b), axis=0))
"""