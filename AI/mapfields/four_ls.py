import AI.PotentialFieldCalculator


__author__ = 'lexic92'

attractive = []
repulsive = []
tangential = []

attractive.append(AttractiveObject(x=flag.x, y=flag.y, radius=10, spread=1000000, alpha=1))
attractive.append(AttractiveObject(x=flag.x, y=flag.y, radius=10, spread=1000000, alpha=1))
attractive.append(AttractiveObject(x=flag.x, y=flag.y, radius=10, spread=1000000, alpha=1))
attractive.append(AttractiveObject(x=flag.x, y=flag.y, radius=10, spread=1000000, alpha=1))
attractive.append(AttractiveObject(x=flag.x, y=flag.y, radius=10, spread=1000000, alpha=1))
attractive.append(AttractiveObject(x=flag.x, y=flag.y, radius=10, spread=1000000, alpha=1))


repulsive.append(RepulsiveObject(x=point[0], y=point[1], radius=3, spread=6, alpha=10))
repulsive.append(RepulsiveObject(x=point[0], y=point[1], radius=3, spread=6, alpha=10))
repulsive.append(RepulsiveObject(x=point[0], y=point[1], radius=3, spread=6, alpha=10))
repulsive.append(RepulsiveObject(x=point[0], y=point[1], radius=3, spread=6, alpha=10))
repulsive.append(RepulsiveObject(x=point[0], y=point[1], radius=3, spread=6, alpha=10))
