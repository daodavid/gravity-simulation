# -*- coding: utf-8 -*-
"""
Created on Thu Jun  6 14:53:01 2019

@author: David
"""

from gravity import *
import matplotlib.pyplot as plt
from matplotlib import animation, rc
from IPython.display import HTML
import numpy as np
print("gge")
step=0.01
g = Ground()
g.add_body(Body(1200, 1, 1, 1, 0,h=step))
g.add_body(Body(3000, 5, 1, -1, 0,h=step))

#g.add_body(Body(32, -5, -5, -3*np.cos(np.pi / 4), -1*np.cos(np.pi / 4),h=0.1))
#g.add_body(Body(32, 3, 4,  -3*np.cos(np.pi / 4), -1*np.cos(np.pi / 4),h=0.1))

g.calculate(r=500)

fig = plt.figure(figsize=(6, 6))
fig = plt.figure(figsize=(6, 6))

u = lambda t, x, y: 0
v = lambda t, x, y: -10
#
# point.add_force(f)
# z = point.calculate_radius_vector(20 * np.cos(np.pi / 4), +50 * np.sin(np.pi / 4), n=700)
# plt.plot(z[:, 0], z[:, 1])
n = 400
size = int(g.get_size(n))
# print(size)
anim = animation.FuncAnimation(plt.gcf(), g.update_HTML_animation, interval=1, fargs=(fig,), frames=n, blit=False)
HTML(anim.to_html5_video())
plt.show()