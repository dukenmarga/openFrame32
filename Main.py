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

from model.model import Model
from recorder.recorder import Recorder
from solver.truss import Truss
#from gui.draw import Draw

'''
    Node, element, material, load, and section numbering are using
    normal increment start from 1 (not Zero), see below.
    Altough python is using numbering from 0, just
    let the program do the rest.
    Main program must be clear and readable and must not confuse people.
'''

model = Model()
# Define material's properties
#material = Material()
model.material.addMaterial('concrete', F=30000000, E=210000000) #material 1 (not Zero)
#material.addMaterial('steel', F=400000000, Fu=600000000) #material 2

# Define section property.
#section = Section()
model.section.AddSection(area=6e-4, secondInertia=0.0001333, material=1) # section 1 using material 1
#section.AddSection(area=0.09, secondInertia=0.0006750, material=2) # section 2 using material 2

# Define node.
#node = Node()
model.node.addNode(0,0) # node 1
model.node.addNode(0,4) # node 2
model.node.addNode(3,4) # node 3
#node.addNode(120,0) # node 4

# Define main structure.
#structure = Structure()
model.structure.AddElement((1, 3), section=1) # node 1 + node 2 using section 1
model.structure.AddElement((2, 3), section=1) # node 2 + node 3 using section 2
#structure.AddElement((1, 4), section=1)

# Define load.
#load = Load()
model.load.addLoad(3, Fy=1000) # load 1 at node 2 (Newton)

# Define restrain.
#restrain = Restrain()
#restrain.addRestrain(3, 'pin') # node 1 is pin
model.restrain.addRestrain(2, 'pin') # node 3 is roller
#restrain.addSpring(3, k=100000, direction='y') #node 3 is spring
model.restrain.addRestrain(1, 'pin') # node 4 is roller
#restrain.addSettlement(1, (-0.05, 0.0))

truss = Truss()
rec = Recorder()
truss.solve2d(model, rec)

#draw = Draw()
#draw.drawSimple(structure,node)

print "Trigonometri: "
print rec.pre.T
print ""
print "Local Stiffness Matrix:"
print rec.pre.localStiffnessMatrix
print "Global Stiffness Matrix:"
print rec.pre.globalStiffnessMatrix
print "Load Matrix:"
print rec.pre.loadMatrix
print "Unsolved stiffness matrix:"
print rec.pre.unsolvedGlobalStiffnessMatrix
print "Unsolved load matrix:"
print rec.pre.unsolvedLoadMatrix
print "Deformation"
print rec.post.nodeDeformation
print "Force"
print rec.post.nodeForce
print "Stress"
print rec.post.nodeStress
print rec.pre.unsolvedLoadMatrixWithSettlement