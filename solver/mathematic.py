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

import math

def sin(x):
    return math.sin(x*math.pi/180)
def cos(x):
    return math.cos(x*math.pi/180)
def tan(x):
    return math.tan(x*math.pi/180)
def sec(x):
    return 1/(sin(x))
def cosec(x):
    return 1/(cos(x))
def cotan(x):
    return 1/(tan(x))
    
def S(x):
    return sin(x)
def C(x):
    return cos(x)
def T(x):
    return tan(x)
def SC(x):
    return sec(x)
def CSC(x):
    return cosec(x)
def CT(x):
    return cotan(x)
def p(x, y):
    '''return x^y
    Example:
    p(3,2) = 16'''
    return math.pow(x, y)
def hypotenuse(a, b):
    '''return the length of the longest side of
    right-triangle
    Example:
    hypotenuse(3,4) = 5
    hypotenuse(5,12) = 13
    '''
    return math.sqrt(math.pow(a, 2) + math.pow(b, 2))