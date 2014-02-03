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
import math

class Material:
    def __init__(self):
        #self.concrete = Concrete()
        #self.steel = Steel()
        self.list = np.array([[]])
        pass
    def defineShearModulus(self, E, v):
        return E / (2*(1+v))
    
    # F here means Fc for concrete or Fy for steel
    # material: steel, concrete
    def addMaterial(self, material, F, Fu=0, E=0, v=0):
        if material == 'concrete':
            indexMaterial = 1
            v = 0.17
            E = 4700 * math.sqrt(F)
            Fu = 1.1 * F
        else:
            indexMaterial = 2
            v = 0.3
            E = 200000000000
            Fu = 1.1 * F
        if self.list.size == 0:
            self.list = np.array([[indexMaterial, F, Fu, E, v]])
        else:
            self.list = np.append(self.list, [[indexMaterial, F, Fu, E, v]], axis=0)


class Concrete(Material):
    def __init__(self):
        Material.__init__(self)
        self.list = np.array([[]])
        
    def addConcrete(self, Fc, E, v=0.2):
        '''Define concrete material
            Fc = compressive concrete strength \
            E = modulus elasticity\
            v = Poison ratio
            list = 2 dimension for holding material properties
        '''
        if self.list.size == 0:
            self.list = np.array([[Fc, E, v]])
        else:
            self.list = np.append(self.list, [[Fc, E, v]], axis=0)
            
class Steel(Material):
    def __init__(self):
        Material.__init__(self)
        self.list = np.array([[]])

    def addSteel(self, Fy, Fu, E, v=0.3):
        if self.list.size == 0:
            self.list = np.array([[Fy, Fu, E, v]])
        else:
            self.list = np.append(self.list, [[Fy, Fu, E, v]], axis=0)