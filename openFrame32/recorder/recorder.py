# openFrame32
# Copyright (c) 2014 Duken Marga Turnip
# License: BSD 3-clause
# (https://github.com/dukenmarga/openFrame32/blob/master/LICENSE.txt)

from openFrame32.recorder.post import Post
from openFrame32.recorder.pre import Pre


class Recorder:
    def __init__(self):
        self.pre = Pre()
        self.post = Post()
        pass
