# vectorized computation
import numpy as np
from numba import float64, int64, f8, float32
from numba import guvectorize

# visualizing
import matplotlib.pyplot as plt
from matplotlib import animation, rc
from IPython.display import HTML
from mpl_toolkits.mplot3d import Axes3D
import mpl_toolkits.mplot3d.axes3d as p3
import pandas as pd

# common python 
from datetime import datetime
import warnings
from random import *
import sys

from numba import jit


class Body:
    ''' The class constructs the particle'''

    def __init__(self,  x0, y0, v_x, v_y, mass=30):
        '''
        Parameters:
        x0 : number
        x coordintate

        y : number
        y coordintate

        v_x : number
        velocity of x coord.

        v_y : number
        velocity of y coord.

        mass : number
        Mass of body

        '''
        # the moment coordinates
        self._mcoord = np.array([x0, y0])

        # the moment velocity
        self._mvelocity = np.array([v_x, v_y])

        self._mass = mass


def gravity_force(X_i, x_kj, M_i, M_kn, g=0.001, error_value=0.00001):
    ''''
    G_ik = sum_i g*(M_i.M_kn)* (r_i - r_k)/( (r_i1 - r_k1)^2 +(r_i2 - r_k2)^2 )
    G_i = S_i g.m.M(r_i - r_k)/(|r_i - r_k|^2)

    The core method using for calculation of force Gravity
    on one particle. The force is the sum of all forces coming from other particles

    This method calculates gravity force which acts on particle X_i.
    The force G is a sum of all forces producing from every particle.

    The method is written in NumPy thus it is  vectorized in order to achieve the highest performance

    Parameters :

        X_i  : ndarray [ , ]
        radius vector X_i = [x_ij]
        example :
         X_1 = [x_10,x_11] = [x(axis), y(axis)]

        x_kj : ndarray
        matrix of all coords exclude X_i
        x_kj= [ [x_10, x_11 ], [..., ... ] , [x_k0,x_k1] ]

        g : number 
        gravity constant 

        error_value : float
        special parameter setting  for fixing of  problem in case when the modul |r|
        tends to zero then the F tend to infinity and the model is broken (in real world this cannot happens)
        the error value is the min distance in which the bodies interact one each other 
        with the same constant force in order to prevent Infinity values.
        when this value is aachieve the method will show RuntimeWarning

    Return :
        Sum of all  gravity forces coming from particles x_kj wich acts on particle X_i

    '''
    # prevent calculation of force of body respect to itself
    index1, index2 = np.where(x_kj[:, 0] == X_i[0])[
        0], np.where(x_kj[:, 1] == X_i[1])[0]
    if ((index1 == index2).any()):
        x_kj = np.delete(x_kj, index1, axis=0)
        M_kn = np.delete(M_kn, index1)

    # dr matrix contain all delta elemes [[x_i0 - x_10, x_i1 - x_i1],[...,...],[x_i0 - x_k0, x_i1- x_k1]]
    dr_kj = x_kj - X_i  #
    # return [(x_i0-x_k0)^2,(x_i1-x_k1)^2]
    mod_dr_kj = dr_kj**2
    # return [sum_k (x_i0-x_k0)^2, sum_k (x_i1-x_k1)^2]
    mod_dr_k = np.sum(mod_dr_kj, axis=1)

    # when |dr| --> 0 then F--> infinity
    error_value = 0.0000001
    if (mod_dr_k < error_value).any():
        message = '|dr|, |dr|-->0 , , there for the dr has been repalced by configured error value {}  '.format(
            error_value)
        mod_dr_k[mod_dr_k < error_value] = error_value
        if x_kj.shape[0] > 2:
            warnings.showwarning(
                message, filename='gravity.py', lineno=135, category=RuntimeWarning)

    mod_dr_k = mod_dr_k.reshape(-1, 1)
    M_kn = M_kn.reshape(-1, 1)

    G = g*M_i*M_kn*(dr_kj/mod_dr_k)
    sum_force = np.sum(G, axis=0)
    return sum_force


