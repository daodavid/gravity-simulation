from gravity_simulation.gravity import *




for i in range(100):
    for j in range(30):
        j = j+2
        field = GravityField()
        field.generate_random(j, mass=[1000, 3000], r=[-50, 50])
        field.run(157000, C=0.003)
        field.save_animation(reduce_size_body=100, frames=150)
