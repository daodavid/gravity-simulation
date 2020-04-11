from gravity_simulation.gravity import *


field = GravityField()

field = GravityField()



field.run(17000, C=0.01)
field.save_animation(frames=80,figsize =(6,6),reduce_size_body=5)