import numpy as np
import math as mt
import sympy as sy

import sys
sys.setrecursionlimit(5000)

def calcOBJpoints(image,provRx,provRy,provRz):
    '''given image and c'''
    '''we have 100 img pts, 100 obj pts

    unknowns'''

    Xo = sy.Symbol('Xo')
    Yo = sy.Symbol('Yo')
    Zo = sy.Symbol('Zo')
    rx = sy.Symbol('rx')
    ry = sy.Symbol('ry')
    rz = sy.Symbol('rz')
    scale = sy.Symbol('scale')

    Rx =  np.matrix([[1, 0, 0],
                     [0, sy.cos(rx), -sy.sin(rx)],
                     [0, sy.sin(rx), sy.cos(rx)]])

    Ry =  np.matrix([[sy.cos(ry), 0, sy.sin(ry)],
                     [0, 1, 0],
                     [-sy.sin(ry), 0, sy.cos(ry)]])

    Rz =  np.matrix([[sy.cos(rz), -sy.sin(rz), 0],
                     [sy.sin(rz), sy.cos(rz), 0],
                     [0, 0, 1]])

    RotM = Rx * Ry * Rz

    PerspectiveC = np.matrix([[Xo],
                              [Yo],
                              [Zo]])
    obj = np.matrix([[X],
                     [Y],
                     [Z]])


    image_coords = scale * RotM * (obj - PerspectiveC)
    x = image_coords.item(0)
    y = image_coords.item(1)
    negative_c = image_coords.item(2)

    A = np.matrix([[0] * (6+len(image)),])
    A = np.delete(A, (0), axis=0)

    L = np.matrix([[0],])
    L = np.delete(L, (0), axis=0)


    for ray_name, ray in image.items():
        imageP = ray.imagePoint
        objP = ray.objectPoint

        dYo = sy.diff(x,Yo).subs(rx,dx)
        dXo = sy.diff(x,Xo).subs(rx,dx)
        dZo = sy.diff(x,Zo).subs(rx,dx)
        dRx = sy.diff(x,rx).subs(rx,dx)
        dRy = sy.diff(x,ry).subs(rx,dx)
        dRz = sy.diff(x,rz).subs(rx,dx)

        

        L = np.vstack([L,[imageP.X - x]])

        # A = np.vstack([A,[0,0,0,0,0,0,0]])
        # A = np.vstack([A,[0,0,0,0,0,0,0]])









    print (A)
    

    return 0




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

''' unknowns are = [ Xo, Yo, Zo, dk, dk, dw, scale(for eash point)]









'''