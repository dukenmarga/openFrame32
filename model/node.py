# openSAP32
# Copyright (c) 2014 Duken Marga Turnip
# License: BSD 3-clause
# (https://github.com/dukenmarga/openSAP32/blob/master/LICENSE.txt)

import numpy as np

class Node:
    '''Manage node coordinat of structure
       This class use cartesian domain: x, y, z
    '''
    def __init__(self):
        self.list = np.array([[]])
        pass
    def addNode(self, x, y=0, z=0):
        '''Add node in coordinate (x, y, z)
        
        Parameter
        ---------
        x : int
            Coordinate in x direction
        y : int, optional
            Coordinate in y direction (default: 0)
        z : int, optional
            Coordinate in z direction (default: 0)
            
        Example
        -------

        >>> node = Node()
        >>> node.addNode(12, 3)
        >>> node.addNode(13, 4, 5)
        '''
        if self.list.size == 0:
            self.list = np.array([[x, y, z]])
        else:
            self.list = np.append(self.list, [[x, y, z]], axis=0)
        pass
    