@guvectorize(["float64[:, :],  float64[:] ,float64[:, :]"], "(n, m), (n) ,() -> (n, m)", nopython=False, fastmath=True, forceobj=True)
def acc(x_ij, M_i, out=None):
    # G = 6.674×10−8
    G = 0.1
    n = x_ij.shape[0]

    # if (n,)==M_i.shape:
    #M_i = M_i.reshape(-1,1)
    # print(M_i.shape)

    for i in range(x_ij.shape[0]):
        acc = 0
        # sepate particles
        X_i = x_ij[i]
        x_kj = np.delete(x_ij, i, axis=0)
        m = M_i[i]
        m_k = np.delete(M_i, i).reshape(-1, 1)

        # dr matrix contain all delta elemenets [[x_i0 - x_10, x_i1 - x_i1],[...,...],[x_i0 - x_k0, x_i1- x_k1]]
        dr_kj = x_kj - X_i

        # [(x_i0-x_k0)^2,(x_i1-x_k1)^2]
        mod_dr_kj = dr_kj**2
        #[sum_k (x_i0-x_k0)^2, sum_k (x_i1-x_k1)^2]
        mod_dr_k = np.sum(mod_dr_kj, axis=1)

        # when |dr| --> 0 then F--> infinity
        error_value = 0.001
        if (mod_dr_k < error_value).any():
            #message = '|dr|, |dr|-->0 , , there for the dr has been repalced by configured error value {}  '.format(error_value)
            mod_dr_k[mod_dr_k < error_value] = error_value
            #print(message)

        # if x_kj.shape[0] > 2 :
            # warnings.showwarning(
            # message, filename='gravity.py', lineno=135, category=RuntimeWarning)

        mod_dr_k = mod_dr_k.reshape(-1, 1)
        #M_kn = M_kn.reshape(-1, 1)
        F = G*m*m_k*(dr_kj/mod_dr_k)

        out[i] = np.sum(F, axis=0)*(1/m)


