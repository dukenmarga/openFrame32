# openSAP32
# Copyright (c) 2014 Duken Marga Turnip
# License: BSD 3-clause
# (https://github.com/dukenmarga/openSAP32/blob/master/LICENSE.txt)

import numpy as np

class Pre():
    def __init__(self):
        self.T = np.array([[]])
        self.localStiffnessMatrix = np.array([[[]]])
        self.globalStiffnessMatrix = np.array([[]])
        self.loadMatrix = np.array([])
        self.unsolvedLoadMatrix = np.array([])
        self.unsolvedLoadMatrixWithSettlement = np.array([])
        self.unsolvedGlobalStiffnessMatrix = np.array([[[]]])
        pass