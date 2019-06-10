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
g.add_body(Body(1200, 5, 6,3*np.cos(np.pi / 4), -5*np.cos(np.pi / 4),h=step))
g.add_body(Body(1200, 10, 12,-2*np.cos(np.pi / 4), -5*np.cos(np.pi / 4),h=step))
g.add_body(Body(9000, 0, 0, 0.0001,0.0001,h=step))
g.add_body(Body(800, -10, -12,0.001*np.cos(np.pi / 4), 0.02*np.cos(np.pi / 4),h=step))
g.add_body(Body(1200, -16, -16,0.001*np.cos(np.pi / 4), 0.03*np.cos(np.pi / 4),h=step))
g.add_body(Body(200, 10, 10,-2*np.cos(np.pi / 4), -5*np.cos(np.pi / 4),h=step))
g.add_body(Body(2000, 12, 12, 0.0001,0.0001,h=step))
#g.add_body(Body(5000, 3, 5, -1*np.cos(np.pi / 4), -1*np.cos(np.pi / 4),h=step))
#g.add_body(Body(32, -5, -5, -3*np.cos(np.pi / 4), -1*np.cos(np.pi / 4),h=0.1))
#g.add_body(Body(32, 3, 4,  -3*np.cos(np.pi / 4), -1*np.cos(np.pi / 4),h=0.1))
g.calculate(r=1000)

fig = plt.figure(figsize=(6, 6))
fig = plt.figure(figsize=(6, 6))

u = lambda t, x, y: 0
v = lambda t, x, y: -10
#
# point.add_force(f)
# z = point.calculate_radius_vector(20 * np.cos(np.pi / 4), +50 * np.sin(np.pi / 4), n=700)
# plt.plot(z[:, 0], z[:, 1])
n = 200
size = int(g.get_size(n))
# print(size)
anim = animation.FuncAnimation(plt.gcf(), g.update_HTML_animation, interval=1, fargs=(fig,), frames=n, blit=False)
anim.save('video/system-6.mp4', writer=writer)
HTML(anim.to_html5_video())
plt.show()
Writer = animation.writers['ffmpeg']
writer = Writer(fps=15, metadata=dict(artist='Me'), bitrate=1800)

