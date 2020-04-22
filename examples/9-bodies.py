from gravity_simulation.gravity import *


field = GravityField()

field.add_body(Body(15, 6 , -np.cos(np.pi / 4)/100, 0.01*np.cos(np.pi / 4) ,mass=30))
field.add_body(Body(6, 6 , -np.cos(np.pi / 4)/100, 0.01*np.cos(np.pi / 4) ,mass=50))
field.add_body(Body(-3, 0 ,np.cos(np.pi / 4)/(10*20), np.cos(np.pi / 4)/(10*20),mass=1500))
field.add_body(Body(-6, -6 , -0.01*np.cos(np.pi / 4)/100, -0.001*np.cos(np.pi / 4) ,mass=60))
field.add_body(Body(-10, 6 , -np.cos(np.pi / 4)/100, 0.01*np.cos(np.pi / 4) ,mass=100))
field.add_body(Body(-19, 0 ,np.cos(np.pi / 4)/(10*20), np.cos(np.pi / 4)/(10*20),mass=100))
field.add_body(Body(20, 6 , -np.cos(np.pi / 4)/100, 0.01*np.cos(np.pi / 4) ,mass=100))




field.run(47000, C=0.001)
field.save_animation(frames=100,figsize =(6,6),reduce_size_body=1)