# -*- coding: utf-8 -*-
"""
Created on Mon Jun 10 09:58:53 2019

@author: David
"""

from gravity import *
import matplotlib.pyplot as plt
from matplotlib import animation, rc
from IPython.display import HTML
import numpy as np
print("gdasdasge")
print("WOW WOW OWWO!!")
step = 0.05
g = Ground()
g.show_tragectory(True)

g.add_body(Body(100000, -1,-15 ,-0.00001*np.cos(np.pi / 4), 0.0001*np.cos(np.pi / 4),h=step))
g.add_body(Body(10000, -6, -4,1*np.cos(np.pi / 4), 1*np.cos(np.pi / 4),h=step))

g.calculate(r=6000)

fig = plt.figure(figsize=(6, 6))
fig = plt.figure(figsize=(6, 6))

u = lambda t, x, y: 0
v = lambda t, x, y: -10
#
# point.add_force(f)
# z = point.calculate_radius_vector(20 * np.cos(np.pi / 4), +50 * np.sin(np.pi / 4), n=700)
# plt.plot(z[:, 0], z[:, 1])
n = 300
size = int(g.get_size(n))
# print(size)
anim = animation.FuncAnimation(plt.gcf(), g.update_HTML_animation, interval=1, fargs=(fig,), frames=n, blit=False)
anim.save('video/system-3--37-body.mp4', writer=writer)
HTML(anim.to_html5_video())
plt.show()
Writer = animation.writers['ffmpeg']
writer = Writer(fps=15, metadata=dict(artist='Me'), bitrate=1800)

