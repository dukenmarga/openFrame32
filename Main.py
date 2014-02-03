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

from model.structure import Structure
from model.material import Material
from model.section import Section
from model.node import Node
from model.load import Load
from model.restrain import Restrain
from solver.truss import Truss

'''
    Node, element, material, load, and section numbering are using
    normal increment start from 1 (not Zero), see below.
    Altough python is using numbering from 0, just
    let the program do the rest.
    Main program must be clear and readable and must not confuse people.
'''

# Define material's properties
material = Material()
material.addMaterial('concrete', F=30000000) #material 1 (not Zero)
material.addMaterial('steel', F=400000000, Fu=600000000) #material 2

# Define section property.
section = Section()
section.AddSection(area=0.04, secondInertia=0.0001333, material=1) # section 1 using material 1
section.AddSection(area=0.09, secondInertia=0.0006750, material=2) # section 2 using material 2

# Define node.
node = Node()
node.addNode(0,0) # node 1
#node.addNode(5,5) # node 2
#node.addNode(10,0) # node 3
node.addNode(10,0) # node 4

# Define main structure.
structure = Structure()
structure.AddElement((1, 2), section=2) # node 1 + node 2 using section 1
#structure.AddElement((2, 3), section=2) # node 2 + node 3 using section 2
#structure.AddElement((2, 4), section=2)

# Define load.
load = Load()
load.addLoad(2, Fx=10000) # load 1 at node 2 (Newton)

# Define restrain.
restrain = Restrain()
restrain.addRestrain(1, 'pin') # node 1 is pin
restrain.addRestrain(2, 'roller') # node 3 is roller
#restrain.addRestrain(4, 'pin') # node 4 is roller

truss = Truss()
truss.solve2d(node, material, section, structure, load, restrain)
print "Trigonometri: "
print truss.dataTrigonometri
print ""
print "Local Stiffness Matrix:"
print truss.localStiffnessMatrix
print "Global Stiffness Matrix:"
print truss.globalStiffnessMatrix
print "Load Matrix:"
print truss.loadMatrix
print "Unsolved stiffness matrix:"
print truss.unsolvedGlobalStiffnessMatrix
print "Unsolve load matrix:"
print truss.unsolvedLoadMatrix
print "Solution"
print truss.solution

#print np.allclose(np.dot(truss.unsolvedGlobalStiffnessMatrix, truss.solution), truss.unsolvedLoadMatrix)
