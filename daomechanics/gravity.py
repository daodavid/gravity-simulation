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


class Body:
    def __init__(self, mass, x0, y0, v0_1, v0_2):
        self.mass = mass
        self.x1 = x0
        self.x2 = y0
        self.v1 = v0_1
        self.v2 = v0_2
        self.x_args = [x0]
        self.y_args = [y0]
        self.v1_args = [v0_1]
        self.v2_args = [v0_2]

    def get_mass(self):
        return self.mass

    def set_coord(self,x,y):
        self.x1=x
        self.x2=y
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


class NodeBody:
    def __init__(self, body, range=[4, 4]):
        self.body = body
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

    def __add__(self, node):
        if key_x <= node.body.x and key_y >= node.y:
            if node.Q_11 is None:
                node.Q_11 = Node(key_x, key_y, value)
                return
            self.__add__(node.Q_11, key_x, key_y, value)
        elif key_x >= node.x and key_y >= node.y:
            if node.Q_12 is None:
                node.Q_12 = Node(key_x, key_y, value)
                return
            self.__add__(node.Q_12, key_x, key_y, value)
        elif key_x <= node.x and key_y <= node.y:
            if node.Q_21 is None:
                node.Q_21 = Node(key_x, key_y, value)
                return
            self.__add__(node.Q_21, key_x, key_y, value)
        elif key_x >= node.x and key_y <= node.y:
            if node.Q_22 is None:
                node.Q_22 = Node(key_x, key_y, value)
                return
            node.__add__(node.Q_22, key_x, key_y, value)

    def execute(self, funct):
        pass


class Gravity:
    pass


###https://www.maths.tcd.ie/~btyrrel/nbody.pdf
def center_mas():
    pass
