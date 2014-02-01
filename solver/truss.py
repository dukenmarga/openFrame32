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
import solver.mathematic as maths

class Truss():
    def __init__(self):
        self.list = np.array([[]])
        self.dataTrigonometri = np.array([[]])
        self.localStiffnessMatrix = np.array([[[]]])
        self.globalStiffnessMatrix = np.array([[]])
        self.loadMatrix = np.array([])
        pass
    def solve2d(self, node, material, section, structure, load, restrain):
        self.DOF = 2
        self.assembleTrigonometri(structure, node)
        self.assembleLocalStiffness(structure, section)
        self.assembleGlobalStiffness(structure, node)
        self.assembleLoad(load, node)
        pass
    def assembleTrigonometri(self, structure, node):
        '''
        This function stores value of sin, cos, and tan of angle
        that is formed beetween node1 and node2 for
        each element in structure.
        
        Example
        -------
        Element 2 in structure is formed beetween
        node2: (x2=4,y2=3) and node1: (x1=0, y1=0). So,
        b = y2-y1 = 3-0 = 3;
        a = x2-x1 = 4-0 = 4;
        c = 5 => use pythagoras

        Sin = b/c;
        Cos = a/c;
        Tan = a/b;
        
        Todo: Handle value if divisionzero is occured
        
        '''
        for element in structure.list:
            # n1 & n2 are number of nodes for each element
            n1, n2 = element[0]-1, element[1]-1

            # a is length of coordinate of node 2 and node 1 in x direction
            # b is length of coordinate of node 2 and node 1 in y direction
            # c is real length of node 1 and node 2
            indexX, indexY = 0, 1
            a = node.list[n2][indexX] - node.list[n1][indexX]
            b = node.list[n2][indexY] - node.list[n1][indexY]
            c = length = maths.hypotenuse(b, a)
            
            # S=sin C=cos T=tan
            S = b/c
            C = a/c
            T = 0 #a/b
            
            # Store trigonometri data of each element
            if self.dataTrigonometri.size == 0:
                self.dataTrigonometri = np.array([[S, C, T, length]])
            else:
                self.dataTrigonometri = np.append(self.dataTrigonometri, [[S, C, T, length]], axis=0)
        pass
    def assembleLocalStiffness(self, structure, section):
        i = 0
        indexArea = 0
        indexSecondInertia = 1
        indexLength = 3
        for element in structure.list:
            # n1 & n2 are number of nodes for each element
            n1, n2 = element[0]-1, element[1]-1
            numberSection = element[2]-1
            
            # B = A*E/L
            A = section.list[numberSection][indexArea]
            E = section.list[numberSection][indexSecondInertia]
            L = self.dataTrigonometri[i][indexLength]
            B = A * E / L
            
            S = self.dataTrigonometri[i][0]
            C = self.dataTrigonometri[i][1]
            
            matrix = [[C*C,   C*S, -C*C, -C*S],
                      [C*S,   S*S, -C*S, -S*S],
                      [-C*C, -C*S,  C*C,  C*S],
                      [-C*S, -S*S,  C*S,  S*S]]
            if self.localStiffnessMatrix.size == 0:
                self.localStiffnessMatrix = np.array([matrix])
            else:
                self.localStiffnessMatrix= np.append(self.localStiffnessMatrix, \
                                                    [matrix], axis=0)
            i = i+1
        self.localStiffnessMatrix *= B
        pass
    def assembleGlobalStiffness(self, structure, node):
        size = np.size(node.list, 1) * self.DOF
        self.globalStiffnessMatrix = np.array(np.zeros((size, size)))
        
        i = 0
        for element in structure.list:
            # n1 & n2 are number of nodes for each element
            n1, n2 = element[0], element[1]
            
            a1 = 2*n1-2
            a2 = 2*n1
            b1 = 2*n2-2
            b2 = 2*n2
            self.globalStiffnessMatrix[a1:a2, a1:a2] += self.localStiffnessMatrix[i, 0:2, 0:2]
            self.globalStiffnessMatrix[a1:a2, b1:b2] += self.localStiffnessMatrix[i, 0:2, 2:4]
            self.globalStiffnessMatrix[b1:b2, a1:a2] += self.localStiffnessMatrix[i, 2:4, 0:2]
            self.globalStiffnessMatrix[b1:b2, b1:b2] += self.localStiffnessMatrix[i, 2:4, 2:4]
            i = i+1
            pass
        pass
    def assembleLoad(self, load, node):
        size = np.size(node.list, 1) * 2 
        self.loadMatrix = np.array(np.zeros((size,1)))
        for load in load.list:
            node = load[0]
            Fx = load[1]
            Fy = load[2]
            self.loadMatrix[2*node-2:2*node] += [[Fx], [Fy]]
        pass
    