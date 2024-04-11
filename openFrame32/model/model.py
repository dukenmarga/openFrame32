# openFrame32
# Copyright (c) 2014 Duken Marga Turnip
# License: BSD 3-clause
# (https://github.com/dukenmarga/openFrame32/blob/master/LICENSE.txt)

from openFrame32.model.load import Load
from openFrame32.model.material import Material
from openFrame32.model.node import Node
from openFrame32.model.restrain import Restrain
from openFrame32.model.section import Section
from openFrame32.model.structure import Structure


class Model:
    def __init__(self):
        self.structure = Structure()
        self.material = Material()
        self.section = Section()
        self.node = Node()
        self.load = Load()
        self.restrain = Restrain()
        pass
