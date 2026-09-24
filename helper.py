import math
import random

from anim.__init__ import *
from functions.__init__ import *
from styles.__init__ import *
from objects.__init__ import *
from graphing.__init__ import *

def bezier(p0, p1, p2, p3, p4):
    t0 = ((1 - X) ** 4) * p0
    t1 = ((1 - X) ** 3) * X * p1
    t2 = ((1 - X) ** 2) * (X**2) * p2
    t3 = ((1 - X)) * (X**3) * p3
    t4 = (X**4) * p4
    return t0 + t1 + t2 + t3 + t4