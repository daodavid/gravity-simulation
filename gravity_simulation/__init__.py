"""Gravity simulation API

The module has an API for calculation and visualization of N-bodies 
interaction under gravity forces

Example:
     
    from gravity_simulation.gravity import GravityField
    from gravity_simulation.gravity import Body
    
    field = GravityField()
        field.add_body(Body(15, 6, -np.cos(np.pi / 4)/100,
                        0.01*np.cos(np.pi / 4), mass=30))
        field.add_body(Body(6, 6, -np.cos(np.pi / 4)/100,
                        0.01*np.cos(np.pi / 4), mass=50))
        field.add_body(Body(-3, 0, np.cos(np.pi / 4)/(10*20),
                        np.cos(np.pi / 4)/(10*20), mass=1500))
        field.add_body(Body(-6, -6, -0.01*np.cos(np.pi / 4) /
                        100, -0.001*np.cos(np.pi / 4), mass=60))
        field.add_body(Body(-10, 6, -np.cos(np.pi / 4)/100,
                        0.01*np.cos(np.pi / 4), mass=100))
        field.add_body(Body(-19, 0, np.cos(np.pi / 4)/(10*20),
                        np.cos(np.pi / 4)/(10*20), mass=100))
        field.add_body(Body(-20, -6, -0.01*np.cos(np.pi / 4) /
                        100, -0.001*np.cos(np.pi / 4), mass=60))
        field.add_body(Body(30, 6, -np.cos(np.pi / 4)/100,
                        0.01*np.cos(np.pi / 4), mass=100))
        
        X, Y = field.run(17000, C=0.01)
        field.save_animation(frames=80, figsize=(6, 6), reduce_size_body=5)
        $ python example_google.py

The implementation is fully vectorized in order to achieve high performance.

Attributes:
   gravity.GravityField : class
   gravity.Body : class
   gravity.calculate_gravity :method 

   https://github.com/daodavid/gravity-simulation

"""