import logging

import numpy as np
import math as mt

from timing import log_timing, log_timing_decorator

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.error('Start')



filename = 'jameson - Cloud(2).xyz'

f = open(filename , 'r')

from point import Point

Points = []
for line in f:
    sp = line.split(';')
    minY, maxY = -10.0,10.0
    minX, maxX = -10.0,10.0
    minZ, maxZ = -10,10.0
    #print('here')

    if float(sp[0])<maxX and float(sp[0])>minX:

        if float(sp[1])<maxY and float(sp[1])>minY:

            if float(sp[2])<maxZ and float(sp[2])>minZ:

                Points.append(Point(float(sp[0]),float(sp[1]),float(sp[2])))

print('read')
f = open('Ponts.xyz','w')
for line in Points:
    line = str(line.x)+';'+str(line.y)+';'+str(line.z)+'\n'
    f.write(line)
