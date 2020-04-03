# openSAP32
# Copyright (c) 2014 Duken Marga Turnip
# License: BSD 3-clause
# (https://github.com/dukenmarga/openSAP32/blob/master/LICENSE.txt)

from structure import Structure
from material import Material
from section import Section
from node import Node
from load import Load
from restrain import Restrain


class Model():
    def __init__(self):
        self.structure = Structure()
        self.material = Material()
        self.section = Section()
        self.node = Node()
        self.load = Load()
        self.restrain = Restrain()
        pass
