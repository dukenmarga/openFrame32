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
    ''' Construct and define properties of
        material.
    '''
    def __init__(self):
        self.list = np.array([[]])
        pass
    def defineShearModulus(self, E=0, v=0):
        ''' Calculate shear modulus
        
        Parameters
        ----------
        E : float
            Young's modulus of elasticity of material
            Default value is 0
        v : float
            Poisson's ratio. Default is 0
        
        Example
        -------
        >>> material = Material()
        >>> material.defineShearModulus(200000, 0.17)
        85470.0854701
        '''
        return E / (2*(1+v))
    
    def addMaterial(self, material, F, Fu=0, E=0, v=0):
        ''' Add material.

        Parameters
        ----------
        material : {'concrete', 'steel'}
            String contain material type (Default: 'steel')
        F : float
            Fc for concrete or Fy for steel. Default value for
            concrete is `30 MPa` and `400 MPa` for steel.
        Fu : float, optional
            Ultimit strength of material
            Default value is 1.1 times yield strength (F)
        E : float, optional
            Young's modulus of elasticity of material
            Default value is :math:`4700*\\sqrt{F}` MPa for concrete
            and :math:`200000` MPa for steel
        v : float, optional
            Poisson's ratio. Default is 0.17 for concrete and 0.3 for
            steel material.

        Example
        -------
        >>> material = Material()
        >>> material.addMaterial('concrete', F=30000000) 
        >>> material.addMaterial('steel', F=400000000, Fu=600000000)

        '''
        # indexMaterial is used to distinguish beetween material
        # indexMaterial: 1 for concrete, 2 for steel
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