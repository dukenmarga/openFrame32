# openFrame32
# Copyright (c) 2014 Duken Marga Turnip
# License: BSD 3-clause
# (https://github.com/dukenmarga/openFrame32/blob/master/LICENSE.txt)

import numpy as np


class Structure:
    """Assembly structure"""

    def __init__(self):
        self.list = np.array([[]])

    def AddElement(self, node1: int, node2: int, section: int):
        """Construct element an element by combining 2 nodes

        Example
        -------
        Add element from node 2 and 3 using section 2

        >>> structure = Structure()
        >>> structure.addElement((2,3), 2)
        """

        if self.list.size == 0:
            self.list = np.array([[node1, node2, section]])
        else:
            self.list = np.append(self.list, [[node1, node2, section]], axis=0)
