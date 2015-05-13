
from __future__ import absolute_import
from ..PotentialFieldCalculator import *


__author__ = 'lexic92'

attractive = []
repulsive = []
tangential = []

#Reference for syntax
#attractive.append(AttractiveObject(x=150.0, y=120.0, radius=30, spread=1000000, alpha=1))

#From the email list: (Treat the following string as a block comment)
# Email list is missing the x=0, y=0 middle box thing.
comment='''
{'y': 120.0, 'x': 150.0}
{'y': 180.0, 'x': 150.0}
{'y': 120.0, 'x': 210.0}
{'y': -120.0, 'x': 150.0}
{'y': -120.0, 'x': 210.0}
{'y': -180.0, 'x': 150.0}
{'y': -120.0, 'x': -90.0}
{'y': -180.0, 'x': -90.0}
{'y': -120.0, 'x': -150.0}
{'y': 120.0, 'x': -90.0}
{'y': 180.0, 'x': -90.0}
{'y': 120.0, 'x': -150.0}
{'y': 0.0, 'x': 10.0}


all 30 except the middle radius is 60.
'''
# I am just guessing on spread=100. Might need to adjust later.
repulsive.append(RepulsiveObject(x=150.0, y=120.0, radius=30, spread=100, alpha=1))
repulsive.append(RepulsiveObject(x=150.0, y=180.0, radius=30, spread=100, alpha=1))
repulsive.append(RepulsiveObject(x=210.0, y=120.0, radius=30, spread=100, alpha=1))
repulsive.append(RepulsiveObject(x=150.0, y=-120.0, radius=30, spread=100, alpha=1))
repulsive.append(RepulsiveObject(x=210.0, y=-120.0, radius=30, spread=100, alpha=1))
repulsive.append(RepulsiveObject(x=150.0, y=-180.0, radius=30, spread=100, alpha=1))
repulsive.append(RepulsiveObject(x=-90.0, y=-120.0, radius=30, spread=100, alpha=1))
repulsive.append(RepulsiveObject(x=-90.0, y=-180.0, radius=30, spread=100, alpha=1))
repulsive.append(RepulsiveObject(x=-150.0, y=-120.0, radius=30, spread=100, alpha=1))
repulsive.append(RepulsiveObject(x=-90.0, y=120.0, radius=30, spread=100, alpha=1))
repulsive.append(RepulsiveObject(x=-90.0, y=180.0, radius=30, spread=100, alpha=1))
repulsive.append(RepulsiveObject(x=-150.0, y=120.0, radius=30, spread=100, alpha=1))
repulsive.append(RepulsiveObject(x=10.0, y=0.0, radius=30, spread=100, alpha=1))

# Email list is missing the x=0, y=0 middle box thing. So I added it here:
repulsive.append(RepulsiveObject(x=0.0, y=0.0, radius=60, spread=100, alpha=1))
