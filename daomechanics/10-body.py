# -*- coding: utf-8 -*-
"""
Created on Thu Jun  6 14:57:40 2019

@author: David
"""

print("343!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
step = 0.01
g = Ground()
g.add_body(Body(1220, 1, 1, 0.01, 0.001,h=step))
g.add_body(Body(7, 3, 4,  -3*np.cos(np.pi / 4), -1*np.cos(np.pi / 4),h=step))
g.add_body(Body(3, 4, 5, -1*np.cos(np.pi / 4), -2*np.cos(np.pi / 4),h=step))
g.add_body(Body(3333,-9, -4, 0.1,0.1,h=step))
g.add_body(Body(100, -7.5, -5.2, 3*np.cos(np.pi / 4), 1*np.cos(np.pi / 4),h=step))
g.add_body(Body(32, -10, -11,  3*np.cos(np.pi / 4), 1*np.cos(np.pi / 4),h=step))
g.add_body(Body(1100, -5, -4,  3*np.cos(np.pi / 4), 1*np.cos(np.pi / 4),h=step))
g.add_body(Body(32, -4, -7,  3*np.cos(np.pi / 4), 1*np.cos(np.pi / 4),h=step))
#g.add_body(Body(32, -5, -5, -3*np.cos(np.pi / 4), -1*np.cos(np.pi / 4),h=0.1))
#g.add_body(Body(32, 3, 4,  -3*np.cos(np.pi / 4), -1*np.cos(np.pi / 4),h=0.1))
g.calculate(r=30000)

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
anim = animation.FuncAnimation(plt.gcf(), g.update_HTML_animation, interval=1, fargs=(fig,), frames=n, blit=False)
HTML(anim.to_html5_video())
plt.show()
