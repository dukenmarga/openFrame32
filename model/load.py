# openSAP32
# Copyright (c) 2014 Duken Marga Turnip
# License: BSD 3-clause
# (https://github.com/dukenmarga/openSAP32/blob/master/LICENSE.txt)

import numpy as np

class Load:
    '''Define and manage load in structure'''
    def __init__(self):
        self.list = np.array([[]])
        pass
    def addLoad(self, node, Fx=0, Fy=0, Fz=0):
        '''Add point load in node
        
        Parameters
        ----------
        node : int
            Number of node
        Fx : float, optional
            Point load in x direction (default: 0)
        Fy : float, optional
            Point load in y direction (default: 0)
        Fz : float, optional
            Point load in z direction (default: 0)
        
        Example
        -------
        This example shows how to add 500 N to node 2
        in x direction
        
        >>> load = Load()
        >>> load.addLoad(2, 500)
        '''
        if self.list.size == 0:
            self.list = np.array([[node, Fx, Fy, Fz]])
        else:
            self.list = np.append(self.list, [[node, Fx, Fy, Fz]], axis=0)
        pass