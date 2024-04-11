# openFrame32
# Copyright (c) 2014 Duken Marga Turnip
# License: BSD 3-clause
# (https://github.com/dukenmarga/openFrame32/blob/master/LICENSE.txt)

import math


def sin(x: float) -> float:
    return math.sin(x * math.pi / 180)


def cos(x: float) -> float:
    return math.cos(x * math.pi / 180)


def tan(x: float) -> float:
    return math.tan(x * math.pi / 180)


def sec(x: float) -> float:
    return 1 / (sin(x))


def cosec(x: float) -> float:
    return 1 / (cos(x))


def cotan(x: float) -> float:
    return 1 / (tan(x))


def S(x: float) -> float:
    return sin(x)


def C(x: float) -> float:
    return cos(x)


def T(x: float) -> float:
    return tan(x)


def SC(x: float) -> float:
    return sec(x)


def CSC(x: float) -> float:
    return cosec(x)


def CT(x: float) -> float:
    return cotan(x)


def p(x: float, y: float) -> float:
    """return x^y
    Example:
    p(3,2) = 16"""
    return math.pow(x, y)


def hypotenuse(a: float, b: float) -> float:
    """return the length of the longest side of
    right-triangle
    Example:
    hypotenuse(3,4) = 5
    hypotenuse(5,12) = 13
    """
    return math.sqrt(math.pow(a, 2) + math.pow(b, 2))
