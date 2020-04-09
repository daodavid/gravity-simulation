# N-bodies problem




instalation :
  git clone 
 in folder porject 
  pip install .
    from mechanic.gravity import GravityField


##### The only way to solve force iteraction between n bodies ,where n>2 is numerical approach.It can not be find the solution with common analitical itegration.The solution involve complexity O(n)=2∗k.h.n2 number of itergration step ,where h = itegration step or time step,k count of itegration and k.v=t t-time,The multiplier 2 is because that is second order DU.In this paper we will see how this complexity can be reduced to O(n log n) or O(n) by using Barnes-Hut and Leapfrogs algorithms
 <font size="4" face = "Times New Roma" color='#3f134f' >
  <a color='blue' href="https://nbviewer.jupyter.org/github/daodavid/Barnes-Hut-Algorithm_Nbodies_Problem/blob/gh-pages/n-bodies-project.ipynb">N-bodies problem and Barnes-Hut algorithm 
</a>
</font>
![](https://github.com/daodavid/Barnes-Hut-Algorithm_Nbodies_Problem/blob/master/video/8-bodies.gif)

![](https://github.com/daodavid/Barnes-Hut-Algorithm_Nbodies_Problem/blob/master/video/3-bodies.gif)

![alt text](https://github.com/Daodavid93/Barnes-Hut-Algorithm_Nbodies_Problem/blob/master/sources/18_1.jpg)

