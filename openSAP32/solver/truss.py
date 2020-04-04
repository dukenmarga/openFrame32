# openSAP32
# Copyright (c) 2014 Duken Marga Turnip
# License: BSD 3-clause
# (https://github.com/dukenmarga/openSAP32/blob/master/LICENSE.txt)

import numpy as np
import openSAP32.solver.mathematic as maths

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
        self.INDEX_AREA = 0
        self.INDEX_YOUNG_MODULUS = 3
        self.INDEX_LENGTH = 3
        self.INDEX_SECTION = 2
        self.INDEX_MATERIAL = 2
        self.INDEX_SIN = 0
        self.INDEX_COS = 1
        self.INDEX_ANGLE = 2
        self.INDEX_SPRING_STIFF = 1
        self.INDEX_NODE_1, self.INDEX_NODE_2 = 0, 1
        self.INDEX_POSITION_X, self.INDEX_POSITION_Y = 0, 1
        self.INDEX_NODE = 0
        self.INDEX_FX = 1
        self.INDEX_FY = 2
        self.INDEX_DX = 1
        self.INDEX_DY = 2
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
            # NODE_1 & NODE_2 are number of nodes for each element
            NODE_1, NODE_2 = element[self.INDEX_NODE_1]-1, element[self.INDEX_NODE_2]-1

            length_x = node.list[NODE_2][self.INDEX_POSITION_X] - node.list[NODE_1][self.INDEX_POSITION_X]
            length_y = node.list[NODE_2][self.INDEX_POSITION_Y] - node.list[NODE_1][self.INDEX_POSITION_Y]
            length_element = maths.hypotenuse(length_y, length_x)
            
            # S=sin C=cos T=tan
            S = length_y/length_element
            C = length_x/length_element
            T = 0
            
            # Store trigonometri data of each element
            if rec.pre.T.size == 0:
                rec.pre.T = np.array([[S, C, T, length_element]])
            else:
                rec.pre.T = np.append(rec.pre.T, [[S, C, T, length_element]], axis=0)
        

        # SPRING
        for spring in restrain.spring:
            # S=sin C=cos T=tan
            S = maths.sin(spring[self.INDEX_ANGLE])
            C = maths.cos(spring[self.INDEX_ANGLE])
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
        
        # LOCAL STIFFNESS FROM ELEMENT
        structure = model.structure
        section = model.section
        material = model.material
        restrain = model.restrain
        Trig = rec.pre.T
        for element in structure.list:
            if self.totalMember == 0:
                break
            
            NUM_SECTION = element[self.INDEX_SECTION]-1
            A = section.list[NUM_SECTION, self.INDEX_AREA]
            NUM_MATERIAL = int(section.list[NUM_SECTION, self.INDEX_MATERIAL]-1)
            E = material.list[NUM_MATERIAL][self.INDEX_YOUNG_MODULUS]
            L = Trig[i][self.INDEX_LENGTH]
            K = A * E / L
            
            S = Trig[i][self.INDEX_SIN]
            C = Trig[i][self.INDEX_COS]
            
            matrix = [[C*C,   C*S, -C*C, -C*S],
                      [C*S,   S*S, -C*S, -S*S],
                      [-C*C, -C*S,  C*C,  C*S],
                      [-C*S, -S*S,  C*S,  S*S]]
            matrix = np.dot(matrix, K)

            if rec.pre.localStiffnessMatrix.size == 0:
                rec.pre.localStiffnessMatrix = np.array([matrix])
            else:
                rec.pre.localStiffnessMatrix= np.append(rec.pre.localStiffnessMatrix, \
                                                    [matrix], axis=0)
            i = i+1
        
        # LOCAL STIFFNESS FROM SPRING
        i = self.totalMember
        for spring in restrain.spring:
            k = spring[self.INDEX_SPRING_STIFF]

            S = Trig[i][self.INDEX_SIN]
            C = Trig[i][self.INDEX_COS]
            
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
        localStiffnessMatrix = rec.pre.localStiffnessMatrix
        for element in structure.list:
            # NODE_1 & NODE_2 are number of nodes for each element
            NODE_1, NODE_2 = element[self.INDEX_POSITION_X], element[self.INDEX_POSITION_Y]
            
            #ArrayIndexing
            a1 = 2*NODE_1-2
            a2 = 2*NODE_1
            b1 = 2*NODE_2-2
            b2 = 2*NODE_2
            rec.pre.globalStiffnessMatrix[a1:a2, a1:a2] += localStiffnessMatrix[i, 0:2, 0:2]
            rec.pre.globalStiffnessMatrix[a1:a2, b1:b2] += localStiffnessMatrix[i, 0:2, 2:4]
            rec.pre.globalStiffnessMatrix[b1:b2, a1:a2] += localStiffnessMatrix[i, 2:4, 0:2]
            rec.pre.globalStiffnessMatrix[b1:b2, b1:b2] += localStiffnessMatrix[i, 2:4, 2:4]
            i = i+1
            pass

        # SPRING
        i = self.totalMember
        restrain = model.restrain
        for spring in restrain.spring:
            n = spring[self.INDEX_NODE]
            
            #ArrayIndexing
            a1 = 2*n-2
            a2 = 2*n
            rec.pre.globalStiffnessMatrix[a1:a2, a1:a2] += localStiffnessMatrix[i, 0:2, 0:2]
            i = i+1
        pass
    def assembleLoad(self, model, rec):
        '''Assemble load matrix'''
        rec.pre.loadMatrix = np.array(np.zeros((self.totalDOF,1)))
        load = model.load
        for load in load.list:
            node = load[self.INDEX_NODE]
            Fx = load[self.INDEX_FX]
            Fy = load[self.INDEX_FY]
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
        rec.pre.unrestrainedNode = np.array(unrestrainedNode)

        unsolvedStiffness = rec.pre.globalStiffnessMatrix[np.ix_(rec.pre.unrestrainedNode, rec.pre.unrestrainedNode)]
        unsolvedLoad = rec.pre.loadMatrix[np.ix_(rec.pre.unrestrainedNode)]

        rec.pre.unsolvedGlobalStiffnessMatrix = np.array(unsolvedStiffness)
        rec.pre.unsolvedLoadMatrix = np.array(unsolvedLoad)
        
        # Calculate final load due to settlement
        rec.pre.unsolvedLoadMatrixWithSettlement = rec.pre.unsolvedLoadMatrix
        unsolvedLoadMatrixWithSettlement = rec.pre.unsolvedLoadMatrixWithSettlement
        globalStiffnessMatrix = rec.pre.globalStiffnessMatrix
        for settlement in restrain.settlement:
            n = settlement[self.INDEX_NODE]-1
            dx = settlement[self.INDEX_DX]
            dy = settlement[self.INDEX_DY]
            rec.pre.unsolvedLoadMatrixWithSettlement = \
                unsolvedLoadMatrixWithSettlement \
                - globalStiffnessMatrix[n, n] * dx \
                - globalStiffnessMatrix[n+1, n+1] * dy
        pass
    def solveDeformation(self,model, rec):
        '''Find deformation for each node'''
        restrain = model.restrain
        rec.post.nodeDeformation = np.zeros((self.totalDOF, 1))
        # Use least-square function
        # TODO: use try except to handle singular matrix using lnsqt
        
        unknownNodeDeformation = np.linalg.solve(rec.pre.unsolvedGlobalStiffnessMatrix,\
                                                 rec.pre.unsolvedLoadMatrixWithSettlement)
        rec.post.nodeDeformation[rec.pre.unrestrainedNode] = unknownNodeDeformation
        rec.post.nodeDeformation[restrain.list] = 0
        for settlement in restrain.settlement:
            n = settlement[self.INDEX_NODE]-1
            dx = settlement[self.INDEX_DX]
            dy = settlement[self.INDEX_DY]
            rec.post.nodeDeformation[n] =+ dx
            rec.post.nodeDeformation[n+1] += dy
    def solveInternalForceStress(self, model, rec):
        '''Calculate internal force for each node'''
        i = 0
        structure = model.structure
        section = model.section
        material = model.material
        Trig = rec.pre.T

        for element in structure.list:
            #NormalIndexing
            NODE_1, NODE_2 = element[self.INDEX_POSITION_X], element[self.INDEX_POSITION_Y]
            #ArrayIndexing
            NUM_SECTION = element[self.INDEX_SECTION]-1
            
            A = section.list[NUM_SECTION, self.INDEX_AREA]
            NUM_MATERIAL = int(section.list[NUM_SECTION, self.INDEX_MATERIAL]-1)
            E = material.list[NUM_MATERIAL][self.INDEX_YOUNG_MODULUS]
            L = Trig[i][self.INDEX_LENGTH]
            K = E / L

            S = Trig[i][self.INDEX_SIN]
            C = Trig[i][self.INDEX_COS]
                        
            matrix = [[C, S, 0, 0],
                      [0, 0, C, S]]

            #Stress
            s = np.dot(K, np.array([[1,  -1]]))
            s = np.dot(s, matrix)
            s = np.dot(s, rec.post.nodeDeformation[np.ix_([2*NODE_1-2,2*NODE_1-1, 2*NODE_2-2,2*NODE_2-1])])

            #Force
            f = np.dot(K*A, np.array([[1,  -1],
                               [-1,  1]]))
            f = np.dot(f, matrix)
            f = np.dot(f, rec.post.nodeDeformation[np.ix_([2*NODE_1-2,2*NODE_1-1, 2*NODE_2-2,2*NODE_2-1])])

            if rec.post.nodeForce.size == 0:
                rec.post.nodeStress = np.array(s)
                rec.post.nodeForce = np.array(f)
            else:
                rec.post.nodeStress = np.append(rec.post.nodeStress, s, axis=0)
                rec.post.nodeForce = np.append(rec.post.nodeForce, f, axis=0)
            i = i+1
        pass
