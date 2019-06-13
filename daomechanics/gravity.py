import time
import timeit
import matplotlib.pyplot as plt
from matplotlib import animation, rc
from IPython.display import HTML
import numpy as np

"""
https://beltoforion.de/article.php?a=barnes-hut-galaxy-simulator
The Barnes-Hut algorithm
"""


class Gravity:
    G = 0.001

    @staticmethod
    def calculate(dx, dy, M):
        """
        dx is distance between Obj1 and Obj2 measured under X axis
        dy is distance between Obj1 and Obj2 measured under Y axis
        M is the mass of obj2
        """

        #gravity low
        v1 = Gravity.G*M * dx / ((dx ** 2 + dy ** 2) ** (3/2))
        v2 = Gravity.G*M * dy / ((dx ** 2 + dy ** 2) ** (3/2))

        return np.array([v1, v2])


class Body:

    """
    The body is the material point.For the material point we do not consider its form,
    the only meaningful parameters are,mass and radius vector
    """
    ID = 0

    def __init__(self, mass, x0, y0, v0_1, v0_2, h=0.001):
        self.mass = mass
        self.x1 = x0  #current lenght of X coordinate
        self.x2 = y0  #current lenght of Y coordinate
        self.v1 = v0_1 ##current velocity on X coord
        self.v2 = v0_2 # current velocity on Y coord
        self.x_args = [x0] #list of moment state of X coords
        self.y_args = [y0]
        self.v1_args = [v0_1] #list of velocities on X coords
        self.v2_args = [v0_2]  #list of velocities on Y coords
        Body.ID += 1
        self.ID = Body.ID
        self.h = h  #integration step

    def get_mass(self):
        return self.mass

    def set_coord(self, x, y):
        """
        set state of the object,its coordinates
        """
        self.x1 = x
        self.x2 = y
        self.x_args.append(x)
        self.y_args.append(y)
    def get_radious(self):
        """
        returs all coordinates X_args,Y_args and their velocity as matrix (numpy array)
        """
        return np.array([self.x_args,self.y_args,self.v1_args,self.v2_args]).T

    def set_velocity(self, v1, v2):
        """
        setting of velocity
        """
        self.v1 = v1
        self.v2 = v2
        self.v1_args.append(v1)
        self.v2_args.append(v2)

    def get_init_cordinates(self):
        """
        the initial state of coordinates
        """
        return np.array([self.x0_1, self.x0_2])

    def get_init_velocity(self):
        """
          the initial state of velocity
        """
        return np.array([self.v0_1, self.v0_2])

    def get_x_args(self):
        """
        return all x_cordinates until this moment
        """
        return self.x_args

    def set_y_args(self):
        """
         return all y_cordinates until this moment
        """

        return self.y_args


    """
        leap from main algoritam
        leap frog  integration main algoritams
     
        step 1)
            x = x + vx * (h / 2)
                y = y + vy * (h / 2)
     
        step 2)
            vx = (vx + h * u(t, x, y))/c
            vy = (vy + h * v(t, x, y))/c
    
         step 3)   
            x = x + vx * (h / 2)
            y = y + vy * (h / 2)
        
        """

    def update_half_step_coordites(self):
        """
        step 1 of leapFrog integration
        This method is used for calculating of x coordinates
        for every particles before to be calculated the  new velocity values
        """
        self.x1 = self.x1 + self.v1 * self.h / 2
        self.x2 = self.x2 + self.v2 * self.h / 2

    def calculate_velocity(self, body):
        """
        step 2 of leapfrog integration.
        Here will be calculated the new velocity parameters
        in way that every force will contribute for changing of velocaty of body
         """


        delta_x = body.x1 - self.x1
        delta_y = body.x2 - self.x2



        if abs(delta_y) < 1.5 or abs(delta_x) < 1.5:  ### in the program we do not consider the law of conservation of energy,theorfore ,the calculation is skipp in verry small distcance bewtween object ,because the velocity become infinity

           return


        M = body.get_mass()

        a = Gravity.calculate(delta_x, delta_y, M)
        step = self.h
        if abs(a[0])>30 or abs(a[1])>30:
            step = self.h/100000
            print("St")
        p1 = self.v1 = self.v1 + step * a[0]
        p2 = self.v2 = self.v2 + step * a[1]


        if self.v1>10 or self.v2>10:
           print(self.v1)
           print(self.v2)



    def caluclate_velocity_center_mass(self,coord,mass):
        """
        calculate force acting to body using the center of mass
        """
        delta_x = coord[0] - self.x1
        delta_y = coord[1] - self.x2

        if abs(delta_y) <1 and abs(delta_x) <1:  ### in the program we do not consider the law of conservation of energy,theorfore ,the calculation is skipp in verry small distcance bewtween object ,because the velocity become infinit
           return
        a = Gravity.calculate(delta_x, delta_y, mass)
        step = self.h
        if abs(a[0])>30 or abs(a[1])>30:
            print("St")
            step = self.h/100000
        p1 = self.v1 = self.v1 + step * a[0]
        p2 = self.v2 = self.v2 + step * a[1]









    def reculculate_cordinates(self):
        """
        step 3 of leapfrog
        """
        self.x1 = self.x1 + self.v1 * self.h / 2
        self.x2 = self.x2 + self.v2 * self.h / 2
        self.x_args.append(self.x1)
        self.y_args.append(self.x2)
        self.v1_args.append(self.v1)
        self.v2_args.append(self.v2)

    def increment_velocity(self, R):
        pass

    def __str__(self):
        return "[" + str(self.x1) + "," + str(self.x2) + "]" + "- mass : " + str(self.mass)


