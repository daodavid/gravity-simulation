import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib import animation, rc
from IPython.display import HTML
import numpy as np
from datetime import datetime
import warnings


class Body:
    '''
    fuc
    '''

    ID = 0
    @classmethod
    def get_ID(cls):
        '''
        get unique id 
        '''
        Body.ID = Body.ID+1
        return Body.ID

    def __init__(self,  x0, y0, v_x, v_y, mass=1, h=0.001):
        '''
        Parameters

        '''
        self.id = Body.get_ID()
        # integration step
        self.h = h

        # ndarray current coors
        self._mcoord = np.array([x0, y0])
        # current velocity
        self._mvelocity = np.array([v_x, v_y])

        # all cordinates in time
        self._coord = np.array(self._mcoord)


class GravityField:

    # g = 2.071×10−43 s2⋅m^−1⋅kg^−1.
    # gravity constant
    G = 0.001

    def __init__(self, integratin_setp=0.1):

        self.h = integratin_setp
        # curent coordinates and velocity of all bodies
        self._mcoords = np.array([])  # [id,x,y]
        self._mvelocity = np.array([])  # [id,v_x,v_y]

        # all  x cordinates for all  particule
        self.x_cordinates = np.array([])
        # all y cordinates for all particlues
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

        if self.x_cordinates.size != 0:
            self.x_cordinates = np.append([self.x_cordinates], b._mcoord[0])
            self.y_cordinates = np.append([self.y_cordinates], b._mcoord[1])
        else:
            self.x_cordinates = np.array(b._mcoord[0])
            self.y_cordinates = np.array(b._mcoord[1])

    def leaf_frog_step1(self):
        """

         step 1 of leapFrog integration
         This method is used for calculating of x coordinates
         for every particles before to be calculated the  new velocity values
        """

        #self.x1 = self.x1 + self.v1 * self.h / 2
        #self.x2 = self.x2 + self.v2 * self.h / 2
        self._mcoords = self._mcoords + self._mvelocity*(self.h/2)
        x = self._mcoords[:, 0]
        y = self._mcoords[:, 1]

        if self.x_cordinates.shape == x.shape:
            self.x_cordinates = np.array([self.x_cordinates, x])
            self.y_cordinates = np.array([self.y_cordinates, y])
        else:
            self.x_cordinates = np.append(self.x_cordinates, [x], axis=0)
            self.y_cordinates = np.append(self.y_cordinates, [y], axis=0)

    def leap_frog_step2(self):
        # v1 = Gravity.G*M * dx / ((dx ** 2 + dy ** 2) ** (3/2))
        # v2 = Gravity.G*M * dy / ((dx ** 2 + dy ** 2) ** (3/2))

        def calc_sum_all_forces(element, all_cordinates, masses):
            # delta element_ij - all_corinates_kj
            delta_r_M = all_cordinates-element
            # all delta (x_ij - x_kj) ^2
            # mutiple by mass (miss)
            devider_modul_r = np.sum(delta_r_M**2, axis=1)**(3/2)
            if(devider_modul_r.any() < self.approx_error or devider_modul_r<elf.approx_error ):
                warnings.warn("delta r < approx_error ,the force is skipp ".format(self.approx_error))
                devider_modul_r = 1


            g1 = 100*np.sum(delta_r_M[:, 0]*(1/devider_modul_r))
            g2 = 100*np.sum(delta_r_M[:, 1]*(1/devider_modul_r))

            return [g1, g2]

        for i in range(self._mcoords.shape[0]):
            all_codinates = np.delete(self._mcoords, i, 0)
            force = calc_sum_all_forces(
                self._mcoords[i, :], all_codinates, self._masses)

            self._mvelocity[i][0] = self._mvelocity[i][0] + force[0]*self.h
            self._mvelocity[i][1] = self._mvelocity[i][1] + force[1]*self.h
            if(i == 0):
                pass
                #  print('f_x=' + str(force[0]))
                #  self._force = np.append(self._force,force[0])
                #  print('v_x' + str(i) +' '+ str(self._mvelocity[i][1]))
                #  print('x_1 :' + str(self._mcoords[i][0]))
                #  print('y_1=' + str(self._mcoords[i+1][0]))
                #  print('...')

    def save(self):
        columns = ['body_' + str(i) for i in range(self.x_cordinates[0].size)]
        self.X_cordinates = pd.DataFrame(self.x_cordinates, columns=columns)
        self.Y_cordinates = pd.DataFrame(self.y_cordinates, columns=columns)
        print('calculation complete succsefuly')

    def run(self, n, number_frames=20, approx_error = 1.5):
        '''
        parametes :
        n- number of iteration
        '''
      
        self.number_iter = n
        self.number_frames = n  # number_frames
        self.frame_step = 1  # int(n/number_frames)
        self.approx_error = approx_error 
        for i in range(n):
            field.leaf_frog_step1()
            field.leap_frog_step2()
        self.save()


    def result(self):

        return self.X_cordinates, self.Y_cordinates

    def __repr__(self):
        return ''

    def update_anim(self, i, arg):
        x, y = self.X_cordinates, self.Y_cordinates
        ax = plt.gca()
        arg.clf()
        k = self.frame_step*i
        for j in range(x.shape[1]):
            body = 'body_{}'.format(j)
            plt.scatter(x[body][k], y[body][k])
            plt.plot(np.array(x[body]), np.array(y[body]), color='blue')
        #q = plt.scatter(self.X_cordinates, self.Y_cordinates, color='indigo', linewidths=None)


        ax.spines['left'].set_position('zero')
        ax.spines['right'].set_color('none')
        ax.spines['top'].set_color('none')

        # return particles
    def save_animation(self, path=None):
        print('saving of animation')
        fig = plt.figure(figsize=(6, 6))

        Writer = animation.writers['ffmpeg']
        writer = Writer(fps=15, metadata=dict(artist='Me'), bitrate=1800)

        anim = animation.FuncAnimation(plt.gcf(), field.update_anim, interval=1, fargs=(
            fig,), frames=self.number_frames, blit=False)
        name = str(np.random.randint(0, 1000))
        name = str(datetime.now())
        name = datetime.now().microsecond
        anim.save('resources/mp4/{}.mp4'.format(str(name)), writer=writer)
        HTML(anim.to_html5_video())


field = GravityField()
#field.add_body(Body(3, 2, -0.3, -1))
field.add_body(Body(-15 ,5,-0.00001*np.cos(np.pi / 4), 0.0001*np.cos(np.pi / 4)))
field.add_body(Body( -6, -4,1*np.cos(np.pi / 4), 1*np.cos(np.pi / 4)))
#field.add_body(Body(-15 ,-5,+0.00001*np.cos(np.pi / 4), -0.0001*np.cos(np.pi / 4)))
#field.add_body(Body( -6, 6,1*np.cos(np.pi / 4), 1*np.cos(np.pi / 4)))
#field.add_body(Body(1, 1, 0.2, 0.2))
field.run(100)
field.save_animation()
x, y = field.result()

plt.plot(x['body_1'][0:50])

plt.plot(x['body_0'][0:50])
# print(x['body_0'])
plt.show()
plt.plot(np.log(field._force[1:20]))
plt.plot(field._force[1:20])
plt.show()

# def update_HTML_animation(X,Y):

