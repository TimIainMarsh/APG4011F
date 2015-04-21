
class Camera(dict):
        def __init__(self,c):
            self.SensorDimentions =  [230,230]
            self.c = c
            '''camera layer not really nessisary it just stores c and sensor dim'''




class images(dict):
    def __init__(self,Xo,Yo,Zo,w,t,k,scale):
            self.scale = scale
        
            self.Xo = Xo
            self.Yo = Yo
            self.Zo = Zo

            self.w =  w
            self.t = t
            self.k = k
            '''each image is associated with where the camera
               was at the moment it took the picture'''

class imagePoint(object):
    def __init__(self,xo,yo,scale):
        self.scale = scale
        self.xo = xo
        self.yo = yo
        ''' each ray belongs to an image. there are as many points as rays'''
