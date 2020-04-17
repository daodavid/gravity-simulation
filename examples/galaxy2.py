from gravity_simulation.gravity import GravityField
from gravity_simulation.gravity import Body

field = GravityField()
# v = (0,10)
# print(v[1])

#galaxy1 
field.generate_random(20,mass=[600,3000],r = [-10000,-5000])
field.add_body(Body(x0=-1400,y0=-900,v_x=0,v_y=0,mass = 15000))
field.generate_random(1000,mass=[100,300],r = [-10000,-5000])

#galaxy2 
field.generate_random(20,mass=[1000,3000],r = [1600,3000])
field.add_body(Body(x0=1200,y0=1200,v_x=0,v_y=0,mass = 15000))
field.generate_random(1000,mass=[100,500],r = [1600,3000])










field.run(8000,C = 0.1)
field.save_animation(reduce_size_body=300,frames=150,title='galaxy')