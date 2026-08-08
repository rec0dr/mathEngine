import math
import random

from anim.__init__ import *
from functions.__init__ import *
from styles.__init__ import *
from objects.__init__ import *
from graphing.__init__ import *

width, height = (600,600)
scaleX, scaleY = (10,10)

app = GraphApp(width, height, scaleX, scaleY, fps=90, pan_sensitivity=100, zoom_sensitivity=100, fixed_center = None)

t1 = LOG(X, 2)
t2 = LOG(X, 3)
k = TracedPoint(t1, 0)
pt = Point(app.analyzer.intersection(t1, t2, -10, 10))
app.add_dobjects(k, t1, t2)
app.add_graph_objects(GraphObject.from_atts(pt, color=BLUE))
app.add_animations(Animation(k, "parameter", 10, 10, EaseType.SIN_IN_OUT))
app.run()