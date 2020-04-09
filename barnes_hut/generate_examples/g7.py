



"""
Created on Thu Jun 13 20:09:15 2019

@author: David
"""

import matplotlib.pyplot as plt
from matplotlib import animation, rc
from IPython.display import HTML
from random import *
import numpy as np
from daomechanics.gravity import *
    
    
print('helsslo')
g = Ground()


step = 0.1
    
# generate 300 particles with speed velocity  40-  48
for i in range(300):
    v1 = uniform(40,48)
    v2 = uniform(45,48)
    x1 = uniform(-200,10)
    x2 = uniform(0,30)
    print('helsslo')
    m = uniform(100,400)   
    g.add_body(Body(m, x1,x2 ,0.4*np.cos(np.pi / (v1/180)), -0.5*np.cos(np.pi / (v2/180)),h=step))
  
g.add_body(Body(9000000, 40,5,0.04,-0.1,h=0.001))  
  

for i in range(300):
    v1 = uniform(40,48)
    v2 = uniform(45,48)
    x1 = uniform(200,10)
    x2 = uniform(0,-30)
    print('helsslo')
    m = uniform(100,400)   
    g.add_body(Body(m, x1,x2 ,0.4*np.cos(np.pi / (v1/180)), -0.5*np.cos(np.pi / (v2/180)),h=step))
  
g.add_body(Body(9000000, 40,5,-0.04,0.1,h=0.001))  




for i in range(300):
    v1 = uniform(40,48)
    v2 = uniform(45,48)
    x1 = uniform(100,0)
    x2 = uniform(0,20)
    print('helsslo')
    m = uniform(100,400)   
    g.add_body(Body(m, x1,x2 ,-0.4*np.cos(np.pi / (v1/180)), -0.5*np.cos(np.pi / (v2/180)),h=step))
  
g.add_body(Body(9000000, 40,5,-0.04,-0.1,h=0.001))       

for i in range(400):
    v1 = uniform(40,48)
    v2 = uniform(45,48)
    x1 = uniform(-100,0)
    x2 = uniform(0,-10)
    print('helsslo')
    m = uniform(100,400)   
    g.add_body(Body(m, x1,x2 ,0.05*np.cos(np.pi / (v1/180)), 0.5*np.cos(np.pi / (v2/180)),h=step))
     
  
g.add_body(Body(9000000, -50,-7,0.5,0.2,h=0.001))     

g.calculate(r=700)

fig = plt.figure(figsize=(6, 6))
fig = plt.figure(figsize=(6, 6))

u = lambda t, x, y: 0
v = lambda t, x, y: -10

n = 300
size = int(g.get_size(n))
# print(size)
Writer = animation.writers['ffmpeg']
writer = Writer(fps=15, metadata=dict(artist='Me'), bitrate=1800)

anim = animation.FuncAnimation(plt.gcf(), g.update_HTML_animation, interval=1, fargs=(fig,), frames=n, blit=False)
anim.save('video2/galaxy-g7-great-g.mp4', writer=writer)
HTML(anim.to_html5_video())