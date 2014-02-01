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
from solver.truss import Truss

'''
    Node, element, material, load, and section numbering are using
    normal increment start from 1 (not Zero), see below.
    Altough python is using numbering from 0, just
    let the program do the rest.
    Main program must be clear and readable and must not confuse people.
'''

# Define material property.
material = Material()
material.addMaterial('concrete', F=30) #material 1 (not Zero)
material.addMaterial('steel', F=400, Fu=600) #material 2

# Define section property.
section = Section()
section.AddSection(area=100, secondInertia=400, material=1) # section 1 using material 1
section.AddSection(area=200, secondInertia=500, material=2) # section 2 using material 2

# Define node.
node = Node()
node.addNode(0,0) # node 1
node.addNode(5,5) # node 2
node.addNode(10,0) # node 3

# Define main structure.
structure = Structure()
structure.AddElement((1, 2), section=1) # node 1 + node 2 using section 1
structure.AddElement((2, 3), section=2) # node 2 + node 3 using section 2

# Define load.
load = Load()
load.addLoad(2, 200) # load 1 at node 2

truss = Truss()
truss.solve2d(node, material, section, structure, load)
#print "Trigonometri: "
#print truss.dataTrigonometri
#print ""
print "Local Stiffness Matrix:"
print truss.localStiffnessMatrix
print "Global Stiffness Matrix"
print truss.globalStiffnessMatrix