from Camera import Camera
from Camera import images
from Camera import imagePoint

import random as rd

def makeCamera():
    c = 30
    camera = Camera(c)
    
    for i in range(2):
        scale = 20000
        camera[i] = images(10,10,10,0,0,90,scale)
        for j in range(36):
            scale = 20000 + rd.random()
            camera[i][j] = imagePoint(0,0,scale)
    return camera
        
def Give_Ray_Grid(Cameras):
    for i in range(2):
        count = 0
        for r in range(6):
            for c in range(6):
                Cameras[i][count].xo = r
                Cameras[i][count].yo = c
                count += 1


if __name__ == '__main__':
    Cameras = makeCamera()
    Give_Ray_Grid(Cameras)

    
                
    




