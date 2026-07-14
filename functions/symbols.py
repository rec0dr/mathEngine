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
T_RED     = (255,0,0)
T_ORANGE  = (255,160,16)
T_YELLOW  = (255,255,0)
T_GREEN   = (0,255,0)
T_BLUE    = (0,0,255)
T_CYAN    = (0,255,255)
T_PURPLE  = (160,32,255)
T_MAGENTA = (255,0,255)
T_PINK    = (255,96,208)
T_BROWN   = (160,128,96)

T_WHITE   = (255,255,255)
T_BLACK   = (0,0,0)
T_GRAY    = (128,128,128)




