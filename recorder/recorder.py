# openSAP32
# Copyright (c) 2014 Duken Marga Turnip
# License: BSD 3-clause
# (https://github.com/dukenmarga/openSAP32/blob/master/LICENSE.txt)

from pre import Pre
from post import Post

class Recorder():
    def __init__(self):
        self.pre = Pre()
        self.post = Post()
        pass
    