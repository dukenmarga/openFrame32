# openSAP32
# Copyright (c) 2014 Duken Marga Turnip
# License: BSD 3-clause
# (https://github.com/dukenmarga/openSAP32/blob/master/LICENSE.txt)

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