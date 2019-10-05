from random import *
import numpy as np
from daomechanics.gravity import *
g = Ground()
"""

Example of two galaxy 
"""

step = 0.1
# Generate random particles
for i in range(250):
    v1 = uniform(45,48)
    v2 = uniform(45,48)
    x1 = uniform(150,0)
    x2 = uniform(130,0)
    m = uniform(100,2000)   
    g.add_body(Body(m, x1,x2 ,-3*np.cos(np.pi / (v1/180)), -5*np.cos(np.pi / (v2/180)),h=step))
    
    

  
g.add_body(Body(9000000, 0,0,-np.cos(np.pi / 4),-np.cos(np.pi / 4),h=0.001)) 





for i in range(250):
    v1 = uniform(45,48)
    v2 = uniform(45,48)
    x1 = uniform(0,-120)
    x2 = uniform(0,-120)
    m = uniform(100,2000)   
    g.add_body(Body(m, x1,x2 ,-3*np.cos(np.pi / (v1/180)), -5*np.cos(np.pi / (v2/180)),h=step))
    
    

    
for i in range(250):
    v1 = uniform(45,48)
    v2 = uniform(45,48)
    x1 = uniform(-150,-180)
    x2 = uniform(100,-180)
    m = uniform(100,2000)   
    g.add_body(Body(m, x1,x2 ,-3*np.cos(np.pi / (v1/180)), -5*np.cos(np.pi / (v2/180)),h=step))
  
g.add_body(Body(9000000, -170,0,3,0,h=0.001)) 

g.calculate(r=500)

fig = plt.figure(figsize=(6, 6))
fig = plt.figure(figsize=(6, 6))

u = lambda t, x, y: 0
v = lambda t, x, y: -10
n = 300
size = int(g.get_size(n))

Writer = animation.writers['ffmpeg']
writer = Writer(fps=15, metadata=dict(artist='Me'), bitrate=1800)

anim = animation.FuncAnimation(plt.gcf(), g.update_HTML_animation, interval=1, fargs=(fig,), frames=n, blit=False)
anim.save('video2/galaxy2s.mp4', writer=writer)
HTML(anim.to_html5_video())