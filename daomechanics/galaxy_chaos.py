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



for i in range(20):
    v1 = uniform(50,45)
    v2 =uniform(50,45)
    x1 = uniform(40,80)
    x2 =uniform(40,130)
    m = uniform(1000,2000)
    g.add_body(Body(m, x1,0.1 , 3, np.cos(np.pi*(45/180)),h=step))

for i in range(100):
    v1 = uniform(50,45)
    v2 =uniform(50,45)
    x1 = uniform(40,80)
    x2 =uniform(40,130)
    m = uniform(100,500)
    g.add_body(Body(m, x1,0.1 , 3, np.cos(np.pi*(45/180)),h=step))    
g.add_body(Body(5000, 45,45, 3, -2*np.cos(np.pi*(v1/45))/100,h=step))    

for i in range(50):
    v1 = uniform(0,360)
    v2 = uniform(0,360)
    x1 = uniform(-25,25)
    x2 = uniform(-20,20)
    m  =  uniform(2000,2150)
    g.add_body(Body(m, x1,x2 , v1*np.cos(np.pi*(v1/180))/1000, v2*np.cos(np.pi*(v1/180) )/500,h=step))
g.add_body(Body(7000, 0,0, 0.0001,0.0001,h=step)) 	
    
for i in range(20):
    v1 = uniform(50,45)
    v2 =uniform(50,45)
    x1 = uniform(30,55)
    x2 =uniform(40,130)
    m = uniform(1000,2000)
    g.add_body(Body(m, x1,0.1 , 3, v2*np.cos(np.pi*(45/180)),h=step))

g.add_body(Body(5000, 45,45, 3, -100*np.cos(np.pi*(v1/45)) ,h=step))  	 
g.calculate(r=5000)
   
    


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
anim.save('video/galaxychaise.mp4', writer=writer)
HTML(anim.to_html5_video())

