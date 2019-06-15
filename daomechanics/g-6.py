# -*- coding: utf-8 -*-
"""
Created on Fri Jun 14 08:41:33 2019

@author: David
"""

# -*- coding: utf-8 -*-
"""
Created on Thu Jun 13 20:10:27 2019

@author: David
"""

# -*- coding: utf-8 -*-
"""
Created on Thu Jun 13 20:09:15 2019

@author: David
"""

import matplotlib.pyplot as plt
from matplotlib import animation, rc
from IPython.display import HTML
from random import *
import numpy as np
from gravity import *
    
    
print('helsslo')
g = Ground()


step = 0.1
    


for i in range(200):
    v1 = uniform(40,48)
    v2 = uniform(45,48)
    x1 = uniform(50,0)
    x2 = uniform(-30,0)
    print('helsslo')
    m = uniform(100,400)   
    g.add_body(Body(m, x1,x2 ,0.02*np.cos(np.pi / (v1/180)), -0.03*np.cos(np.pi / (v2/180)),h=step))
  
g.add_body(Body(9000000, 40,-10,-0.04,1,h=0.001))     






for i in range(150):
    v1 = uniform(40,48)
    v2 = uniform(45,48)
    x1 = uniform(50,0)
    x2 = uniform(0,30)
    print('helsslo')
    m = uniform(100,400)   
    g.add_body(Body(m, x1,x2 ,-0.02*np.cos(np.pi / (v1/180)), -0.03*np.cos(np.pi / (v2/180)),h=step))
  
g.add_body(Body(9000000, 40,10,-0.04,-1,h=0.001))      

for i in range(200):
    v1 = uniform(40,48)
    v2 = uniform(45,48)
    x1 = uniform(-50,0)
    x2 = uniform(0,-30)
    print('helsslo')
    m = uniform(100,400)   
    g.add_body(Body(m, x1,x2 ,0.1, 0.3,h=step))
     
  
g.add_body(Body(9000000, -50,-30.01,0.04,0,h=0.001))  

g.calculate(r=500)

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
Writer = animation.writers['ffmpeg']
writer = Writer(fps=15, metadata=dict(artist='Me'), bitrate=1800)

anim = animation.FuncAnimation(plt.gcf(), g.update_HTML_animation, interval=1, fargs=(fig,), frames=n, blit=False)
anim.save('video2/galaxy-dssda.mp4', writer=writer)
HTML(anim.to_html5_video())