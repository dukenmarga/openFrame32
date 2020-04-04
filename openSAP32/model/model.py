# openSAP32
# Copyright (c) 2014 Duken Marga Turnip
# License: BSD 3-clause
# (https://github.com/dukenmarga/openSAP32/blob/master/LICENSE.txt)

from openSAP32.model.structure import Structure
from openSAP32.model.material import Material
from openSAP32.model.section import Section
from openSAP32.model.node import Node
from openSAP32.model.load import Load
from openSAP32.model.restrain import Restrain


class Model():
    def __init__(self):
        self.structure = Structure()
        self.material = Material()
        self.section = Section()
        self.node = Node()
        self.load = Load()
        self.restrain = Restrain()
        pass
