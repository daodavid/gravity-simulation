from gravity_simulation.gravity import GravityField
from gravity_simulation.gravity import Body

field = GravityField()

field = GravityField()


field.generate_random(2000, mass=[100, 900], r_x=[0, 2000], r_y=[
                      0, 6000], r_0=-1000, alpha=[0, 360], velocity=[0, 500])
field.add_body(Body(x0=0, y0=0, v_x=100, v_y=100, mass=9999))


field.generate_random(2000, mass=[100, 900], r_x=[0, 1000], r_y=[0, 6000], alpha=[0, 360],r_0=19000,velocity=[0,500])
field.add_body(Body(x0=1000,y0=1000,v_x=100,v_y=100,mass=9999))



#field.generate_random(2100, mass=[1000, 2000], r_x=[-500, 2000], r_y=[-1000, 0],r_0=15000,velocity=[0,1500], alpha=[0, 360])


field.run(2500, C=0.3)
field.save_animation(frames=150, title='galaxy', size_body=5)  # size_body=100