"""
Created on Mon Jun 10 09:58:53 2019

@author: David
"""

from daomechanics.gravity import *
import matplotlib.pyplot as plt
from matplotlib import animation, rc
from IPython.display import HTML
import numpy as np

step = 0.05 # integration step
g = Ground()
g.show_tragectory(True)


### generate 3 body with different mass 
g.add_body(Body(10000, -1,-15 ,-0.000001*np.cos(np.pi / 4), 0.0000001*np.cos(np.pi / 4),h=step))
g.add_body(Body(1000, -6, -4,1*np.cos(np.pi / 4), 1*np.cos(np.pi / 4),h=step))
g.add_body(Body(1000, -7, -23,1.2*np.cos(np.pi / 4), -1.5*np.cos(np.pi / 4),h=step))

g.calculate(r=100)

fig = plt.figure(figsize=(6, 6))
fig = plt.figure(figsize=(6, 6))
  
u = lambda t, x, y: 0
v = lambda t, x, y: -10


n = 100
size = int(g.get_size(n))

Writer = animation.writers['ffmpeg']
writer = Writer(fps=15, metadata=dict(artist='Me'), bitrate=1800)
anim = animation.FuncAnimation(plt.gcf(), g.update_HTML_animation, interval=1, fargs=(fig,), frames=n, blit=False)
anim.save('system-goodbodyyy.mp4', writer=writer)
HTML(anim.to_html5_video())
plt.show()