class NodeBody:

    """
    Node ,leaf

    The objects of this class
    contain the body and its childs in Tree

    This class coutains the main logic of Barnes-Hut algoritams

    every node has a 4 childs represent 4 quadrants

    """
    criteria = 0.5

    def __init__(self, body, range=[4, 4]):

        self.body = body
        self.width_node = 0
        self.size_node = 0

        """
         Quadrants
        |11|12' 
        |21|22|
        _
        """
        self.root = None
        self.Q_11 = None  # Quadrant 11
        self.Q_12 = None  # Quadrant 12
        self.Q_21 = None  # Quadrant 21
        self.Q_22 = None  # Quadrant 22
        self.children = []  # helper lsit wich contains all nodes described above

    def __set_width_node(self, node):
        d = self.get_distance(node)
        if d > self.width_node:
            self.width_node = d

    def __add__(self, node, body):
        """
        insert into tree depends on comparing of coordinates
        """

        if body.x1 <= node.body.x1 and body.x2 >= node.body.x2:
            if node.Q_11 is None:
                node.Q_11 = NodeBody(body)
                self.children.append(node.Q_11)
                self.__set_width_node(node.Q_11)
                return
            node.Q_11.__add__(node.Q_11, body)
        elif body.x1 >= node.body.x1 and body.x2 >= node.body.x2:
            if node.Q_12 is None:
                node.Q_12 = NodeBody(body)
                self.children.append(node.Q_12)
                self.__set_width_node(node.Q_12)
                return
            node.Q_12.__add__(node.Q_12, body)
        elif body.x1 <= node.body.x1 and body.x2 <= node.body.x2:
            if node.Q_21 is None:
                node.Q_21 = NodeBody(body)
                self.children.append(node.Q_21)
                self.__set_width_node(node.Q_21)
                return
            node.Q_21.__add__(node.Q_21, body)
        elif body.x1 >= node.body.x1 and body.x2 <= node.body.x2:
            if node.Q_22 is None:
                node.Q_22 = NodeBody(body)
                self.children.append(node.Q_22)
                self.__set_width_node(node.Q_22)
                return
            node.Q_22.__add__(node.Q_22, body)

    def get_distance(self, node2):
        dx = self.body.x1 - node2.body.x2
        dy = self.body.x2 - node2.body.x2

        delta = np.sqrt(dx ** 2 + dy ** 2)
        return delta

    def get_width_note(self):
        n=0
        z=0
        for i in self.children:
           if z<self.get_distance(i):
                z=self.get_distance(i)

        return z


    def compute_center_mass_node(self):
        """

        recursivly compute center of mass of one node and its leafs
        R = Sum (x_i*m_iE1 + y_i*mi*E2)/M
        where M = sum m_i
        :param node: nodeBody
        :return: center of mass as sum of all bodyes with root given node
        """

        c = self.get_radius_vector_mass_node()
        sum_x = c[0]  # sum of x_i*m_i
        sum_y = c[1]  # sum of y_i*m_i
        sum_m = c[2]  # sum of m_i
        x_coord = sum_x / sum_m
        y_coord = sum_y / sum_m
        self.center_mass = np.array([x_coord, y_coord])
        self.mass_node=sum_m

        if self.body.ID == 1:
              pass
        return self.center_mass

    def use_approximation(self, node2):
        """

        comparing W/R
        where W - width of the region of node
        R distance between body and node

        this method do diciacion if the calulation of force will be
        acording only one body of node or the hole bodies belongs to the node as center of mass
        :param distance:
        :param node:
        :return:
        """
        s = node2.get_width_note()
        d = node2.compute_center_mass_node()
        k1 = (self.body.x1 - d[0]) ** 2
        k2 = (self.body.x1 - d[0]) ** 2

        k = np.sqrt(k1 + k2)
        if k == 0 or s == 0:
            return False
        o = s / k

        if o < NodeBody.criteria:
            return True
        else:
            return False

    def get_radius_vector_mass_node(self):
        """
        That method returns np.array(sum of x1_children  , sum x2_children,sum M_children)

        :return:
        """
        N = self.children
        result = np.array([self.body.x1 * self.body.mass, self.body.x2 * self.body.mass, self.body.mass])
        M = 0
        if len(N) > 0:
            for i in range(len(N)):
                result = result + N[i].get_radius_vector_mass_node()

        return result

    def iterate(self):
        if self.Q_11 is not None:
            self.Q_11.iterate()

        if self.Q_21 is not None:
            self.Q_21.iterate()

        if self.Q_12 is not None:
            self.Q_12.iterate()
        if self.Q_22 is not None:
            self.Q_22.iterate()


