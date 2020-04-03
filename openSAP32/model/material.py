# openSAP32
# Copyright (c) 2014 Duken Marga Turnip
# License: BSD 3-clause
# (https://github.com/dukenmarga/openSAP32/blob/master/LICENSE.txt)

import numpy as np
import math

class Material:
    ''' Define and manage properties of
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
        
        Return
        ------
        out : float
            Shear modulus
        
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
        # indexMaterial is used to distinguish between material
        # indexMaterial: 1 for concrete, 2 for steel
        if material == 'concrete':
            indexMaterial = 1
            if v == 0:
                v = 0.17
            if E ==0:
                E = 4700 * math.sqrt(F)
            if Fu == 0:
                Fu = 1.1 * F
        else:
            indexMaterial = 2
            if v == 0:
                v = 0.3
            if E == 0:
                E = 200000000000
            if Fu == 0:
                Fu = 1.1 * F
        if self.list.size == 0:
            self.list = np.array([[indexMaterial, F, Fu, E, v]])
        else:
            self.list = np.append(self.list, [[indexMaterial, F, Fu, E, v]], axis=0)