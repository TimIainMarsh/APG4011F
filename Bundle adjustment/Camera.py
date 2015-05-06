import math as mt
class Camera(dict):
        def __init__(self,c):
            self.SensorDimentions =  [0.230,0.230]
            self.c = c
            '''camera layer not really nessisary it just stores c and sensor dim'''




class images(dict):
    kind = 'ImageFromCamera'
    def __init__(self,Xo,Yo,Zo,w,p,k,scale):
            self.scale = scale
        
            self.Xo = Xo
            self.Yo = Yo
            self.Zo = Zo

            self.w = mt.radians(w)
            self.p = mt.radians(p)
            self.k = mt.radians(k)
            '''each image is associated with where the camera
               was at the moment it took the picture'''
    def set_Params():
        pass

class Ray(object):
    def __init__(self,imagePoint,objectPoint):
        self.imagePoint = imagePoint
        self.objectPoint = objectPoint

class imagePoint(object):
    kind = 'PointInImage'
    def __init__(self,xi,yi,zi,scale):
        self.scale = scale
        self.xi = xi
        self.yi = yi
        self.zi = -zi
        ''' each ray belongs to an image. there are as many points as rays'''



class objectPoint(object):
    kind = 'PointInObject'
    def __init__(self,X,Y,Z):
        # self.scale = scale
        self.X = X
        self.Y = Y
        self.Z = Z
        ''' each ray belongs to an image. there are as many points as rays'''
