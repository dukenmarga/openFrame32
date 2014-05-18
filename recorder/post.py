# openSAP32
# Copyright (c) 2014 Duken Marga Turnip
# License: BSD 3-clause
# (https://github.com/dukenmarga/openSAP32/blob/master/LICENSE.txt)

import numpy as np

class Post():
    def __init__(self):
        self.nodeDeformation = np.array([])
        self.nodeForce = np.array([])
        self.nodeStress = np.array([])
        pass