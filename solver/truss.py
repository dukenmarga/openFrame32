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
        pass
    def solve2d(self, model, rec):
        '''Solve Truss 2 dimension'''
        self.DOF = 2 # degree of freedom each node
        self.totalNode = np.size(model.node.list, 0)
        self.totalMember = np.size(model.structure.list, 0)
        self.totalDOF = self.totalNode * self.DOF
        self.assembleTrigonometri(model, rec)
        self.assembleLocalStiffness(model, rec)
        self.assembleGlobalStiffness(model, rec)
        self.assembleLoad(model, rec)
        self.assembleUnsolvedMatrix(model, rec)
        self.solveDeformation(model, rec)
        self.solveInternalForceStress(model, rec)
        pass
    def assembleTrigonometri(self, model, rec):
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
        # ELEMENT
        structure = model.structure
        node = model.node
        restrain = model.restrain
        
        for element in structure.list:
            if self.totalMember == 0:
                break
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
            if rec.pre.T.size == 0:
                rec.pre.T = np.array([[S, C, T, length]])
            else:
                rec.pre.T = np.append(rec.pre.T, [[S, C, T, length]], axis=0)
        

        # SPRING
        for spring in restrain.spring:
            # S=sin C=cos T=tan
            S = maths.sin(spring[2])
            C = maths.cos(spring[2])
            if C < 1e-10:
                C = 0
            T = 0

            length = 0
            # Store trigonometri data of each element
            if rec.pre.T.size == 0:
                rec.pre.T = np.array([[S, C, T, length]])
            else:
                rec.pre.T = np.append(rec.pre.T, [[S, C, T, length]], axis=0)
        pass
    def assembleLocalStiffness(self, model, rec):
        '''Assemble local stiffness of each element
        Local stiffness is also known as element stiffness
        '''
        i = 0
        # All index number below are using ArrayIndexing
        indexArea = 0
        indexYoungModulus = 2
        indexLength = 3

        # LOCAL STIFFNESS FROM ELEMENT
        structure = model.structure
        section = model.section
        material = model.material
        restrain = model.restrain
        for element in structure.list:
            if self.totalMember == 0:
                break
            #ArrayIndexing
            numberSection = element[2]-1
            
            A = section.list[numberSection, indexArea]
            typeMaterial = section.list[numberSection, indexYoungModulus]-1
            E = material.list[typeMaterial][3]
            L = rec.pre.T[i][indexLength]
            B = A * E / L

            S = rec.pre.T[i][0]
            C = rec.pre.T[i][1]
            
            matrix = [[C*C,   C*S, -C*C, -C*S],
                      [C*S,   S*S, -C*S, -S*S],
                      [-C*C, -C*S,  C*C,  C*S],
                      [-C*S, -S*S,  C*S,  S*S]]
            matrix = np.dot(matrix, B)

            if rec.pre.localStiffnessMatrix.size == 0:
                rec.pre.localStiffnessMatrix = np.array([matrix])
            else:
                rec.pre.localStiffnessMatrix= np.append(rec.pre.localStiffnessMatrix, \
                                                    [matrix], axis=0)
            i = i+1
        
        # LOCAL STIFFNESS FROM SPRING
        i = self.totalMember
        for spring in restrain.spring:
            k = spring[1]

            S = rec.pre.T[i][0]
            C = rec.pre.T[i][1]
            
            matrix = [[C*C,   C*S, -C*C, -C*S],
                      [C*S,   S*S, -C*S, -S*S],
                      [-C*C, -C*S,  C*C,  C*S],
                      [-C*S, -S*S,  C*S,  S*S]]
            matrix = np.dot(matrix, k)

            if rec.pre.localStiffnessMatrix.size == 0:
                rec.pre.localStiffnessMatrix = np.array([matrix])
            else:
                rec.pre.localStiffnessMatrix= np.append(rec.pre.localStiffnessMatrix, \
                                                    [matrix], axis=0)
            i = i+1
        pass
    def assembleGlobalStiffness(self, model, rec):
        ''' Assemble global stiffness of structures'''
        rec.pre.globalStiffnessMatrix = np.array(np.zeros((self.totalDOF, self.totalDOF)))
        
        # ELEMENT
        i = 0
        structure = model.structure
        for element in structure.list:
            # n1 & n2 are number of nodes for each element
            # ArrayIndexing
            n1, n2 = element[0], element[1]
            
            #ArrayIndexing
            a1 = 2*n1-2
            a2 = 2*n1
            b1 = 2*n2-2
            b2 = 2*n2
            rec.pre.globalStiffnessMatrix[a1:a2, a1:a2] += rec.pre.localStiffnessMatrix[i, 0:2, 0:2]
            rec.pre.globalStiffnessMatrix[a1:a2, b1:b2] += rec.pre.localStiffnessMatrix[i, 0:2, 2:4]
            rec.pre.globalStiffnessMatrix[b1:b2, a1:a2] += rec.pre.localStiffnessMatrix[i, 2:4, 0:2]
            rec.pre.globalStiffnessMatrix[b1:b2, b1:b2] += rec.pre.localStiffnessMatrix[i, 2:4, 2:4]
            i = i+1
            pass

        # SPRING
        i = self.totalMember
        restrain = model.restrain
        for spring in restrain.spring:
            # n is number of spring nodes 
            # ArrayIndexing
            n = spring[0]
            
            #ArrayIndexing
            a1 = 2*n-2
            a2 = 2*n
            rec.pre.globalStiffnessMatrix[a1:a2, a1:a2] += rec.pre.localStiffnessMatrix[i, 0:2, 0:2]
            i = i+1
        pass
    def assembleLoad(self, model, rec):
        '''Assemble load matrix'''
        rec.pre.loadMatrix = np.array(np.zeros((self.totalDOF,1)))
        load = model.load
        for load in load.list:
            node = load[0]
            Fx = load[1]
            Fy = load[2]
            rec.pre.loadMatrix[2*node-2:2*node] += [[Fx], [Fy]]
        pass
    def assembleUnsolvedMatrix(self, model, rec):
        '''Construct unsolved matrix.
        Unsolved matrix is consist of matrix of global stiffness of node
        which are not restrained and matrix of load at unrestrained node.
        '''
        # construct array number of unrestrained node
        sequence = np.arange(self.totalDOF)
        unrestrainedNode=[]
        restrain = model.restrain
        for i in sequence:
            if i not in restrain.list:
                unrestrainedNode += [i]
        self.unrestrainedNode = np.array(unrestrainedNode)

        unsolvedStiffness = rec.pre.globalStiffnessMatrix[np.ix_(self.unrestrainedNode, self.unrestrainedNode)]
        unsolvedLoad = rec.pre.loadMatrix[np.ix_(self.unrestrainedNode)]

        rec.pre.unsolvedGlobalStiffnessMatrix = np.array(unsolvedStiffness)
        rec.pre.unsolvedLoadMatrix = np.array(unsolvedLoad)
        
        # Calculate final load due to settlement
        rec.pre.unsolvedLoadMatrixWithSettlement = rec.pre.unsolvedLoadMatrix
        for deformation in restrain.settlement:
            n = deformation[0]-1
            dx = deformation[1]
            dy = deformation[2]
            rec.pre.unsolvedLoadMatrixWithSettlement = \
                rec.pre.unsolvedLoadMatrixWithSettlement \
                - rec.pre.globalStiffnessMatrix[n, n] * dx \
                - rec.pre.globalStiffnessMatrix[n+1, n+1] * dy
        pass
    def solveDeformation(self,model, rec):
        '''Find deformation for each node'''
        restrain = model.restrain
        rec.post.nodeDeformation = np.zeros((self.totalDOF, 1))
        # Use least-square function
        # TODO: use try except to handle singular matrix using lnsqt
        
        unknownNodeDeformation = np.linalg.solve(rec.pre.unsolvedGlobalStiffnessMatrix,\
                                                 rec.pre.unsolvedLoadMatrixWithSettlement)
        rec.post.nodeDeformation[self.unrestrainedNode] = unknownNodeDeformation
        rec.post.nodeDeformation[restrain.list] = 0
        for deformation in restrain.settlement:
            n = deformation[0]-1
            dx = deformation[1]
            dy = deformation[2]
            rec.post.nodeDeformation[n] =+ dx
            rec.post.nodeDeformation[n+1] += dy
    def solveInternalForceStress(self, model, rec):
        '''Calculate internal force for each node'''
        # All index number below are using ArrayIndexing
        indexArea = 0
        indexYoungModulus = 2
        indexLength = 3
        i = 0
        structure = model.structure
        section = model.section
        material = model.material
        for element in structure.list:
            #NormalIndexing
            n1, n2 = element[0], element[1]
            #ArrayIndexing
            numberSection = element[2]-1
            
            A = section.list[numberSection, indexArea]
            typeMaterial = section.list[numberSection, indexYoungModulus]-1
            E = material.list[typeMaterial][3]
            L = rec.pre.T[i][indexLength]
            B = E / L

            S = rec.pre.T[i][0]
            C = rec.pre.T[i][1]
                        
            matrix = [[C, S, 0, 0],
                      [0, 0, C, S]]

            #Stress
            s = np.dot(B, np.array([[1,  -1]]))
            s = np.dot(s, matrix)
            s = np.dot(s, rec.post.nodeDeformation[np.ix_([2*n1-2,2*n1-1, 2*n2-2,2*n2-1])])

            #Force
            f = np.dot(B*A, np.array([[1,  -1],
                               [-1,  1]]))
            f = np.dot(f, matrix)
            f = np.dot(f, rec.post.nodeDeformation[np.ix_([2*n1-2,2*n1-1, 2*n2-2,2*n2-1])])

            if rec.post.nodeForce.size == 0:
                rec.post.nodeStress = np.array(s)
                rec.post.nodeForce = np.array(f)
            else:
                rec.post.nodeStress = np.append(rec.post.nodeStress, s, axis=0)
                rec.post.nodeForce = np.append(rec.post.nodeForce, f, axis=0)
            i = i+1
        pass