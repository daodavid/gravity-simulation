import numpy as np
from numba import guvectorize

# from datetime import datetime
# # for i in range(10000,10020) :
# #     start = datetime.now()
# #     a = np.full((i+10000, i+10000), 100)
# #     #print(a.shape)
# #     np.sum(a)
# #     print(datetime.now()-start)

# # @guvectorize([(int64[:], int64, int64[:])], '(n),()->(n)')


# def add(a, b):
#     d = a - b
#     return d




# x = y = np.array([[11, 12],
#                   [21, 22]])

                

# # k = np.vectorize(sum, signature='()->(n)', excluded=['b'])
# k = np.vectorize(add, signature='(),()->()', excluded=['b'])
   
# res = k(x,y)
# print(res)


# # = k(a=x,b=y)
# #print(res)

# def inner1d(a , b  ):  #signature = (i),(i)->()
#   c = a+b
#   return c


# #k = np.vectorize(inner1d, signature='(),()->()', excluded=['b'])
# #res = k(x,y)

# x = y = np.array([1,2])  
# y = x =np.array([[11, 12],
#                   [21, 22]])


# #k = np.vectorize(inner1d, signature='(i),(i)->(i)')  #excluded=['b']
# #res = k(x,y)
# #print(res)

# def inner(a,b):
#   c = a*b
#   return c

# k = np.vectorize(inner, signature='(m,n),(n,p)->(m,p)')  #excluded=['b']
# #k = np.vectorize(inner, signature='(i),(i)->(i)')  #excluded=['b']
# res = k(x,y)
# #print(res)


# def inner2(a,b):
#   c = a+b
#   return c

# k = np.vectorize(inner2, signature='(m,n),(m,n)->(m,p)')  #excluded=['b']
# #k = np.vectorize(inner, signature='(i),(i)->(i)')  #excluded=['b']
# res = k(x,y)
# #print(res)

# def inner3(a,b):
#   c = a+b
#   return c

# k = np.vectorize(inner3, signature='(m),(m,n)->(m,n)')  #importen
# #k = np.vectorize(inner, signature='(i),(i)->(i)')  #excluded=['b']
# #res = k(x,y)
# #print(res)


# k = np.vectorize(inner3, signature='(m),(m,n)->(m,n)')
# '''
# https://docs.scipy.org/doc/numpy-1.13.0/reference/c-api.generalized-ufuncs.html

# '''
# res = k(x,y)
# print(res)


# def inner3(a,b):
#     c = a+b
#     d = np.sum(c,axis=1)
#     return d


# k = np.vectorize(inner3, signature='(m),(m,n)->(m)')
# res = k(x,y)
# #print(res)



# k = np.vectorize(inner3, signature='(m),(m,n),(),(m)->(m)')
# res = k(x,y,m,M)

# #@np.vectorize(signature='(m),(m,n),(),(m)->(m)')
# def inner3(a,b,m,M):
#     c = a+b
#     d = np.sum(c,axis=1)
#     return d


# k = np.vectorize(inner3, signature='(m_i),(m_i,n),(),(m_i)->(m_i)')
# res = k(x,y,m,M)
# print(int(2.62917283e-05))



from numba import vectorize, float64
@guvectorize(["void(float64[:,:], float64[:,:], float64[:,:])"],
             "(m,n),(n,p)->(m,p)")
def w(a, b, result):
       c = a*b
       return c



# @vectorize(signature='(m),(m,n),(),(m)->(m)' )
# def inner3(a,b,m,M):
#     c = a+b
#     d = np.sum(c,axis=1)
#     return d

# m = np.array(['1','1'])
# M = m
y = x =np.array([[1, 2],
                  [1, 2]])
# res = inner3(x,y,m,M)

v = w(x,y)

print(w)
print(int(8.34895083e-312))

print(np.sum)




def gravity_force(X_i, x_kj, M_i, M_kn, g=0.001, error_value=0.00001):
    ''''
    G_ik = sum_i g*(M_i.M_kn)* (r_i - r_k)/( (r_i1 - r_k1)^2 +(r_i2 - r_k2)^2 )
    G_i = S_i g.m.M(r_i - r_k)/(|r_i - r_k|^2)

    The core method using for calculation of force Gravity
    on one particle. The force is the sum of all forces coming from other particles

    This method calculates gravity force which acts on particle X_i.
    The force G is a sum of all forces producing from every particle.

    The method is written in NumPy thus it is  vectorized in order to achieve the highest performance

    Parameters :

        X_i  : ndarray [ , ]
        radius vector X_i = [x_ij]
        example :
         X_1 = [x_10,x_11] = [x(axis), y(axis)]

        x_kj : ndarray
        matrix of all coords exclude X_i
        x_kj= [ [x_10, x_11 ], [..., ... ] , [x_k0,x_k1] ]

        g : number 
        gravity constant 

        error_value : float
        special parameter setting  for fixing of  problem in case when the modul |r|
        tends to zero then the F tend to infinity and the model is broken (in real world this cannot happens)
        the error value is the min distance in which the bodies interact one each other 
        with the same constant force in order to prevent Infinity values.
        when this value is aachieve the method will show RuntimeWarning

    Return :
        Sum of all  gravity forces coming from particles x_kj wich acts on particle X_i

    '''
    # prevent calculation of force of body respect to itself
    index1, index2 = np.where(x_kj[:, 0] == X_i[0])[
        0], np.where(x_kj[:, 1] == X_i[1])[0]
    if ((index1 == index2).any()):
        x_kj = np.delete(x_kj, index1, axis=0)
        M_kn = np.delete(M_kn, index1)

    # dr matrix contain all delta elemes [[x_i0 - x_10, x_i1 - x_i1],[...,...],[x_i0 - x_k0, x_i1- x_k1]]
    dr_kj = x_kj - X_i  #
    # return [(x_i0-x_k0)^2,(x_i1-x_k1)^2]
    mod_dr_kj = dr_kj**2
    # return [sum_k (x_i0-x_k0)^2, sum_k (x_i1-x_k1)^2]
    mod_dr_k = np.sum(mod_dr_kj, axis=1)

    # when |dr| --> 0 then F--> infinity
    error_value = 0.0000001
    if (mod_dr_k < error_value).any():
        message = '|dr|, |dr|-->0 , , there for the dr has been repalced by configured error value {}  '.format(
            error_value)
        mod_dr_k[mod_dr_k < error_value] = error_value
        if x_kj.shape[0] > 2:
            warnings.showwarning(
                message, filename='gravity.py', lineno=135, category=RuntimeWarning)

    mod_dr_k = mod_dr_k.reshape(-1, 1)
    M_kn = M_kn.reshape(-1, 1)

    G = g*M_i*M_kn*(dr_kj/mod_dr_k)
    sum_force = np.sum(G, axis=0)
    return sum_force
