
import numba, numpy as np
from numba import guvectorize
from numba import vectorize
from numba import  float64,int64,f8
#from numbapro import guvectorize

@vectorize(["float64(float64, float64)"], nopython=False)
def F(a,b):
     return (a+b)*5
    #d = np.sum(c,axis=1)
    #return d

x = y = np.array([[11, 12],
                   [21, 22]])

M = [1,2]

res = F(x,y)   
print(res)