
from __future__ import absolute_import
from ..PotentialFieldCalculator import *


__author__ = 'lexic92'

attractive = []
repulsive = []
tangential = []



 #Blue base (the top one)
#attractive.append(AttractiveObject(x=0, y=370, radius=30, spread=100, alpha=1))

#Red base (the left one)
#attractive.append(AttractiveObject(x=-370, y=0, radius=30, spread=100, alpha=1))


#Top Left L
tangential.append(TangentialObject(x=-90, y=120, radius=30, spread=150, beta=1))
tangential.append(TangentialObject(x=-90, y=180, radius=30, spread=150, beta=1))
tangential.append(TangentialObject(x=-150, y=120, radius=30, spread=150, beta=1))

#Top Right L
tangential.append(TangentialObject(x=150, y=120, radius=30, spread=100, beta=1))
tangential.append(TangentialObject(x=150, y=180, radius=30, spread=100, beta=1))
tangential.append(TangentialObject(x=210, y=120, radius=30, spread=100, beta=1))

#Bottom Right L
tangential.append(TangentialObject(x=150, y=-120, radius=30, spread=100, beta=1))
tangential.append(TangentialObject(x=210, y=-120, radius=30, spread=100, beta=1))
tangential.append(TangentialObject(x=150, y=-180, radius=30, spread=100, beta=1))

#Bottom Left L
tangential.append(TangentialObject(x=-90, y=-120, radius=30, spread=100, beta=1))
tangential.append(TangentialObject(x=-90, y=-180, radius=30, spread=100, beta=1))
tangential.append(TangentialObject(x=-150, y=-120, radius=30, spread=100, beta=1))

#Top Left L
tangential.append(TangentialObject(x=-90, y=120, radius=30, spread=100, beta=1))
tangential.append(TangentialObject(x=-90, y=180, radius=30, spread=100, beta=1))
tangential.append(TangentialObject(x=-150, y=120, radius=30, spread=100, beta=1))

#Middle Rectangular Obstacle
tangential.append(TangentialObject(x=0, y=10, radius=60, spread=100, beta=10))
