"""
All commonly used symbols / helper variables for the user.

Includes commonly used variables, trig functions,
colors for function styles, and parametrics.

Author: Evan Le
Date: 2026-10-21
License: Personal Use
"""

import math

from .function import Variable
from .parametric import Parametric
from .sinusoid import Sinusoid, TrigType
from .logarithm import Logarithm

# Variables

X = Variable("x")
Y = Variable("y")
T = Variable("t")

# Simplistic functions

def SIN(arg):
    return Sinusoid(arg=arg, trig_type=TrigType.SIN)

def COS(arg):
    return Sinusoid(arg=arg, trig_type=TrigType.COS)

def TAN(arg):
    return Sinusoid(arg=arg, trig_type=TrigType.TAN)

def CSC(arg):
    return Sinusoid(arg=arg, trig_type=TrigType.CSC)

def SEC(arg):
    return Sinusoid(arg=arg, trig_type=TrigType.SEC)

def COT(arg):
    return Sinusoid(arg=arg, trig_type=TrigType.COT)

def LOG(arg, base=10):
    return Logarithm(arg=arg, base=base)

def LN(arg):
    return Logarithm(arg=arg, base=math.e)

# Colors
# T = Tuple
RED     = (255,0,0)
ORANGE  = (255,160,16)
YELLOW  = (255,255,0)
GREEN   = (0,255,0)
BLUE    = (0,0,255)
CYAN    = (0,255,255)
PURPLE  = (160,32,255)
MAGENTA = (255,0,255)
PINK    = (255,96,208)
BROWN   = (160,128,96)

WHITE   = (255,255,255)
BLACK   = (0,0,0)
GRAY    = (128,128,128)

# Thicknesses
THIN    = 2
MED     = 4
THICK   = 6

# Numbers
PI      = math.pi
E       = math.e
π       = PI

# Parametrics

def PARAMETRIC_CIRCLE(r: float, center: tuple):
    return Parametric(argX=r*Sinusoid(trig_type=TrigType.COS) + center[0], argY=r*Sinusoid() + center[1], tMin=0, tMax=2*PI)

def PARAMETRIC_ELLIPSE(r1: float, r2: float, center: tuple):
    return Parametric(argX=r1*Sinusoid(trig_type=TrigType.COS) + center[0], argY=r2*Sinusoid() + center[1], tMin=0, tMax=2*PI)




