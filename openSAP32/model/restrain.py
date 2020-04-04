# openSAP32
# Copyright (c) 2014 Duken Marga Turnip
# License: BSD 3-clause
# (https://github.com/dukenmarga/openSAP32/blob/master/LICENSE.txt)

import numpy as np

class Restrain:
    ''' Define and manage restrain in node'''
    def __init__(self):
        self.list = np.array([])
        self.settlement = np.array([])
        self.spring = np.array([])
        pass
    def addRestrain(self, node, restrain, dimension=2):
        ''' Add restrain to node in structure
        
        Parameters
        ----------
        node : int
            Number of node
        restrain : {'fixed', 'pin', 'roller'}
            Type of restrain
        dimension : int, optional
            Dimension of structure (default: 2)
        
        Example
        -------
        This example shows how to add fixed restrain
        to node 2 and roller restrain to node 4
        
        >>> restrain = Restrain()
        >>> restrain.addRestrain(2, 'fixed')
        >>> restrain.addRestrain(4, 'roller')
        '''
        
        # The logic is to determine node which are
        # restrained based on the type
        # This algorithm still use translation
        # restrain without considering rotation
        totalDOF = dimension*node
        if restrain == 'fixed': # 1,1,1
            restrained = [totalDOF-dimension, totalDOF-dimension+1]
        elif restrain == 'pin': # 1,1,0
            restrained = [totalDOF-dimension, totalDOF-dimension+1]
        elif restrain == 'rollerX' or restrain == 'roller': # 0,1,0
            restrained = [totalDOF-dimension+1]
        elif restrain == 'rollerY': # 1,0,0
            restrained = [totalDOF-dimension]
        else:
            return
        if self.list.size == 0:
            self.list = np.array(restrained)
        else:
            self.list = np.append(self.list, restrained, axis=0)
    def addSettlement(self, node, dx, dy, dimension=2):
        '''Add settlement to node'''
        if self.settlement.size == 0:
            self.settlement = np.array([[node, dx, dy]])
        else:
            self.settlement = np.append(self.settlement, [[node, dx, dy]], axis=0)
        pass
    def addSpring(self, node, k, direction='x', dimension=2):
        '''Add spring restrain to node'''
        if direction == 'x':
            angle = 180
        elif direction == '-x':
            angle = 0
        elif direction == 'y':
            angle = 270
        elif direction == '-y':
            angle = 90

        if self.spring.size == 0:
            self.spring = np.array([[node, k, angle]])
        else:
            self.spring = np.append(self.spring, [[node, k, angle]], axis=0)
        pass
        