class GravityField:

    '''The class holds all bodies and provide its updatin in time.

    Args :
      x_cordinates : keeps the evolution of all bodies coordinates on the X axis through iterations
      y_cordinates : keeps the evolution of all bodies coordinates on the Y axis through iterations

    Attributes: 
    add_body(Body) :  adding new body on the field
    run() :  start the process of calculation and updating of  corrdinates of Bodies
    save_animation() : creates an animation mp4

    Example : 

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

    '''

    def __init__(self, integratin_setp=0.1, G=0.01):
        # gravity constant
        self.g = G

        self.h = integratin_setp
        # curent coordinates and velocity of all bodies
        self._mcoords = np.array([])  # [id,x,y]
        self._mvelocity = np.array([])  # [id,v_x,v_y]

        # all  x cordinates for all  particule
        self.x_cordinates = np.array([])
        # all y cordinat for all particlues in all time  [ , ]
        self.y_cordinates = np.array([])
        self._masses = np.array([])
        self._force = np.array([])

    def add_body(self, b):

        if self._mcoords.size != 0:
            self._mcoords = np.append(self._mcoords, [b._mcoord], axis=0)
            self._mvelocity = np.append(
                self._mvelocity, [b._mvelocity], axis=0)
        else:
            self._mcoords = np.array([b._mcoord])
            self._mvelocity = np.array([b._mvelocity])

        self._masses = np.append(self._masses, b._mass)

        if self.x_cordinates.size != 0:
            self.x_cordinates = np.append([self.x_cordinates], b._mcoord[0])
            self.y_cordinates = np.append([self.y_cordinates], b._mcoord[1])
        else:
            self.x_cordinates = np.array(b._mcoord[0])
            self.y_cordinates = np.array(b._mcoord[1])

    def __leapFrog_step1(self):
        """ leap frog step 1 
            x = x + v_1*self.h/2
         """

        #self.x1 = self.x1 + self.v1 * self.h / 2
        #self.x2 = self.x2 + self.v2 * self.h / 2
        self._mcoords = self._mcoords + self._mvelocity*(self.h/2)

        # moment state
        x = self._mcoords[:, 0]
        y = self._mcoords[:, 1]

        # insert new cordinates
        if self.x_cordinates.shape == x.shape:
            self.x_cordinates = np.array([self.x_cordinates, x])
            self.y_cordinates = np.array([self.y_cordinates, y])
        else:
            self.x_cordinates = np.append(self.x_cordinates, [x], axis=0)
            self.y_cordinates = np.append(self.y_cordinates, [y], axis=0)

    def __leapFrog_step2(self):
        '''leapFrog algorithm step 2
           v_{1/2} = v_1 + a(x_{1/2})*h
        '''
        a = acc(self._mcoords, self._masses)
        self._mvelocity = self._mvelocity + a*self.h

    def run(self, n, C=0.01, approx_error=0.00001):
        '''  Starting point 

        Parametes :
          n  : number
          number of itetaion
          C  : float number
          integration step using in leap from integration process

          approx_error : float 
          very special setting look at method calculate_gravity

        Return : 
          X,Y pandas data frames 
          returns the  evolution  of all coordinates 
          of X, Y in time

        Еxample :
         '''

        self.h = C
        self.number_iter = n
        #self.number_frames = number_frames
        #self.frame_step = int(n/number_frames)
        self.approx_error = approx_error
        self.number_of_bodies = self._mvelocity.shape[0]
        self.error = approx_error
        self.number_iteration = n

        print('start calculation {}'.format(datetime.now()))

        for i in range(self.number_iteration):
            self.__leapFrog_step1()
            self.__leapFrog_step2()

            #print out progress bar
            p = ((i+1)/self.number_iteration)*100
            sys.stdout.write("\r%d%%" % p)
            sys.stdout.flush()

        print('   calculation  completed :{}'.format(datetime.now()))

        self.__save__()
        return self.__result__()

    def __save__(self):
        columns = ['body_' + str(i) for i in range(self.x_cordinates[0].size)]
        self.X_cordinates = pd.DataFrame(self.x_cordinates, columns=columns)
        self.Y_cordinates = pd.DataFrame(self.y_cordinates, columns=columns)
        print('calculation complete succsefuly')

    def __result__(self):

        return self.X_cordinates, self.Y_cordinates

    def __update_anim__(self, i, arg):
        arg.clf()
        k = self.frame_step*i

        linewidth = 1/self.number_of_bodies

        X, Y = self.x_cordinates, self.y_cordinates
			
        body_size = self.size_body*self._masses/self.number_of_bodies

        x_plot, y_plot = X[k], Y[k]
        plt.scatter(x_plot, y_plot, color='skyblue', s=body_size)
        #plt.plot(X, Y, color='skyblue', linewidth=linewidth)
        title = plt.title(self.title)
        plt.setp(title, color='skyblue')

    def save_animation(self, frames=50, name=None, **kwargs):
        '''
        Save animation in mp4

        Parameters :
          frames : int
          the number of frames wich  will be genarated

          name : str
          name of the file 

          **kwargs 
            can be passed some plot settin 
            as title ,figsize ,reduce_size_body

          example :

         save_animation(frames = 100 , name = 'my_animation' ,figsize=(6, 6),
                        reduce_size_body=20,title='N body generation')


        '''

        N = self._mcoords.shape[0]
        self.title = 'gravity simulation number of bodies = {}'.format(N)
        self.show_trajectory = True
        self.size_body = 10
        figsize = (6, 6)
        for key, value in kwargs.items():
            if key == 'title':
                self.title = value
            elif key == 'figsize':
                figsize = value
            elif key == 'size_body':
                self.size_body = value

        fig = plt.figure(figsize=figsize)
        plt.style.use('dark_background')

        self.frame_step = int(self.number_iter/frames)

        Writer = animation.writers['ffmpeg']
        writer = Writer(fps=15, metadata=dict(artist='Me'), bitrate=1800)

        anim = animation.FuncAnimation(plt.gcf(), self.__update_anim__, interval=1, fargs=(
            fig,), frames=frames, blit=False)

        if name is None:
            random_name = str(np.random.randint(0, 100))
            name = ('exm.{} ,b_{}, itr={}').format(
                random_name, N, self.number_iteration)

        name = name+'.mp4'
        print('start rendering {}'.format(datetime.now()))
        anim.save(name, writer=writer)
        print('end rendering {}'.format(datetime.now()))
        # HTML(anim.to_html5_video())  ### for notebooks

    def generate_random(self, N_bodies, mass=[20, 500], r_x=[-5, 5],r_y=[-5, 5],r_0=0, velocity=[-5, 5], alpha=[0, 360]):
        for i in range(N_bodies):

            #pass
            v = np.random.randint(velocity[0], velocity[1])
            a = np.random.randint(alpha[0], alpha[1])
            radius_x = np.random.randint(r_x[0], r_x[1])
            radius_y = np.random.randint(r_y[0], r_y[1])
            m = np.random.randint(mass[0], mass[1])
            self.add_body(Body(r_0 + radius_x*np.cos((a/360)*2*np.pi),r_0+ radius_y*np.sin((a/360)*2*np.pi)
                              , v*np.cos((a/360)*2*np.pi), v*np.sin((a/360)*2*np.pi), mass=m))


# field = GravityField()
# # v = (0,10)
# # print(v[1])
# field.generate_random(15,mass=[100,500],r = [-5,5])
# field.add_body(Body(x0=0,y0=0,v_x=0,v_y=0,mass = 3000))
# v = [1,10]
# v = np.random.randint(v[0],v[1])
# field.run(1300,C = 0.01)
# field.save_animation(reduce_size_body=50,frames=150)
field = GravityField()


field.generate_random(2000, mass=[100, 900], r_x=[0, 2000], r_y=[0, 6000], r_0=-1000, alpha=[0, 360],velocity=[0,500])
field.add_body(Body(x0=0,y0=0,v_x=100,v_y=100,mass=9999))


field.generate_random(2000, mass=[100, 900], r_x=[0, 1000], r_y=[0, 6000], alpha=[0, 360],r_0=19000,velocity=[0,500])
field.add_body(Body(x0=1000,y0=1000,v_x=100,v_y=100,mass=9999))




#field.generate_random(2100, mass=[1000, 2000], r_x=[-500, 2000], r_y=[-1000, 0],r_0=15000,velocity=[0,1500], alpha=[0, 360])





field.run(4000, C=0.1)
field.save_animation( frames=150, title='galaxy',size_body=5)  #size_body=100
