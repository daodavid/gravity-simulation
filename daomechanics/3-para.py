# -*- coding: utf-8 -*-
"""
Created on Tue Jun 11 17:31:28 2019

@author: David
"""

# -*- coding: utf-8 -*-
"""
Created on Tue Jun 11 17:10:16 2019

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
step = 0.01
g = Ground()


#g.add_body(Body(50000, 0,0 , 0.001, 0.00001 ,h=step))
for i in range(300):
    v1 = uniform(50,70)
    v2 =uniform(50,70)
    x1 = uniform(40,60)
    x2 =uniform(40,80)
    m = uniform(500,2000)
    g.add_body(Body(m, x1,x2 , np.cos(np.pi*(45/180))/5, np.cos(np.pi*(v1/180))/10 ,h=step))
    
    

for i in range(100):
    #v1 = uniform(-30,30)
    v2 = uniform(1,30)
    x1 = uniform(40,60)
    x2 =uniform(100,120)
    m  =  uniform(2000,5150)
    g.add_body(Body(m, x1,x2 , 4*np.cos(np.pi*(45/180))/5, 4*np.cos(np.pi*(v1/180) )/10,h=step))
    
for i in range(300):
     v1 = uniform(40,70)
     v2 =uniform(50,70)
     x1 = uniform(40,60)
     x2 =uniform(150,170)
     m = uniform(500,2000)
     g.add_body(Body(m, x1,x2 , np.cos(np.pi*(45/180))/5, np.cos(np.pi*(v1/180))/10,h=step))
    
g.calculate(r=3000)
   
    


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
Writer = animation.writers['ffmpeg']
writer = Writer(fps=15, metadata=dict(artist='Me'), bitrate=1800)

anim = animation.FuncAnimation(plt.gcf(), g.update_HTML_animation, interval=1, fargs=(fig,), frames=n, blit=False)
anim.save('video/3-paral.mp4', writer=writer)
HTML(anim.to_html5_video())