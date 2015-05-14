__author__ = 'lexic92'
from __future__ import absolute_import
from ..PotentialFieldCalculator import *

attractive = []
repulsive = []
tangential = []

#Blue base
#attractive.append(AttractiveObject(x=0, y=370, radius=10, spread=20, alpha=1))

#Red base
#repulsive.append(AttractiveObject(x=0, y=-370, radius=10, spread=100, beta=1))

#4 boxes
#RIGHT
tangential.append(TangentialObject(x=121.2132034355, y=21.2132034356, radius=30, spread=60, beta=1))

#LEFT
tangential.append(TangentialObject(x=-78.78679656439999, y=21.2132034356, radius=30, spread=60, beta=1, clockwise=False))

#TOP
tangential.append(TangentialObject(x=21.2132034356, y=121.2132034355, radius=30, spread=60, beta=1))

#BOTTOM
tangential.append(TangentialObject(x=21.2132034356, y=-78.78679656439999, radius=30, spread=60, beta=1))