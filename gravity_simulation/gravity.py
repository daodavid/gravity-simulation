# vectorized computation
import numpy as np

# libs for visualizing
import matplotlib.pyplot as plt
from matplotlib import animation, rc
from IPython.display import HTML
from mpl_toolkits.mplot3d import Axes3D
import mpl_toolkits.mplot3d.axes3d as p3
import pandas as pd

# common python libs
from datetime import datetime
import warnings
from random import *


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



def calculate_gravity(X_i, x_kj, M_i, M_kn, g=0.001, error_value=0.00001):
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

    # dr matrix contain all delta elemes [[x_i0 - x_10, x_i1 - x_i1],[...,...],[x_i0 - x_k0, x_i1- x_k1]]
    dr_kj = x_kj - X_i  #
    mod_dr_kj = dr_kj**2
    mod_dr_k = np.sum(mod_dr_kj, axis=1)

    # when |dr| --> 0 then F--> infinity
    if (mod_dr_k < error_value).any():
        message = '|dr|, |dr|-->0 , , there for the dr has been repalced by configured error value {}  '.format(
            error_value)
        mod_dr_k[mod_dr_k < error_value] = error_value
        warnings.showwarning(
            message, filename='gravity.py', lineno=135, category=RuntimeWarning)

    mod_dr_k = mod_dr_k.reshape(-1, 1)
    M_kn = M_kn.reshape(-1, 1)

    G = g*M_i*M_kn*(dr_kj/mod_dr_k)

    return np.sum(G, axis=0)


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

        # track cordinate in time
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

        for i in range(self._mcoords.shape[0]):
            all_codinates = np.delete(self._mcoords, i, 0)
            masses = np.delete(self._masses, i)
            force = calculate_gravity(
                self._mcoords[i, :], all_codinates, self._masses[i], masses, self.g, error_value=self.error)

            M = self._masses[i]
            a = force/M
            self._mvelocity[i][0] = self._mvelocity[i][0] + a[0]*self.h
            self._mvelocity[i][1] = self._mvelocity[i][1] + a[1]*self.h
            #v = self._mvelocity[i] + a*self.h
            #v = v

    def run(self, n, C=0.01, approx_error=0.000001):
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
        self.approx_error = 1/10**approx_error
        self.number_of_bodies = self._mvelocity.shape[0]
        self.error = approx_error
        self.number_iteration = n

        print('start calculation {}'.format(datetime.now()))

        for _ in range(self.number_iteration):
            self.__leapFrog_step1()
            self.__leapFrog_step2()

        print('end calculation {}'.format(datetime.now()))

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

        c = self.reduce_size_body

        x_plot, y_plot = X[k], Y[k]
        plt.scatter(x_plot, y_plot, color='skyblue', s=self._masses/c)
        plt.plot(X, Y, color='skyblue', linewidth=linewidth)
        title = plt.title(self.title)
        plt.setp(title, color='skyblue')

    def save_animation(self, frames=80, name=None, **kwargs):
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
        self.reduce_size_body = 30
        figsize = (6, 6)
        for key, value in kwargs.items():
            if key == 'title':
                self.title = value
            elif key == 'figsize':
                figsize = value
            elif key == 'reduce_size_body':
                self.reduce_size_body = value

        fig = plt.figure(figsize=figsize)
        plt.style.use('dark_background')

        self.frame_step = int(self.number_iter/frames)

        Writer = animation.writers['ffmpeg']
        writer = Writer(fps=15, metadata=dict(artist='Me'), bitrate=1800)

        anim = animation.FuncAnimation(plt.gcf(), self.__update_anim__, interval=1, fargs=(
            fig,), frames=frames, blit=False)

        if name is None:
            random_name = str(np.random.randint(0, 100))
            name = ('exmaple_{},bodies_{}').format(random_name, N)

        name = name+'.mp4'
        print('start rendering {}'.format(datetime.now()))
        anim.save(name, writer=writer)
        print('end rendering {}'.format(datetime.now()))
        # HTML(anim.to_html5_video())  ### for notebooks
