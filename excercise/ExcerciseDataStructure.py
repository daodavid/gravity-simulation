"""
author : Daodeiv
Tree codes - ALGORITHM
https://www.geeksforgeeks.org/quad-tree/
"""


class Node:

    def __init__(self, key_x=0, key_y=0, value=None, range=[4, 4]):
        self.x = key_x  # x coordinates
        self.y = key_y  # y cordinates
        self.value = value
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

    def __add__(self, node, key_x, key_y, value):
        if key_x <= node.x and key_y >= node.y:
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

    def execute(self,funct):
         pass

    def iterate(self):
        if self.Q_11 is not None:
            self.Q_11.iterate()
        print(str(self.x) + "," + str(self.y) + "- value" + self.value)
        self.execute(None)
        if self.Q_21 is not None:
            self.Q_21.iterate()


        if self.Q_12 is not None:
            self.Q_12.iterate()
        if self.Q_22 is not None:
            self.Q_22.iterate()





class Tree:
    def __init__(self):
        self.root = None;

    def add_element(self, key_x, key_y, value):
        if self.root is None:
            self.root = Node(key_x, key_y, value)

        else:
            self.root.__add__(self.root, key_x, key_y, value)

    def print(self):
       self.root.iterate()


t = Tree()

t.add_element(key_x=0, key_y=0, value="First 0 0 ")
t.add_element(-1, 2, "-1 2  ")
t.add_element(-1, 1, " - 1 1 ")
t.add_element(-1, -1, " - 1 1 ")
t.add_element(-2, -3, " - 1 1 ")
t.add_element(-2, -2.5, " - 1 1 ")
t.add_element(1, 1, "1 1 ")
t.add_element(2, 3, "2 3 ")


t.print()

