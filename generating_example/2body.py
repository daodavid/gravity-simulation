from mechanic.gravity import GravityField
from mechanic.gravity import Body 
import numpy as np


field = GravityField()
#field.add_body(Body(3, 2, -0.3, -1))

#field.add_body(Body(-15 ,5,-0.00001*np.cos(np.pi / 4), 0.0001*np.cos(np.pi / 4)))
#field.add_body(Body( 6, -4,1*np.cos(np.pi / 4), 1*np.cos(np.pi / 4)))
field.add_body(Body(1, 4,1*np.cos(np.pi / 4), 1*np.cos(np.pi / 4)))
field.add_body(Body( 5, 1, 1*np.cos(np.pi / 4), -1*np.cos(np.pi / 4)))



field.run(10, C = 0.001, number_frames=10,approx_error=1.5)
field.save_animation()