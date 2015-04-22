
import logging

import numpy as np
import math as mt
from point import Point
from scipy.spatial import cKDTree
from scipy.linalg import svd, norm
from timing import log_timing, log_timing_decorator
from multiprocessing import Pool

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.error('Start')


def find_index_of_nearest_xyz(tree, point):
    dist , idx = tree.query(point,k=20)
    return idx


@log_timing_decorator('computeNormals',logger)
def computeNormals(PointsXYZ):

    p = Pool(4)

    f1,f2 = PointsXYZ[:int(len(PointsXYZ)/2)],PointsXYZ[int(len(PointsXYZ)/2):]
    one, two = f1[:int(len(f1)/2)],f1[int(len(f1)/2):]
    three,four = f2[:int(len(f2)/2)],f2[int(len(f2)/2):]

    jobs = [[one,PointsXYZ],[two,PointsXYZ],[three,PointsXYZ],[four,PointsXYZ]]
    
    L1,L2,L3,L4= p.starmap(Normals,jobs)
    PointsNormal = L1+L2+L3+L4
    return PointsNormal

def Normals(Points,TreePoints):
    PointsNormal = []
    tree = cKDTree(TreePoints)
        
    for point in Points:
        idx = find_index_of_nearest_xyz(tree, point)
        neighbors = []
        for i in idx:
            neighbors.append(TreePoints[i])
        normal = NormalCalc(neighbors)
        PointsNormal.append([point[0],point[1],point[2],len(idx),normal[0],normal[1],normal[2],0])
    return PointsNormal

def NormalCalc(neighbors):
    u,s,v = svd(neighbors)
    return v[2]

def ang_classing(PointsNormal):
    vertVec = [0,0,1]
    for point in PointsNormal:
        pointVect = [point[4],point[5],point[6]]

        ang = mt.degrees(float(FindAng(vertVec,pointVect)))
        point[3] = ang
        
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
    sinang = norm(np.cross(v1, v2))
    return np.arctan2(sinang, cosang)

def signalFinish():
    import winsound
    Freq = 1500 # Set Frequency To 2500 Hertz
    Dur = 200 # Set Duration To 1000 ms == 1 second
    winsound.Beep(Freq,Dur)
    winsound.Beep(Freq,Dur)
    winsound.Beep(Freq,Dur)

@log_timing_decorator('Read Points', logger)
def Read_Points(filename):
    Points = []
    f = open(filename , 'r')
    for line in f.readlines():
        read = []
        sp = line.split(';')
        Points.append([float(sp[0]),float(sp[1]),float(sp[2])])
    f.close()
    return Points

@log_timing_decorator('Write Points', logger)
def WriteFile(PointsNormal,fileName):
    f = open('PointsAfter.xyz','w')
    f.write('PointX PointY PointZ AngleFromvertical NormalX NormalY NormalZ Classification\n')
    for line in PointsNormal:
        for i in line:
            f.write(str(i)+' ')
        f.write('\n')

@log_timing_decorator('main',logger)
def main():
    filename = 'Points.xyz'
    PointsXYZ = Read_Points(filename)
    '''Calculate Normals'''
    PointsNormal = computeNormals(PointsXYZ)
    '''calculate the angle from vertical to the normal'''
    ang_classing(PointsNormal)
    fileName = 'PointsAfter.xyz'
    WriteFile(PointsNormal,fileName)
    signalFinish()


if __name__ == '__main__':
    from time import gmtime, strftime
    print(strftime("%Y-%m-%d %H:%M:%S", gmtime()))
    main()
    print(strftime("%Y-%m-%d %H:%M:%S", gmtime()))
