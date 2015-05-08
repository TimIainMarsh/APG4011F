import numpy as np
import math as mt
import sympy as sy

def calcOBJpoints():
    '''unknowns'''

    Xo = sy.Symbol('Xo')
    Yo = sy.Symbol('Yo')
    Zo = sy.Symbol('Zo')
    scale = sy.Symbol('scale')
    rx = sy.Symbol('rx')
    ry = sy.Symbol('ry')
    rz = sy.Symbol('rz')



    Rx =  np.matrix([[1, 0, 0],
                        [0, sy.cos(rx), -sy.sin(rx)],
                        [0, sy.sin(rx), sy.cos(rx)]])

    Ry =  np.matrix([[sy.cos(ry), 0, sy.sin(ry)],
                        [0, 1, 0],
                        [-sy.sin(ry), 0, sy.cos(ry)]])

    Rz =  np.matrix([[sy.cos(rz), -sy.sin(rz), 0],
                        [sy.sin(rz), sy.cos(rz), 0],
                        [0, 0, 1]])

    R = Rx * Ry * Rz



    unknowns = [rx ,ry ,rz ,Xo ,Yo ,Zo ,scale]

    print (unknowns)
    

    # A = np.zeros(shape=(len(unknowns),len(Obs)))

    # print(A)
    

    return 0


calcOBJpoints()
def rotationsSym():
    p = sy.Symbol('p')
    k = sy.Symbol('k')
    w = sy.Symbol('w')


    r11 = sy.cos(p)*sy.cos(k)
    r12 = -sy.cos(p)*sy.sin(k)
    r13 = sy.sin(p)

    r21 = sy.sin(w)*sy.sin(p)*sy.cos(k) + sy.cos(w)* sy.sin(k)
    r22 = -sy.sin(w)*sy.sin(p)*sy.sin(k) + sy.cos(w)* sy.cos(k)
    r23 = -sy.sin(w)* sy.cos(p)

    r31 = -sy.cos(w)*sy.sin(p)*sy.cos(k) + sy.sin(w)* sy.sin(k)
    r32 = -sy.cos(w)*sy.sin(p)*sy.sin(k) + sy.sin(w)* sy.cos(k)
    r33 = -sy.cos(w)* sy.cos(p)

    return r11,r12,r13,r21,r22,r23,r31,r32,r33




def rotations(image):
    Rp = np.matrix([[mt.cos(image.p),0 ,-mt.sin(image.p)],
                    [0              ,1 ,               0],
                    [mt.sin(image.p),0 ,mt.cos(image.p)]])

    Rk = np.matrix([[mt.cos(image.k) ,mt.sin(image.k),0],
                    [-mt.sin(image.k),mt.cos(image.k),0],
                    [0               ,0              ,1]])

    Rw = np.matrix([[1                 ,0,              0],
                    [0,mt.cos(image.w) ,mt.sin(image.w)],
                    [0,-mt.sin(image.w),mt.cos(image.w)]])
    return (Rw * Rp * Rk)


'''part 2'''
'''least squares stuff'''