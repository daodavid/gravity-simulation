# most importent lib
import numpy as np

# visualizing
import matplotlib.pyplot as plt
from matplotlib import animation, rc
from IPython.display import HTML
from mpl_toolkits.mplot3d import Axes3D
import mpl_toolkits.mplot3d.axes3d as p3

# representing data
import pandas as pd
# common python libs
from datetime import datetime
import warnings
from random import *


class Body:
    '''
    just the class constructs the particle
    '''

    def __init__(self,  x0, y0, v_x, v_y, mass=1):
        '''
        Parameters

        '''
        # ndarray current coordinates
        self._mcoord = np.array([x0, y0])
        # current current velocity
        self._mvelocity = np.array([v_x, v_y])
        # mass
        self._mass = mass


class GravityField:

    '''
      bla bla bla !!!!

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

    @classmethod
    def calculate_gravity(cls, X_i, x_kj, M_i, M_kn, g=0.001, error_value=0.01):
        ''''
        G_ik = sum_i g*(M_i.M_kn)* (r_i - r_k)/( (r_i1 - r_k1)^2 +(r_i2 - r_k2)^2 )
        G_i = S_i g.m.M(r_i - r_k)/(|r_i - r_k|^2)

        The core of implementation.
        This method calculates gravity force which acts on particle X_i.
        The force G is a sum of all forces producing from every particle.

        The method is written in NumPy vectorized in order to achieve the highest performance

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
            special setting  for fixing a problem related to ,
            when |r| tends to zero (in real world this cannot happens)

        Return :
            Sum of all  gravity forces wich acts on particle X_i

        '''

        # dr matrix contain all delta elemes [[x_i0 - x_10, x_i1 - x_i1],[...,...],[x_i0 - x_k0, x_i1- x_k1]]
        dr_kj = x_kj - X_i  #
        mod_dr_kj = dr_kj**2
        mod_dr_k = np.sum(mod_dr_kj, axis=1)

        #!!! note since when |dr| --> 0 then F--> infinity
        # and this is inposible for real world therefore ,to keep our model right we will handle that problem
        if (mod_dr_k < error_value).any():
            message = '|dr|, |dr|-->0 , , there for the dr has been repalced by configured error value {}  '.format(
                error_value)
            mod_dr_k[mod_dr_k < error_value] = error_value
            warnings.showwarning(
                message, filename='gravity.py', lineno=135, category=RuntimeWarning)

        mod_dr_k = mod_dr_k.reshape(-1, 1)
        M_kn = M_kn.reshape(-1, 1)

        G = g*M_i*M_kn*(dr_kj/mod_dr_k)

        sum_force_of_all_particles = np.sum(G, axis=0)

        return sum_force_of_all_particles

    def leapFrog_step1(self):
        """
        leap frog step 1
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

    def leapFrog_step2(self):
        '''
        leapFrog algorithm step 2
        v_{1/2} = v_1 + a(x_{1/2})*h
        '''

        for i in range(self._mcoords.shape[0]):
            all_codinates = np.delete(self._mcoords, i, 0)
            masses = np.delete(self._masses, i)
            force = GravityField.calculate_gravity(
                self._mcoords[i, :], all_codinates, self._masses[i], masses, self.g, error_value=self.error)
            
            M = self._masses[i]
            a = force/M
            self._mvelocity[i][0] = self._mvelocity[i][0] + a[0]*self.h
            self._mvelocity[i][1] = self._mvelocity[i][1] + a[1]*self.h
            #v = self._mvelocity[i] + a*self.h
            #v = v

    def save(self):
        columns = ['body_' + str(i) for i in range(self.x_cordinates[0].size)]
        self.X_cordinates = pd.DataFrame(self.x_cordinates, columns=columns)
        self.Y_cordinates = pd.DataFrame(self.y_cordinates, columns=columns)
        print('calculation complete succsefuly')

    def run(self, n, C=0.1, number_frames=20, approx_error=0.01):
        '''
        parametes :
        n- number of iteration
        '''
        start = datetime.now()
        print('start:', str(start))

        self.h = C
        self.number_iter = n
        self.number_frames = number_frames
        self.frame_step = int(n/number_frames)
        self.approx_error = 1/10**approx_error
        self.number_of_bodies = self._mvelocity.shape[0]
        self.error = approx_error
        self.number_iteration = n 

        for i in range(self.number_iteration):
            self.leapFrog_step1()
            self.leapFrog_step2()

        self.save()
        end = datetime.now() - start
        print('all cal process {}'.format(end))

    def result(self):

        return self.X_cordinates, self.Y_cordinates

    def __repr__(self):
        return ''

    def update_anim(self, i, arg):
        ax = plt.gca()
        arg.clf()
        k = self.frame_step*i
        n_bodies = self.number_of_bodies
        linewidth = 1/self.number_of_bodies

        #x, y = self.X_cordinates, self.Y_cordinates
        X, Y = self.x_cordinates, self.y_cordinates

        #
        # for j in range(x.shape[1]):
        #     body = 'body_{}'.format(j)
        #

        #     if(self.show_trajectory) :
        #         plt.plot(np.array(x[body]), np.array(y[body]),color='red',linewidth=linewidth)
        #     plt.scatter(x[body][k], y[body][k],color='white')

        x_plot, y_plot = X[k], Y[k]
        plt.scatter(x_plot, y_plot, color='skyblue', s=self._masses/10)
        plt.plot(X, Y, color='skyblue', linewidth=linewidth)

        #q = plt.scatter(self.X_cordinates, self.Y_cordinates, color='indigo', linewidths=None)

        #plt.scatter(0, 0, color='red', linewidths=0.0001)
        #plt.scatter(-10, 10, color='red', linewidths=0.0001)
        #plt.scatter(10, 10, color='red', linewidths=0.0001)

        # return particles
    def save_animation(self, path=None, show_trajectory=True):

        self.show_trajectory = show_trajectory
        print('saving of animation')
        #fig = add_subplot(111, projection='3d')
        fig = plt.figure(figsize=(10, 10))
        plt.style.use('dark_background')

        Writer = animation.writers['ffmpeg']
        writer = Writer(fps=15, metadata=dict(artist='Me'), bitrate=1800)

        anim = animation.FuncAnimation(plt.gcf(), self.update_anim, interval=1, fargs=(
            fig,), frames=self.number_frames, blit=False)
        name = str(datetime.now())
        name = datetime.now().microsecond
        N = self._mcoords.shape[0]

        anim.save('resources/mp4/bodies={},N={}.mp4'.format(N,str(name),self.number_iteration), writer=writer)
        HTML(anim.to_html5_video())




field = GravityField()


# field.add_body(Body(15, 6 , -np.cos(np.pi / 4)/100, 0.01*np.cos(np.pi / 4) ,mass=30))
# field.add_body(Body(6, 6 , -np.cos(np.pi / 4)/100, 0.01*np.cos(np.pi / 4) ,mass=50))
# field.add_body(Body(-3, 0 ,np.cos(np.pi / 4)/(10*20), np.cos(np.pi / 4)/(10*20),mass=1500))
# field.add_body(Body(-6, -6 , -0.01*np.cos(np.pi / 4)/100, -0.001*np.cos(np.pi / 4) ,mass=60))
# field.add_body(Body(-10, 6 , -np.cos(np.pi / 4)/100, 0.01*np.cos(np.pi / 4) ,mass=100))
# field.add_body(Body(-19, 0 ,np.cos(np.pi / 4)/(10*20), np.cos(np.pi / 4)/(10*20),mass=100))
# field.add_body(Body(-20, -6 , -0.01*np.cos(np.pi / 4)/100, -0.001*np.cos(np.pi / 4) ,mass=60))
# field.add_body(Body(30, 6 , -np.cos(np.pi / 4)/100, 0.01*np.cos(np.pi / 4) ,mass=100))

# field.add_body(Body(-15, -20 , np.cos(np.pi / 4)/(10**100), np.cos(np.pi / 4)/10**100 ,mass=100))

for i in range(1550):
    v = uniform(0,20)

    alpha = uniform(0,360)
    x1 = uniform(-550,700)
    x2 = uniform(-530,500)
    m = uniform(20,300)   
    field.add_body(Body(x1, x2 , -v*np.cos((alpha/360)*np.pi / 4)/100, v*np.sin((alpha/360)*np.pi) ,mass=m))

for i in range(5):
    v = uniform(0,0.1)

    alpha = uniform(0,360)
    x1 = uniform(-550,700)
    x2 = uniform(-530,500)
    m = uniform(500,5000)   
    field.add_body(Body(x1, x2 , -v*np.cos((alpha/360)*np.pi / 4)/100, v*np.sin((alpha/360)*np.pi) ,mass=m))    

for i in range(3):
    v = uniform(0,0.1)

    alpha = uniform(0,360)
    x1 = uniform(-550,700)
    x2 = uniform(-530,500)
    m = uniform(1000,5000)   
    field.add_body(Body(x1, x2 , -v*np.cos((alpha/360)*np.pi / 4)/100, v*np.sin((alpha/360)*np.pi) ,mass=m))        

field.run(16200, C=0.01, number_frames=100, approx_error=0.000001)
field.save_animation()
