# -*- coding: utf-8 -*-
"""
Created on Mon Jun 10 14:45:12 2019

@author: David
"""

# -*- coding: utf-8 -*-
"""
Created on Mon Jun 10 13:54:13 2019

@author: David
"""

# -*- coding: utf-8 -*-
"""
Created on Fri Jun  7 13:22:06 2019

@author: David
"""

# -*- coding: utf-8 -*-
"""
Created on Thu Jun  6 14:57:40 2019

@author: David
"""
from gravity import *
import matplotlib.pyplot as plt
from matplotlib import animation, rc
from IPython.display import HTML
from random import *
import numpy as np
print("gdasdasge")
print("WOW WOW OWWO!!")

#g.add_body(Body(1220, 1, 1, 0.01, 0.001,h=step))
#g.add_body(Body(7, 3, 4,  -3*np.cos(np.pi / 4), -1*np.cos(np.pi / 4),h=step))
#g.add_body(Body(3, 4, 5, -1*np.cos(np.pi / 4), -2*np.cos(np.pi / 4),h=step))
#g.add_body(Body(3333,-9, -4, 0.1,0.1,h=step))
#g.add_body(Body(100, -7.5, -5.2, 3*np.cos(np.pi / 4), 1*np.cos(np.pi / 4),h=step))
#g.add_body(Body(32, -10, -11,  3*np.cos(np.pi / 4), 1*np.cos(np.pi / 4),h=step))
#g.add_body(Body(1100, -5, -4,  3*np.cos(np.pi / 4), 1*np.cos(np.pi / 4),h=step))
#g.add_body(Body(32, -4, -7,  3*np.cos(np.pi / 4), 1*np.cos(np.pi / 4),h=step))



a = uniform(2,10)
step = 0.1
g = Ground()

g.add_body(Body(100000, -1,-15 ,-0.00001*np.cos(np.pi / 4), 0.0001*np.cos(np.pi / 4),h=step))
g.add_body(Body(10000, -6, -4,1*np.cos(np.pi / 4), 1*np.cos(np.pi / 4),h=step))


for i in range(150):
    x1 = uniform(-25,25)
    x2 = uniform(-20,20)
	m  =  uniform(100,1000)
    g.add_body(Body(1000, x1,x2 ,-0.01*np.cos(np.pi / 4), 0.0001*np.cos(np.pi / 4),h=step))
    #g.add_body(Body(100, -6, -4,1*np.cos(np.pi / 4), 1*np.cos(np.pi / 4),h=step))
    
g.add_body(Body(5000, 45,45, 3, -2*np.cos(np.pi*(v1/45)),h=step))    


for i in range(150):
    x1 = uniform(-30,45)
    x2 = uniform(-20,20)
	m  =  uniform(100,1000)
    g.add_body(Body(1000, x1,x2 ,-0.01*np.cos(np.pi / 4), 0.0001*np.cos(np.pi / 4),h=step))
    #g.add_body(Body(100, -6, -4,1*np.cos(np.pi / 4), 1*np.cos(np.pi / 4),h=step))



g.calculate(r=2000)
   
    


fig = plt.figure(figsize=(6, 6))
fig = plt.figure(figsize=(6, 6))

u = lambda t, x, y: 0
v = lambda t, x, y: -10
#
# point.add_force(f)
# z = point.calculate_radius_vector(20 * np.cos(np.pi / 4), +50 * np.sin(np.pi / 4), n=700)
# plt.plot(z[:, 0], z[:, 1])
n = 500
size = int(g.get_size(n))
# print(size)
Writer = animation.writers['ffmpeg']
writer = Writer(fps=15, metadata=dict(artist='Me'), bitrate=1800)

anim = animation.FuncAnimation(plt.gcf(), g.update_HTML_animation, interval=1, fargs=(fig,), frames=n, blit=False)
anim.save('video/galaxy3213.mp4', writer=writer)
HTML(anim.to_html5_video())

