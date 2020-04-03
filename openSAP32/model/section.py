# openSAP32
# Copyright (c) 2014 Duken Marga Turnip
# License: BSD 3-clause
# (https://github.com/dukenmarga/openSAP32/blob/master/LICENSE.txt)

import numpy as np

class Section:
    ''' Define and manage section of element'''
    def __init__(self):
        self.list = np.array([[]])
    def AddSection(self, area=0, secondInertia=0, material=1):
        '''Add property of section
        
        Parameters
        ----------
        area : float
            Total area of section (default=0)
        secondInertia : float
            Second inertia of section (default=0)
        material : int
            Index number of material that is assigned
            using class Material (default: 1)
            
        Example
        -------
        Add 0.04 :math:`m^2` using material 2 and 
        second moment inertia 0.0001333 :math:`m^4`

        >>> section = Section()
        >>> section.addSection(0.04, 0.0001333, 2)
        '''
        
        if self.list.size == 0:
            self.list = np.array([[area, secondInertia, material]])
        else:
            self.list = np.append(self.list, [[area, secondInertia, material]], axis=0)