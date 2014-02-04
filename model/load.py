# ----------------------------------------------------------------------
# openSAP32
# Copyright (c) 2014 Duken Marga Turnip
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
#  * Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
#  * Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in
#    the documentation and/or other materials provided with the
#    distribution.
#  * Neither the name of openSAP32 the names of its
#    contributors may be used to endorse or promote products
#    derived from this software without specific prior written
#    permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
# FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE        
# COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
# ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
# ----------------------------------------------------------------------

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