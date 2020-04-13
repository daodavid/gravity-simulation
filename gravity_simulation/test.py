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