class TreeBody:
    def __init__(self):
        self.root = None;

    def add_element(self, body):
        if self.root is None:
            self.root = NodeBody(body)

        else:
            self.root.__add__(self.root, body)

    def print(self):
        self.root.iterate()

    def calculate_V(self, node, nodes):
        if len(nodes) == 0:
            return
        for i in range(len(nodes)):
            if node.use_approximation(nodes[i]):
                node.body.caluclate_velocity_center_mass(nodes[i].center_mass,nodes[i].mass_node)
                if node.body.ID != nodes[i].body.ID:
                    node.body.calculate_velocity(nodes[i].body)
                self.calculate_V(node, nodes[i].children)


    def calculate_Roo(self, node):
        nodes = self.root.children
        node.compute_center_mass_node()
        if node.body.ID != 1:
            node.body.calculate_velocity(self.root.body)

        for i in range(len(nodes)):

            if node.use_approximation(nodes[i]):
                node.body.caluclate_velocity_center_mass(nodes[i].center_mass,nodes[i].mass_node)

            else:
                if node.body.ID != nodes[i].body.ID:
                    node.body.calculate_velocity(nodes[i].body)
                if len(nodes[i].children) > 0:
                    self.calculate_V(node, nodes[i].children)

        for n in node.children:
            self.calculate_Roo(n)

    def calculate(self):
        self.calculate_Roo(self.root)


class Ground:
    def __init__(self):
        print("innit Ground")
        self.bodies = []
        self.tree = TreeBody()
        self.size = 0
        self.trajectory=False

    def update_coordinates(self):
        for b in self.bodies:
            b.reculculate_cordinates()

    def update_half_coordinates(self):
        for b in self.bodies:
            b.update_half_step_coordites()

    def add_body(self, body):
        self.bodies.append(body)
        self.tree.add_element(body)

    def calculate(self, r=900):

        start = time.time()
        for i in range(r):
            self.update_half_coordinates()
            self.tree.calculate()
            self.update_coordinates()
        end = time.time()
        print(time)
        print(end - start)

        z = len(self.bodies[1].x_args)
        self.size = z


    def get_size( self, n=100):
        self.n=n
        self.increment_plot = int(self.size / n)
        self.m=0
        return n

    def update_HTML_animation(self, i, arg):
        ax = plt.gca()

        #q =ax.quiver(0, 0, self.r[i,2],  self.r[i,3], pivot='mid', color='r', units='inches')
        #q = ax.quiver(0, 0, self.r[i, 2], self.r[i, 3], pivot='mid', color='r', units='inches')
        self.m=self.m+ self.increment_plot
        if(self.m<self.size):
            i=self.m

        arg.clf()
        #plt.figure(figsize=(6, 6))

        ax.patch.set_facecolor('indigo')
        particles, = ax.plot([], [], 'bo', ms=6)
        # particles.set_data([], [])
        # particles.set_data(self.r[i, 0], self.r[i, 1])
        # particles.set_markersize(20)
        #
        plt.scatter(20, 20, color='red', linewidths=0.0001)
        plt.scatter(-20, -20, color='red', linewidths=0.0001)




        for b in self.bodies:
            k=1
            if b.mass>9000:
               k=1000

            q = plt.scatter(b.x_args[i], b.y_args[i],color='indigo', linewidths=int(b.mass/(k*500)))
            if self.trajectory:
              #plt.plot(np.array(b.x_args)[:, 0],np.array( b.y_args[:, 1]), color='blue')
              pass



        ax.spines['left'].set_position('zero')
        ax.spines['right'].set_color('none')
        ax.spines['top'].set_color('none')

        return particles

    def print(self):
        self.tree.print()

    def show_tragectory(self,b):
       self.trajectory=b


"""
Force Calculation 
d - Size of box
r - Partical distance for nodes center of mass

k = d/r

If θ lies below a certain threshold the force 
can be approximated by inserting the quadrant nodes 
mass and its center of mass in the law of gravity. 
The child nodes don't have to be summed up separately.
 A reasonable relation is k < 1. If θ
  is larger than the threshold the quadrants effect can't be 
  approximated and all of its child nodes have to be tested again. The iteration stops only after all nodes have been tested. 
  The worst case scenario is having to test all nodes without finding any node that meets the MAC. In such a case the result 
  is similar to summing up all mutual particle forces (θ=0). 
  The iteration depth can be finetuned by adjusting θ. Animation 1 illustrates 
the influence of θ on the number of force computations

k = d/r

"""


###https://www.maths.tcd.ie/~btyrrel/nbody.pdf
### http://algorithm-interest-group.me/assets/slides/barnes_hut.pdf
### https://www.cs.vu.nl/ibis/papers/nijhuis_barnes_2004.pdf
##http://www.cs.hut.fi/~ctl/NBody.pdf
def center_mas():
    pass



###  conda install -c conda-forge ffmpeg

# for n in range(10):
#     for m in range(n + 1, 10):
#         print("(n,m)" + str(n)+ " ,"+str(m))
