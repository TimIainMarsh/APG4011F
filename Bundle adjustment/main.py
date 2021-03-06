from Camera import Camera
from Camera import images
from Camera import imagePoint,objectPoint, Ray
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import random as rd
import math as mt
import numpy as np
from random import randrange
import LeastSquares as LS




camera1x,camera1y,camera1z = 0,0,500
camera2x,camera2y,camera2z = 1000,0,500
number = 30

def PL(ax,Cameras,colour,sensDim):
    x = []
    y = []
    z = []

    

    x.append(Cameras.Xo)
    y.append(Cameras.Yo)
    z.append(Cameras.Zo)

    for ray_id,ray in Cameras.items():
        # print(ray.objectPoint.X,ray.objectPoint.Y,ray.objectPoint.Z)
        x.append(float(ray.objectPoint.X))
        y.append(float(ray.objectPoint.Y))
        z.append(float(ray.objectPoint.Z))

                 
    ax.scatter(x, y, z,color = colour)
    ax.set_xlabel('X Axis')
    ax.set_ylabel('Y Axis')
    ax.set_zlabel('Z Axis')

    for ray_id,ray in Cameras.items():
        if checkIfSensor(ray,sensDim):
            ax.plot([Cameras.Xo, ray.objectPoint.X], [Cameras.Yo, ray.objectPoint.Y], zs=[Cameras.Zo, ray.objectPoint.Z], c=colour)

def checkIfSensor(ray,sensDim):
    if ray.imagePoint.xi > float(sensDim[0]) or ray.imagePoint.xi < -float(sensDim[0]):
        return False
    if ray.imagePoint.yi > float(sensDim[0]) or ray.imagePoint.yi < -float(sensDim[0]):
        return False
    return True

def plotOBJ(Cameras):
    sensDim = Cameras.SensorDimentions
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    colour = ['b','g']
    for cam_name, camera in Cameras.items():
        print(cam_name)
        if cam_name == 1: break
        PL(ax,camera,colour[cam_name],sensDim)
    plt.axis('equal')
    plt.show()

def plotIMG(Cameras):
    x = []
    y = []
    z = []
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    
    for image_id,image in Cameras.items():
        for ray_id,ray in image.items():

            # print(ray.objectPoint.X,ray.objectPoint.Y,ray.objectPoint.Z)
            x.append(float(ray.imagePoint.xi))
            y.append(float(ray.imagePoint.yi))
            z.append(float(ray.imagePoint.zi))

    ax.scatter(x, y,z)
    ax.set_xlabel('X Label')
    ax.set_ylabel('Y Label')
    ax.set_zlabel('Z Label')
    plt.show()   

def makeCamera():
    c = 0.0030
    camera = Camera(c)
    
    for i in range(1):
        scale = 20000
        camera[i] = images(camera1x,camera1y,camera1z,0,0,0,scale)

        for j in range(number):
            scale = (20000 + (rd.random()*10))
            camera[i][j] = Ray(imagePoint(0,0,camera.c,scale),objectPoint(0,0,0))
    Give_Ray_Grid(camera.SensorDimentions,camera[0])
    return camera

def setRay(one,two):
    return Ray(one,two)

def Give_Ray_Grid(dim,image):
    count = 0
    rngX = (dim[0]/2.0)*1000
    rngY = (dim[1]/2.0)*1000

    for r in range(number):
        image[count].imagePoint.xi = randrange(-rngX,rngX)/1000
        image[count].imagePoint.yi = randrange(-rngY,rngY)/1000
        count += 1

def calculate_objectPoint(c,image):
    for ray_id,ray in image.items():
        imagePoint = ray.imagePoint
        objectPoint = ray.objectPoint
        calculate_OP(imagePoint,objectPoint,image,c)

def calculate_OP(imagePoint,objectPoint,image,c):
    '''Calculates object point from image Point'''
    scale = imagePoint.scale

    R = LS.rotations(image)
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

# def calculate_imagePoint(Cameras):
#     for image_id,image in Cameras.items():
#         c = Cameras.c
#         for ray_id,ray in image.items():
#             imagePoint = ray.imagePoint
#             objectPoint = ray.objectPoint
#             calculate_IP(imagePoint,objectPoint,image,c)

def calculate_imagePoint(c,image,objectCoordList):
    R = LS.rotations(image)
    count = 0
    for obj_id,obj in objectCoordList.items():

        image[count] = setRay(imagePoint(0,0,c,20000),objectPoint(0,0,0))
        X = float(obj[0])
        Y = float(obj[1])
        Z = float(obj[2])
        iP = image[count].imagePoint
        intermediate = np.matrix([[(R[0,0]* (X-image.Xo) + R[0,1]* (Y-image.Yo) + R[0,2]* (Z-image.Zo))],
                                  [(R[1,0]* (X-image.Xo) + R[1,1]* (Y-image.Yo) + R[1,2]* (Z-image.Zo))],
                                  [(R[2,0]* (X-image.Xo) + R[2,1]* (Y-image.Yo) + R[2,2]* (Z-image.Zo))]])

        imgPTS = (1/image.scale) * intermediate
        # print(imgPTS[0],imgPTS[1])
        image[count].imagePoint.xi = float(imgPTS[0])
        image[count].imagePoint.yi = float(imgPTS[1])

        image[count].objectPoint.X = float(X)
        image[count].objectPoint.Y = float(Y)
        image[count].objectPoint.Z = float(Z)
        count += 1




def get_objectCoordList(image):
    ocl = {}
    for ray_id,ray in image.items():
        o = ray.objectPoint
        ocl[ray_id] = ([o.X+(rd.random()*10),o.Y+(rd.random()*10),o.Z+(rd.random()*10)])
    return ocl

if __name__ == '__main__':
    '''create the first camera and popylate its image coords'''
    
    Cameras = makeCamera()
    
    ''' solving for the object coords from the first image'''

    calculate_objectPoint(Cameras.c, Cameras[0])

    '''Creating an object coordinate list. so that i can solve it in 2nd image without 
        first image being present'''
    objectCoordList = get_objectCoordList(Cameras[0])

    '''                 Xo,           Yo,  Zo      w, p,k,scale'''
    Cameras[1] = images(camera2x,camera2y,camera2z,0,0,0,20000)

    
    '''calculate img coords from list created'''
    calculate_imagePoint(Cameras.c,Cameras[1],objectCoordList)

    '''re calculating object points only using 2nd camera''' 
    calculate_objectPoint(Cameras.c, Cameras[1])



    ''' cam 1 - img - obj
        cam 2 - img - obj'''


    


    '''from the image points of the two points calculating the coresponding object points from a homogenious set of points'''\
    '''cloning image 1 to 'newCam' without orr params'''

    # Cameras['newCam'] = Cameras[0]
    # Cameras['newCam'].clearParams()
    # provRx,provRy,provRz = 0,0,0
    # LS.calcOBJpoints(Cameras['newCam'],provRx,provRy,provRz)
    plotOBJ(Cameras)