from gravity_simulation.gravity import GravityField
from gravity_simulation.gravity import Body

field = GravityField()
# v = (0,10)
# print(v[1])
field.generate_random(500, mass=[1000,3000], r_x=[-120,-80], r_y=[-120,-80])
field.generate_random(500, mass=[1000,3000], r_x=[80,120], r_y=[80,120])

field.generate_random(2500,mass=[100,500], r_x = [-120,120], r_y = [-120,120])


field.add_body(Body(x0=-90,y0=-90,v_x=0,v_y=0,mass = 15000))


field.add_body(Body(x0=90,y0=90,v_x=0,v_y=0,mass = 15000))




field.run(500,C = 0.1)
field.save_animation(reduce_size_body=200,frames=200,title='galaxy')
