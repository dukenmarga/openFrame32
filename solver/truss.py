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
    ''' Perform truss structure analysis
    
    All index numbering in this class use 2 method:
    - ArrayIndexing : index number is using numpy indexing
        start from zero (0)
    - NormalIndexing : index number is using normal indexing
        start from one (1), commonly used for numbering
        for human usage.
    '''
    def __init__(self):
        self.list = np.array([[]])
        self.dataTrigonometri = np.array([[]])
        self.localStiffnessMatrix = np.array([[[]]])
        self.globalStiffnessMatrix = np.array([[]])
        self.loadMatrix = np.array([])
        self.unsolvedLoadMatrix = np.array([])
        self.unsolvedLoadMatrixWithSettlement = np.array([])
        self.unsolvedGlobalStiffnessMatrix = np.array([[[]]])
        self.nodeDeformation = np.array([])
        self.nodeForce = np.array([])
        self.nodeStress = np.array([])
        pass
    def solve2d(self, node, material, section, structure, load, restrain):
        '''Solve Truss 2 dimension'''
        self.DOF = 2 # degree of freedom each node
        self.totalDOF = np.size(node.list, 0) * self.DOF
        self.assembleTrigonometri(structure, node)
        self.assembleLocalStiffness(structure, section, material)
        self.assembleGlobalStiffness(structure, node)
        self.assembleLoad(load, node)
        self.assembleUnsolvedMatrix(restrain, node)
        self.solveDeformation(restrain)
        self.solveInternalForceStress(structure, section, material)
        pass
    def assembleTrigonometri(self, structure, node):
        '''Stores value of sin and cos of angle
        that is formed beetween 2 nodes for
        each element in structure.
        
        Example
        -------
        Element 2 in structure is formed beetween
        node2: (x2=4,y2=3) and node1: (x1=0, y1=0). So,
        :math:`b = y2-y1 = 3-0 = 3`,
        :math:`a = x2-x1 = 4-0 = 4`, then using pythagoras
        :math:`c = 5`

        :math:`Sin = b/c`,
        :math:`Cos = a/c`,
        :math:`Tan = a/b`
                
        '''
        for element in structure.list:
            # n1 & n2 are number of nodes for each element
            # ArrayIndexing
            n1, n2 = element[0]-1, element[1]-1

            # a is length of coordinate of node 2 and node 1 in x direction
            # b is length of coordinate of node 2 and node 1 in y direction
            # c is real length of node 1 and node 2
            # iX and iY are index position of coordinates X & Y, ArrayIndexing
            iX, iY = 0, 1
            a = node.list[n2][iX] - node.list[n1][iX]
            b = node.list[n2][iY] - node.list[n1][iY]
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
    def assembleLocalStiffness(self, structure, section, material):
        '''Assemble local stiffness of each element
        Local stiffness is also known as element stiffness
        '''
        i = 0
        # All index number below are using ArrayIndexing
        indexArea = 0
        indexYoungModulus = 2
        indexLength = 3
        for element in structure.list:
            #ArrayIndexing
            numberSection = element[2]-1
            
            A = section.list[numberSection, indexArea]
            typeMaterial = section.list[numberSection, indexYoungModulus]-1
            E = material.list[typeMaterial][3]
            L = self.dataTrigonometri[i][indexLength]
            B = A * E / L

            S = self.dataTrigonometri[i][0]
            C = self.dataTrigonometri[i][1]
            
            matrix = [[C*C,   C*S, -C*C, -C*S],
                      [C*S,   S*S, -C*S, -S*S],
                      [-C*C, -C*S,  C*C,  C*S],
                      [-C*S, -S*S,  C*S,  S*S]]
            matrix = np.dot(matrix, B)

            if self.localStiffnessMatrix.size == 0:
                self.localStiffnessMatrix = np.array([matrix])
            else:
                self.localStiffnessMatrix= np.append(self.localStiffnessMatrix, \
                                                    [matrix], axis=0)
            i = i+1
        pass
    def assembleGlobalStiffness(self, structure, node):
        ''' Assemble global stiffness of structures'''
        self.globalStiffnessMatrix = np.array(np.zeros((self.totalDOF, self.totalDOF)))
        
        i = 0
        for element in structure.list:
            # n1 & n2 are number of nodes for each element
            # ArrayIndexing
            n1, n2 = element[0], element[1]
            
            #ArrayIndexing
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
        '''Assemble load matrix'''
        self.loadMatrix = np.array(np.zeros((self.totalDOF,1)))
        for load in load.list:
            node = load[0]
            Fx = load[1]
            Fy = load[2]
            self.loadMatrix[2*node-2:2*node] += [[Fx], [Fy]]
        pass
    def assembleUnsolvedMatrix(self, restrain, node):
        '''Construct unsolved matrix.
        Unsolved matrix is consist of matrix of global stiffness of node
        which are not restrained and matrix of load at unrestrained node.
        '''
        # construct array number of unrestrained node
        sequence = np.arange(self.totalDOF)
        unrestrainedNode=[]
        for i in sequence:
            if i not in restrain.list:
                unrestrainedNode += [i]
        self.unrestrainedNode = np.array(unrestrainedNode)

        unsolvedStiffness = self.globalStiffnessMatrix[np.ix_(self.unrestrainedNode, self.unrestrainedNode)]
        unsolvedLoad = self.loadMatrix[np.ix_(self.unrestrainedNode)]

        self.unsolvedGlobalStiffnessMatrix = np.array(unsolvedStiffness)
        self.unsolvedLoadMatrix = np.array(unsolvedLoad)
        
        # Calculate final load due to settlement
        self.unsolvedLoadMatrixWithSettlement = self.unsolvedLoadMatrix
        for deformation in restrain.settlement:
            n = deformation[0]-1
            dx = deformation[1]
            dy = deformation[2]
            self.unsolvedLoadMatrixWithSettlement = \
                self.unsolvedLoadMatrixWithSettlement \
                - self.globalStiffnessMatrix[n, n] * dx \
                - self.globalStiffnessMatrix[n+1, n+1] * dy
        pass
    def solveDeformation(self,restrain):
        '''Find deformation for each node'''
        self.nodeDeformation = np.zeros((self.totalDOF, 1))
        # Use least-square function
        # TODO: use try except to handle singular matrix using lnsqt
        unknownNodeDeformation = np.linalg.solve(self.unsolvedGlobalStiffnessMatrix,\
                                                 self.unsolvedLoadMatrixWithSettlement)
        self.nodeDeformation[self.unrestrainedNode] = unknownNodeDeformation
        self.nodeDeformation[restrain.list] = 0
        for deformation in restrain.settlement:
            n = deformation[0]-1
            dx = deformation[1]
            dy = deformation[2]
            self.nodeDeformation[n] =+ dx
            self.nodeDeformation[n+1] += dy
    def solveInternalForceStress(self, structure, section, material):
        '''Calculate internal force for each node'''
        # All index number below are using ArrayIndexing
        indexArea = 0
        indexYoungModulus = 2
        indexLength = 3
        i = 0
        for element in structure.list:
            #NormalIndexing
            n1, n2 = element[0], element[1]
            #ArrayIndexing
            numberSection = element[2]-1
            
            A = section.list[numberSection, indexArea]
            typeMaterial = section.list[numberSection, indexYoungModulus]-1
            E = material.list[typeMaterial][3]
            L = self.dataTrigonometri[i][indexLength]
            B = E / L

            S = self.dataTrigonometri[i][0]
            C = self.dataTrigonometri[i][1]
                        
            matrix = [[C, S, 0, 0],
                      [0, 0, C, S]]

            #Stress
            s = np.dot(B, np.array([[1,  -1]]))
            s = np.dot(s, matrix)
            s = np.dot(s, self.nodeDeformation[np.ix_([2*n1-2,2*n1-1, 2*n2-2,2*n2-1])])

            #Force
            f = np.dot(B*A, np.array([[1,  -1],
                               [-1,  1]]))
            f = np.dot(f, matrix)
            f = np.dot(f, self.nodeDeformation[np.ix_([2*n1-2,2*n1-1, 2*n2-2,2*n2-1])])

            if self.nodeForce.size == 0:
                self.nodeStress = np.array(s)
                self.nodeForce = np.array(f)
            else:
                self.nodeStress = np.append(self.nodeStress, s, axis=0)
                self.nodeForce = np.append(self.nodeForce, f, axis=0)
            i = i+1
        pass    