
# Gravity simulation 
### Python module  for calculation and simulation of n-bodies interaction  under  the influence of  Gravity force.

  
<br> <br>
       
   <img height="500" width="500" src="https://daodavid.github.io/gravity-simulation/resources/gift-generated-examples/b-7.gif">
  <img height="500" width="500" src="https://daodavid.github.io/gravity-simulation/resources/gift-generated-examples/b-11.gif"> 
 <br> <br>
  <img height="500" width="500" src="https://daodavid.github.io/gravity-simulation/resources/gift-generated-examples/b-16.gif">    
  <IMG height="500" width="500" src="https://daodavid.github.io/gravity-simulation/resources/gift-generated-examples/b-100.gif"> 
  <br> <br>
  <img height="500" width="500" src="https://daodavid.github.io/gravity-simulation/resources/gift-generated-examples/201-b.gif">    
  <img height="500" width="500" src="https://daodavid.github.io/gravity-simulation/resources/gift-generated-examples/2550-examples.gif"> 
  <br> <br>   
  
### Installing : 
```
pip install gravity-simulation==1.0.0

```  
### Example : 

```
#random example together with one body bigger mass than others
from gravity_simulation.gravity import *

field.generate_random(15, mass=[20, 500], r=[-5, 5], velocity=[-5, 5], alpha=[0, 360])
field.add_body(Body(x0=0, y0=0,v_x=0, v_y=0, mass = 3000))

field.run(1300, C=0.01)
field.save_animation(frames=50,name='my_example',reduce_size_body=50,frames=150)

```
  

<h6 face="Times New Roma" size="2" color='#270336' >
<font face="Times New Roma" size="2" color='#270336' >
      &nbsp;&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp;&nbsp;My personal opinion is that the  Nympy is an incredible library and without it, The Python is nothing (just an easy programming language and so on), but with the Numpy, The  Python is able to solve serious processes involved a huge number of iterations. When the application was written in common Python then the results were quite bad, for example, when the number of bodies is 2000 and number of the iterations is  10000 the duration of the process takes about 2 days because of the app was useless now when the processes are vectorized with <mark>NumPy</mark> and <mark>Numba</mark> the execution time takes about 2 hours.
    </font>
</h6>
    
 
   
  


##### Barnes-Hut approach
<a href='https://github.com/daodavid/gravity-simulation/blob/BarnesHut_notes_and_implementatios/README.md'>Barnes Hut notes, implementation in progress, and some examples </a>
