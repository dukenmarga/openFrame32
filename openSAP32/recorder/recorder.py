# openSAP32
# Copyright (c) 2014 Duken Marga Turnip
# License: BSD 3-clause
# (https://github.com/dukenmarga/openSAP32/blob/master/LICENSE.txt)

from openSAP32.recorder.pre import Pre
from openSAP32.recorder.post import Post

class Recorder():
    def __init__(self):
        self.pre = Pre()
        self.post = Post()
        pass
    
