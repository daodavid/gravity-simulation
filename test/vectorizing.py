import numpy as np
from datetime import datetime 

n =2
y = np.linspace(0,n,n)

def my_funct(X,z):
    z  = np.array(z)
    a = np.array([1])
    for i in z :
        print(i)
    return str(z)


start_time = datetime.now() 
k = np.array([])
for i in y :
   h = my_funct(i,y)
   k = np.append(k,h)

print(k)
time_elapsed = datetime.now() - start_time 
time_elapsed = time_elapsed.total_seconds() * 1000
print('Time elapsed vectorized (hh:mm:ss.ms) {}'.format(time_elapsed))



"""
vectorized
"""
start_time = datetime.now() 
v = np.vectorize(my_funct, excluded=['z']) 
z =v(X=y,z=[9,2])
print(z)
time_elapsed = datetime.now() - start_time 
time_elapsed = time_elapsed.total_seconds() * 1000
print('Time elapsed vectorized (hh:mm:ss.ms) {}'.format(time_elapsed))







def mypolyval(p, x):
    _p = list(p)
    res = _p.pop(0)
    while _p:
        res = res*x + _p.pop(0)
    return res
vpolyval = np.vectorize(mypolyval, excluded=['p'])
a = vpolyval(p=[1, 2, 3], x=[0, 1])
#print(a)