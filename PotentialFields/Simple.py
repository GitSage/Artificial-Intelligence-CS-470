__author__ = 'byocum'

import matplotlib.pyplot as plt
import numpy

fig = plt.figure()
ax = fig.add_subplot(111)

#generate grid
x = numpy.linspace(-2, 2, 100)
y = numpy.linspace(-1.5, 1.5, 24)
x, y = numpy.meshgrid(x, y)

#calculate vector grid
vx = -y/numpy.sqrt(x**2 + y**2)*numpy.exp(-(x**2+y**2))
vy =  x/numpy.sqrt(x**2 + y**2)*numpy.exp(-(x**2+y**2))



ax.quiver(x, y ,vx, vy, pivot='middle', color='r', headwidth=4, headlength=6)
ax.set_xlabel('$x$') # $ cosmetically changes how the x looks
ax.set_ylabel('$y$')
ax.axis('image')
plt.show()
plt.savefig('visualization_vector_fields_1.png')

