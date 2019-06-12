# -*- coding: utf-8 -*-
"""
Created on Tue Jun 11 17:25:46 2019

@author: David
"""
from gravity import *
import matplotlib.pyplot as plt
from matplotlib import animation, rc
from IPython.display import HTML
from random import *
import numpy as np
step = 0.01
g = Ground()




g.add_body(Body(9000000, 0,0 , 0.001, 0.00001 ,h=step))
 
    
for i in range(200):
    v1 = uniform(0,360)
    v2 = uniform(0,360)
    x1 = uniform(20,100)
    x2 =uniform(20,50)
    m = uniform(1000,10000)
    g.add_body(Body(m, x1,x2 , v1*np.cos(np.pi*(v1/180))/10000, v2*np.cos(np.pi*(v1/180))/10000 ,h=step))

g.add_body(Body(90000, 40,40 , -0.001, -0.00001 ,h=step))	
	
for i in range(200):
    v1 = uniform(0,360)
    v2 = uniform(0,360)
    x1 = uniform(-100,-20)
    x2 =uniform(-50,-20)
    m = uniform(1000,10000)
    g.add_body(Body(m, x1,x2 , v1*np.cos(np.pi*(v1/180))/10000, v2*np.cos(np.pi*(v1/180))/10000 ,h=step))	

g.add_body(Body(90000, -40,-40 , 0.001, 0.00001 ,h=step))		

g.add_body(Body(100000, 10,10 , 0.0001, 0.000001 ,h=step))   
g.add_body(Body(200000, -20,20 , 0.0001, -0.000001 ,h=step)) 
g.calculate(r=2000)

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
anim.save('video/g3-galaxy.mp4', writer=writer)
HTML(anim.to_html5_video())