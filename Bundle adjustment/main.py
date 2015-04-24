from Camera import Camera
from Camera import images
from Camera import imagePoint,objectPoint, Ray
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import random as rd
import math as mt
import numpy as np

camera1x,camera1y,camera1z = 0,0,60
camera2x,camera2y,camera2z = 20,1,60


def plot(Cameras):
    x = []
    y = []
    z = []
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    
    for image_id,image in Cameras.items():

        x.append(image.Xo)
        y.append(image.Yo)
        z.append(image.Zo)

        for ray_id,ray in image.items():
            # print(ray.objectPoint.X,ray.objectPoint.Y,ray.objectPoint.Z)
            x.append(float(ray.objectPoint.X))
            y.append(float(ray.objectPoint.Y))
            z.append(float(ray.objectPoint.Z))
    ax.scatter(x, y, z)
    ax.set_xlabel('X Label')
    ax.set_ylabel('Y Label')
    ax.set_zlabel('Z Label')
    plt.show()   
        
def makeCamera():
    c = 0.0030
    camera = Camera(c)
    
    for i in range(1):
        scale = 20000
        camera[i] = images(camera1x,camera1y,camera1z,0,0,30,scale)

        for j in range(100):
            scale = (20000 + (rd.random()*10))
            camera[i][j] = setRay(imagePoint(0,0,scale),objectPoint(0,0,0))
    Give_Ray_Grid(camera)
    return camera

def setRay(one,two):
    return Ray(one,two)

def Give_Ray_Grid(Cameras):
    for i in range(1):
        count = 0
        for r in range(10):
            for c in range(10):
                Cameras[i][count].imagePoint.xi = (r-3)/1000
                Cameras[i][count].imagePoint.yi = (c-3)/1000
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
    # print(obj)
    objectPoint.X = float(obj[0])
    objectPoint.Y = float(obj[1])
    objectPoint.Z = float(obj[2])

def calculate_imagePoint(Cameras):
    for image_id,image in Cameras.items():
        print('number')
        c = Cameras.c
        for ray_id,ray in image.items():
            imagePoint = ray.imagePoint
            objectPoint = ray.objectPoint
            calculate_IP(imagePoint,objectPoint,image,c)

def calculate_IP(imagePoint,objectPoint,image,c):
    pass
def get_objectCoordList(image):
    ocl = []
    for ray_id,ray in image.items():
        o = ray.objectPoint
        ocl.append([o.X,o.Y,o.Z])
    return ocl

if __name__ == '__main__':
    '''create the first camera and popylate its image coords'''
    Cameras = makeCamera()
    ''' solving for the object coords from the first image'''
    calculate_objectPoint(Cameras)
    '''Creating an object coordinate list. so that i can sole it in 2nd image without 
        first image being present'''
    objectCoordList = get_objectCoordList(Cameras[0])

    Cameras[1] = images(camera2x,camera2y,camera2z,5,5,45,20000)

    print (objectCoordList)

    # calculate_imagePoint(Cameras)

            

    plot(Cameras)


    print (objectCoordList)

    # calculate_imagePoint(Cameras)

            

    plot(Cameras)
