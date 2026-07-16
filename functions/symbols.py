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

SIN = Sinusoid.from_basic(TrigType.SIN)
COS = Sinusoid.from_basic(TrigType.COS)
TAN = Sinusoid.from_basic(TrigType.TAN)
CSC = Sinusoid.from_basic(TrigType.CSC)
SEC = Sinusoid.from_basic(TrigType.SEC)
COT = Sinusoid.from_basic(TrigType.COT)
LOG = Logarithm.from_basic(10)
LN  = Logarithm.from_basic(math.e)

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
THIN = 2
MED = 4
THICK = 6

# Numbers
PI = math.pi
E = math.e

# Parametrics

def PARAMETRIC_CIRCLE(r: float):
    return Parametric(argX=r*Sinusoid(trig_type=TrigType.COS), argY=r*Sinusoid())

def PARAMETRIC_ELLIPSE(r1: float, r2: float):
    return Parametric(argX=r1*Sinusoid(trig_type=TrigType.COS), argY=r2*Sinusoid())




