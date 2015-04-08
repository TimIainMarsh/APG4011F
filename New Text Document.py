import numpy as np
import scipy.linalg as LA

m = [[1,2,3],
     [2,3,4],
     [5,3,8],
     [4,7,3],
     [2,5,6],
     [4,7,8]]

covar = np.cov(m)

u,s,v = LA.svd(m)
print (u)
print (s)
print (v)
