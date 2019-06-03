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
"""
 
Function MainApp::CalcForce
  for all particles
    force = RootNode.CalculateForceFromTree(particle)
  end for
end 

Function force = TreeNode::CalculateForce(targetParticle)
  force = 0

  if number of particle equals 1
    force = Gravitational force between targetParticle and particle
  else
    r = distance from nodes center of mass to targetParticle
    d = height of the node
    if (d/r < θ)
      force = Gravitational force between targetParticle and node 
    else
      for all child nodes n
        force += n.CalculateForce(particle)
      end for
    end if
  end
end
"""


class Gravity:
    def calculate(dx, dy, M):
        v1 = M * dx / ((dx ** 2 + dy ** 2) ** (2 / 3))
        v2 = M * dy / ((dx ** 2 + dy ** 2) ** (2 / 3))

        return np.array([v1, v2])


class Body:
    ID = 0

    def __init__(self, mass, x0, y0, v0_1, v0_2, h=0.001):
        self.mass = mass
        self.x1 = x0
        self.x2 = y0
        self.v1 = v0_1
        self.v2 = v0_2
        self.x_args = [x0]
        self.y_args = [y0]
        self.v1_args = [v0_1]
        self.v2_args = [v0_2]
        Body.ID += 1
        self.ID = Body.ID
        self.h = h

    def get_mass(self):
        return self.mass

    def set_coord(self, x, y):
        self.x1 = x
        self.x2 = y
        self.x_args.append(x)
        self.y_args.append(y)

    def set_velocity(self, v1, v2):
        self.v1 = v1
        self.v2 = v2
        self.v1_args.append(v1)
        self.v2_args.append(v2)

    def get_init_cordinates(self):
        return np.array([self.x0_1, self.x0_2])

    def get_init_velocity(self):
        return np.array([self.v0_1, self.v0_2])

    def get_x_args(self):
        return self.x_args

    def set_y_args(self):
        return self.y_args

    def update_half_step_coordites(self):
        self.x1 = self.x1 + self.v1 * self.h / 2
        self.x1 = self.x2 + self.v2 * self.h / 2

    def calculate_velocity(self, body):
        delta_x = body.x1 - self.x1
        delta_y = body.x2 - self.x2

        if delta_y == 0 or delta_x == 0:
            return

        M = body.get_mass()

        a = Gravity.calculate(delta_x, delta_y, M)

        self.v1 = self.v1 + self.h * a[0]
        self.v2 = self.v2 + self.h * a[1]

        """
        leap frog
        x = x + vx * (h / 2)
        y = y + vy * (h / 2)

        vx = (vx + h * u(t, x, y))/c
        vy = (vy + h * v(t, x, y))/c

        x = x + vx * (h / 2)
        y = y + vy * (h / 2)
        """

    def reculculate_cordinates(self):
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
        return self.width_node

    def compute_center_mass_node(self):
        """
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
        self.cennter_mass = np.array([x_coord, y_coord])
        if self.body.ID == 1:
            print("center of mass of root:!!!!")
            print(self.cennter_mass)
        return self.cennter_mass

    def use_approximation(self, node2):
        """

        comparing W/R
        where W - width of the region of node
        R distance between body and node
        :param distance:
        :param node:
        :return:
        """
        s = node2.width_node
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
        print(self.body.__str__())
        self.execute(None)

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
                print("using app ")
                print(str(node.body.ID) + " ," + str(nodes[i].body.ID))
            else:
                if node.body.ID != nodes[i].body.ID:
                    node.body.calculate_velocity(nodes[i].body)
                self.calculate_V(node, nodes[i].children)
        # if node.body.ID!=1 and len(node.children)>0:
        #   self.calculate_V(node,node.children)

    def calculate_Roo(self, node):
        nodes = self.root.children
        node.compute_center_mass_node()
        if node.body.ID != 1:
            node.body.calculate_velocity(self.root.body)

        for i in range(len(nodes)):

            if node.use_approximation(nodes[i]):
                print("using app ")
                print(str(node.body.ID) + " ," + str(nodes[i].body.ID))
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
        self.bodies = []
        self.tree = TreeBody()
        self.size = 0

    def update_coordinates(self):
        for b in self.bodies:
            b.reculculate_cordinates()

    def update_half_coordinates(self):
        for b in self.bodies:
            b.update_half_step_coordites()

    def add_body(self, body):
        self.bodies.append(body)
        self.tree.add_element(body)

    def calculate(self, r=9000):
        self.size = r * self.bodies[0].h
        start = time.time()
        for i in range(r):
            self.update_half_coordinates()
            self.tree.calculate()
            self.update_coordinates()
        end = time.time()
        print(end - start)

    def get_size( self, n=1):
        self.z = int(self.size / n)
        return self.z

    def update_HTML_animation(self, i, arg):
        ax = plt.gca()

        # q =ax.quiver(0, 0, self.r[i,2],  self.r[i,3], pivot='mid', color='r', units='inches')
        # q = ax.quiver(0, 0, self.r[i, 2], self.r[i, 3], pivot='mid', color='r', units='inches')
        i = i * self.z

        arg.clf()

        particles, = ax.plot([], [], 'bo', ms=6)
        # particles.set_data([], [])
        # particles.set_data(self.r[i, 0], self.r[i, 1])
        # particles.set_markersize(20)
        #
        g= 10
        q = plt.scatter(-g, -g, color='black', linewidths=0.1)
        q = plt.scatter(-g, g, color='black', linewidths=0.1)
        q = plt.scatter(g, g, color='black', linewidths=0.1)
        q = plt.scatter(g, -g, color='black', linewidths=0.1)

        for b in self.bodies:
            # q = plt.scatter(b.x_args[i], b.y_args[i], color='black', linewidths=5)
            q = plt.scatter(b.x_args[i], b.y_args[i], linewidths=int(b.mass/100))
            q = plt.plot(b.y_args,b.y_args)

        # z = plt.plot(self.r[:, 0], self.r[:, 1], color='blue')
        # plt.draw()
        ax.spines['left'].set_position('zero')
        ax.spines['right'].set_color('none')
        ax.spines['top'].set_color('none')

        return particles

    def print(self):
        self.tree.print()


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


g = Ground()
g.add_body(Body(40, 1, 1, 0.01, 0.001))
g.add_body(Body(20, -4, 6, -5* np.sin(np.pi / 4), -7* np.cos(np.pi / 4)))
# g.add_body(Body(32, 7, 7, 1, 1))
# g.add_body(Body(32, 7.1, 6.9, -1, 1))
# g.add_body(Body(32, -1, 1, 1, -1))
# g.add_body(Body(32, 7.5, 6.6, -1, 1))
# g.add_body(Body(32, -5, -5, 1, -1))
# g.add_body(Body(32, 3, 4, -1, 1))
g.calculate()

fig = plt.figure(figsize=(6, 6))
fig = plt.figure(figsize=(6, 6))

u = lambda t, x, y: 0
v = lambda t, x, y: -10
#
# point.add_force(f)
# z = point.calculate_radius_vector(20 * np.cos(np.pi / 4), +50 * np.sin(np.pi / 4), n=700)
# plt.plot(z[:, 0], z[:, 1])
size = int(g.get_size(1))
# print(size)
anim = animation.FuncAnimation(plt.gcf(), g.update_HTML_animation, interval=60, fargs=(fig,), frames=size, blit=False)
HTML(anim.to_html5_video())
plt.show()

###  conda install -c conda-forge ffmpeg

# for n in range(10):
#     for m in range(n + 1, 10):
#         print("(n,m)" + str(n)+ " ,"+str(m))
