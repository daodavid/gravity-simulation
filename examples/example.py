
field = GravityField()


# field.add_body(Body(15, 6 , -np.cos(np.pi / 4)/100, 0.01*np.cos(np.pi / 4) ,mass=30))
# field.add_body(Body(6, 6 , -np.cos(np.pi / 4)/100, 0.01*np.cos(np.pi / 4) ,mass=50))
# field.add_body(Body(-3, 0 ,np.cos(np.pi / 4)/(10*20), np.cos(np.pi / 4)/(10*20),mass=1500))
# field.add_body(Body(-6, -6 , -0.01*np.cos(np.pi / 4)/100, -0.001*np.cos(np.pi / 4) ,mass=60))
# field.add_body(Body(-10, 6 , -np.cos(np.pi / 4)/100, 0.01*np.cos(np.pi / 4) ,mass=100))
# field.add_body(Body(-19, 0 ,np.cos(np.pi / 4)/(10*20), np.cos(np.pi / 4)/(10*20),mass=100))
# field.add_body(Body(-20, -6 , -0.01*np.cos(np.pi / 4)/100, -0.001*np.cos(np.pi / 4) ,mass=60))
field.add_body(Body(30, 6 , -np.cos(np.pi / 4)/100, 0.01*np.cos(np.pi / 4) ,mass=100))

field.add_body(Body(-15, -20 , np.cos(np.pi / 4)/(10**100), np.cos(np.pi / 4)/10**100 ,mass=100))



# for i in range(10):
#     v = uniform(0,0.1)

#     alpha = uniform(0,360)
#     x1 = uniform(-20,200)
#     x2 = uniform(-20,200)
#     m = uniform(20,600)   
#     field.add_body(Body(x1, x2 , -v*np.cos((alpha/360)*np.pi / 4)/100, v*np.sin((alpha/360)*np.pi) ,mass=m))    

# for i in range(2):
#     v = uniform(0,0.1)

#     alpha = uniform(0,360)
#     x1 = uniform(-20,200)
#     x2 = uniform(-20,200)
#     m = uniform(11000,15000)   
#     field.add_body(Body(x1, x2 , -v*np.cos((alpha/360)*np.pi / 4)/100, v*np.sin((alpha/360)*np.pi) ,mass=m))        

field.run(100, C=0.1, number_frames=100, approx_error=0.000001)
field.save_animation()
