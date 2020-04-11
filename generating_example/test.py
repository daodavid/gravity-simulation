import numpy as np

x = np.array([0.1, 2, 3])
x[x < 3] = 0.01


a = np.array([[5, 1, 3],
              [1, 1, 1],
              [1, 2, 1]])

b = np.array([1, 2, 3])
b= b.reshape(-1,1)

c = a*b




from random import *

v = uniform(0,0.1)
print(v)