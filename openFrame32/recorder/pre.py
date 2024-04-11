# openFrame32
# Copyright (c) 2014 Duken Marga Turnip
# License: BSD 3-clause
# (https://github.com/dukenmarga/openFrame32/blob/master/LICENSE.txt)

import numpy as np
from numpy.typing import NDArray


class Pre:
    def __init__(self):
        self.T: NDArray[np.float64] = np.array([[]])
        self.localStiffnessMatrix: NDArray[np.float64] = np.array([[[]]])
        self.globalStiffnessMatrix: NDArray[np.float64] = np.array([[]])
        self.loadMatrix: NDArray[np.float64] = np.array([])
        self.unsolvedLoadMatrix: NDArray[np.float64] = np.array([])
        self.unsolvedLoadMatrixWithSettlement: NDArray[np.float64] = np.array([])
        self.unsolvedGlobalStiffnessMatrix: NDArray[np.float64] = np.array([[[]]])
        pass
