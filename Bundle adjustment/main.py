from Camera import Camera
from Camera import images
from Camera import imagePoint,objectPoint, Ray

import random as rd
import math as mt
import numpy as np

def makeCamera():
    c = 30
    camera = Camera(c)
    
    for i in range(1,3):
        scale = 2000
        if i == 1:
            camera[i] = images(100,100,1000,0,0,0,scale)
        elif i == 2:
            camera[i] = images(120,120,1000,0,0,0,scale)

        for j in range(1,37):
            scale = (2000 + (rd.random()*10))
            camera[i][j] = setRay(imagePoint(0,0,scale),objectPoint(0,0,0))
    return camera

def setRay(one,two):
    return Ray(one,two)

def Give_Ray_Grid(Cameras):
    for i in range(1,3):
        count = 1
        for r in range(1,7):
            for c in range(1,7):
                Cameras[i][count].imagePoint.xi = (r-3)
                Cameras[i][count].imagePoint.yi = (c-3)
                count += 1

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
    return (Rp * Rk * Rw)

def calculate_objectPoint(Cameras):
    for image_id,image in Cameras.items():
        c = Cameras.c
        for ray_id,ray in image.items():
            imagePoint = ray.imagePoint
            objectPoint = ray.objectPoint
            calculate_OP(imagePoint,objectPoint,image,c)

def calculate_OP(imagePoint,objectPoint,image,c):
    '''Calculates object point from image Point'''
    scale = imagePoint.scale

    R = rotations(image)
    # print(R)
    imagePointVector = np.matrix([[imagePoint.xi],
                                  [imagePoint.yi],
                                  [-c]])
    imageCenter = np.matrix([[image.Xo],
                             [image.Yo],
                             [image.Zo]])
    obj = (scale * R * imagePointVector) + imageCenter
    print(obj)
    objectPoint.X = float(obj[0])
    objectPoint.Y = float(obj[1])
    objectPoint.Z = float(obj[2])

def recalculate_imagePoint(Cameras):
    obspts = []
    for image_id,image in Cameras.items():
        for ray_id,ray in image.items():
            x,y,z = ray.objectPoint.X,ray.objectPoint.Y,ray.objectPoint.Z
            obspts.append([x,y,z])

    # print(obspts)
    pass

if __name__ == '__main__':
    Cameras = makeCamera()
    Give_Ray_Grid(Cameras)
    calculate_objectPoint(Cameras)

    # recalculate_imagePoint(Cameras)

            

    x = [100,200]
    y = [100,200]
    z = [100,100]
    for image_id,image in Cameras.items():
        for ray_id,ray in image.items():
            print(ray.objectPoint.X,ray.objectPoint.Y,ray.objectPoint.Z)
            x.append(float(ray.objectPoint.X))
            y.append(float(ray.objectPoint.Y))
            z.append(float(ray.objectPoint.Z))


    from mpl_toolkits.mplot3d import Axes3D
    import matplotlib.pyplot as plt
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(x, y, z)
    ax.set_xlabel('X Label')
    ax.set_ylabel('Y Label')
    ax.set_zlabel('Z Label')
    plt.show()   
        




