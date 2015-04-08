import logging

import numpy as np
import math as mt
from point import Point
from scipy.spatial import cKDTree
import scipy.linalg as LA

from timing import log_timing, log_timing_decorator

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.error('Start')


def find_index_of_nearest_xyz(tree, data, point):
    dist , idx = tree.query(point,k=50)
    return idx

@log_timing_decorator('computeNormals',logger)
def computeNormals(PointsXYZ):
    PointsNormal = []
    tree = cKDTree(PointsXYZ)
    for point in PointsXYZ:
        idx = find_index_of_nearest_xyz(tree, PointsXYZ, point)
        neighbors = []
        for i in idx:
            neighbors.append(PointsXYZ[i])
        normal = NormalCalc(neighbors)
        PointsNormal.append([point[0],point[1],point[2],len(idx),normal[0],normal[1],normal[2],0])
    return PointsNormal


def NormalCalc(neighbors):
    u,s,v = LA.svd(neighbors)
    return v[2]

@log_timing_decorator('ang_classing',logger)
def ang_classing(PointsNormal):
    vertVec = [0,0,1]
    for point in PointsNormal:
        pointVect = [point[4],point[5],point[6]]
        

        ang = mt.degrees(float(FindAng(vertVec,pointVect)))
        if ang>90.0:
            ang = 180-ang
        point[3] = ang
        if ang <= 40.0:
            point[7] = 1
        elif ang >= 60.0:
            point[7] = 2
        else:
            point[7] = 3

def FindAng(v1, v2):
    """ Returns the angle in radians between vectors 'v1' and 'v2'    """
    cosang = np.dot(v1, v2)
    sinang = LA.norm(np.cross(v1, v2))
    return np.arctan2(sinang, cosang)

def signalFinish():
    import winsound
    Freq = 1500 # Set Frequency To 2500 Hertz
    Dur = 200 # Set Duration To 1000 ms == 1 second
    winsound.Beep(Freq,Dur)
    winsound.Beep(Freq,Dur)
    winsound.Beep(Freq,Dur)

@log_timing_decorator('main',logger)
def main():
    filename = 'Points.xyz'

    f = open(filename , 'r')

    PointsXYZ = []
    with log_timing('Reading File',logger):
        count = 0
        for line in f.readlines():
            count += 1
            read = []
            sp = line.split(';')
            PointsXYZ.append([float(sp[0]),float(sp[1]),float(sp[2])])
            #if count == 100000:
              #  break
        f.close()
    '''Calculate Normals'''
    PointsNormal = computeNormals(PointsXYZ)
    
    PointsXYZ = []
    '''calculate the angle from vertical to the normal'''
    ang_classing(PointsNormal)

    
    f = open('PointsAfter.xyz','w')
    f.write('PointX PointY PointZ AngleFromvertical NormalX NormalY NormalZ Classification\n')
    with log_timing('Writing File',logger):
        for line in PointsNormal:
            for i in line:
                f.write(str(i)+' ')
            f.write('\n')
    signalFinish()

if __name__ == '__main__':
    main()
