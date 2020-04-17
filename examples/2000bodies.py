from gravity_simulation.gravity import GravityField
from gravity_simulation.gravity import Body

field = GravityField()
# v = (0,10)
# print(v[1])
field.generate_random(3500,mass=[100,500],r = [-40,40])


field.add_body(Body(x0=22,y0=22,v_x=0,v_y=0,mass = 15000))


field.add_body(Body(x0=-22,y0=-22,v_x=0,v_y=0,mass = 15000))




field.run(1300,C = 0.01)
field.save_animation(reduce_size_body=200,frames=200,title='galaxy')