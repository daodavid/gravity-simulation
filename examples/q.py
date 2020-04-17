import numba, numpy as np

# Define the row-wise function to be vectorized:


def f(a,b):
    b = a.sum() 

# Apply the function to an array with five rows:
a = np.arange(10).reshape(5,2)
b = f(a)   
print(b)


@vectorize(signature='(m),(m,n),(),(m)->(m)' )
def inner3(a,b,m,M):
    c = a+b
    d = np.sum(c,axis=1)
    return d

m = np.array(['1','1'])
M = m
y = x =np.array([[11, 12],
                  [21, 22]])
res = inner3(x,y,m,M)